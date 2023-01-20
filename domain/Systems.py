import statistics
from statistics import pvariance, variance

from calculation.calculation import calculateNormalMaCumulativeTotal
from dataIO.dataIO import getDatapointsFromDatabase
import abc
class systemTypes:
    NORMAL = 0
    VERSUS = 1
    CONFIRMATION = 2
class positions:
    LONG = 1
    SHORT = -1
    FLAT = 0
class Stat:
    gt = 0
    runningGt = []
    running30IncVariance = []
    runningWinCount = []
    runningLossCount = []
    runningTradeCount = []
    runningTieCount = []
    runningMaxWin = []
    runningMaxLoss = []
    runningWinTotal = []
    runningLossTotal = []
    tradeCount = 0
    winCount = 0
    lossCount = 0
    tieCount = 0
    maxWin = 0
    maxLoss = 0

    @staticmethod
    def printStatsHeading():
        headingWidth = 12
        print('GRAND TOTAL'.ljust(headingWidth) +
        'TRADE COUNT'.ljust(headingWidth) +
        'WIN COUNT'.ljust(headingWidth) +
        'LOSS COUNT'.ljust(headingWidth) +
        'AVG WIN'.ljust(headingWidth) +
        'AVG LOSS'.ljust(headingWidth) +
        'MAX WIN'.ljust(headingWidth) +
        'MAX LOSS'.ljust(headingWidth) +
        'W/L RATIO'.ljust(headingWidth) +
        'L/W RATIO'.ljust(headingWidth) +
        'DIVISORS'.ljust(headingWidth)
              )
    def print(self, divisors):
        headingWidth = 12
        print(
            str(format(self.runningGt[-1], '.2f')).ljust(headingWidth) +
            str(self.runningTradeCount[-1]).ljust(headingWidth) +
            str(self.runningWinCount[-1]).ljust(headingWidth) +
            str(self.runningLossCount[-1]).ljust(headingWidth) +
            str(format(float(self.runningWinTotal[-1])/float(self.runningWinCount[-1]), '.2f') if self.runningWinCount[-1] > 0 else '0').ljust(headingWidth) +
            str(format(float(self.runningLossTotal[-1])/float(self.runningLossCount[-1]), '.2f') if self.runningLossCount[-1] > 0 else '0').ljust(headingWidth) +
            str(format(self.runningMaxWin[-1], '.2f')).ljust(headingWidth) +
            str(format(self.runningMaxLoss[-1], '.2f')).ljust(headingWidth) +
            str(format(float(self.runningWinCount[-1])/float(self.runningLossCount[-1]), '.2f') if self.runningLossCount[-1] > 0 else "N/A").ljust(headingWidth) +
            str(format(float(self.runningLossCount[-1])/float(self.runningWinCount[-1]), '.2f') if self.runningWinCount[-1] > 0 else "N/A").ljust(headingWidth) +
            str(divisors)
        )

class Datapoint:
    datetime = None
    price = None

    def __init__(self, datetime, price):
        self.datetime = datetime
        self.price = price
class System:
    dbConnection = None
    datapoints: list[Datapoint] = []
    divisors = []
    systemType = None
    cumulativeTotal = []
    stats: Stat = None


    def __init__(self, divisors=None, systemType=None):
        self.divisors = divisors
        self.systemType = systemType
        self.stats = Stat()

    def calculate(self):
        data = [point.price for point in self.datapoints]
        if self.systemType == systemTypes.NORMAL:
            self.cumulativeTotal = calculateNormalMaCumulativeTotal(self.divisors, data, self.dbConnection)
        elif self.systemType == systemTypes.VERSUS:
            self.__calculateCumulativeTotalVersus(calculateNormalMaCumulativeTotal(self.divisors[0], data, self.dbConnection), calculateNormalMaCumulativeTotal(self.divisors[1], data, self.dbConnection))
        elif self.systemType == systemTypes.CONFIRMATION:
            self.__calculateCumulativeTotalConfirmation(calculateNormalMaCumulativeTotal(self.divisors[0], data, self.dbConnection), calculateNormalMaCumulativeTotal(self.divisors[1], data, self.dbConnection))
        self.__calculateStats()

    def __calculateStats(self):
        data = [datapoint.price for datapoint in self.datapoints]
        syscol = self.cumulativeTotal
        bid=data
        ask = data

        gt = 0
        runningGt = []
        running30IncVariance = []
        runningWinCount = []
        runningLossCount = []
        runningTradeCount = []
        runningTieCount = []
        runningMaxWin = []
        runningMaxLoss = []
        runningWinTotal = []
        runningLossTotal = []
        tradeCount = 0
        winCount = 0
        lossCount = 0
        tieCount = 0

        position = positions.FLAT
        positionPrice = 0
        price = 0
        winloss = 0
        maxWin = 0
        maxLoss = 0
        for i in range(len(syscol)):
            price = data[i]
            bidPrice = bid[i]
            askPrice = ask[i]
            if (syscol[i] > 0):  # the system is long
                if (position == positions.FLAT):
                    position = positions.LONG
                    positionPrice = askPrice  # you're going long so you're buying from the ASK
                elif (position == positions.SHORT):
                    # you've exited a short position and you're going long. Short selling aka 'Shorting' is selling a stock you down own by borrowing it from your broker.
                    # So to exit a short position, in which you have sold a stock, you must now buy one back (at the asking price) to exit the position
                    winloss = positionPrice - askPrice
                    if winloss == 0:
                        tieCount += 1
                    elif winloss < 0:
                        lossCount += 1
                    elif winloss > 0:
                        winCount += 1
                    gt += winloss
                    tradeCount += 1
                    position = positions.LONG
                    positionPrice = askPrice  # you're going long so you're buying from the ASK
            elif (syscol[i] < 0):  # The system is short
                if (position == positions.FLAT):
                    position = positions.SHORT
                    positionPrice = bidPrice  # Short selling aka 'Shorting' is selling a stock you down own by borrowing it from your broker. You can only sell NOW at the highest bid price.
                elif (position == positions.LONG):
                    # you've exited a long position to go short
                    winloss = bidPrice - positionPrice  # sell what you owned at the bidPrice
                    if winloss == 0:
                        tieCount += 1
                    elif winloss < 0:
                        lossCount += 1
                    elif winloss > 0:
                        winCount += 1
                    gt += winloss
                    tradeCount += 1
                    position = positions.SHORT
                    positionPrice = bidPrice  # Short selling aka 'Shorting' is selling a stock you down own by borrowing it from your broker. You can only sell NOW at the highest bid price.
            elif (syscol[i] == 0):  # The system is FLAT (no position)
                if (position == positions.LONG):
                    # you've exited a long position to go flat
                    winloss = bidPrice - positionPrice  # sell what you owned at the bidPrice
                    if winloss == 0:
                        tieCount += 1
                    elif winloss < 0:
                        lossCount += 1
                    elif winloss > 0:
                        winCount += 1
                    gt += winloss
                    tradeCount += 1
                elif (position == positions.SHORT):
                    # you've exited a short position and you're going long. Short selling aka 'Shorting' is selling a stock you down own by borrowing it from your broker.
                    # So to exit a short position, in which you have sold a stock, you must now buy one back (at the asking price) to exit the position
                    winloss = positionPrice - askPrice
                    if winloss == 0:
                        tieCount += 1
                    elif winloss < 0:
                        lossCount += 1
                    elif winloss > 0:
                        winCount += 1
                    gt += winloss
                    tradeCount += 1
                position = positions.FLAT
                positionPrice = price  # it's irrelevant what you make the positionPrice in a flat position. We'll just set it to the market price here.
            if (winloss > maxWin):
                maxWin = winloss
            elif (winloss < maxLoss):
                maxLoss = winloss

            runningGt.append(gt)
            # if len(runningGt) > 2 and winloss < 0:
            #     running30IncVariance.append(variance(runningGt[-30:]))
            # else:
            #     running30IncVariance.append(0)
            runningTradeCount.append(tradeCount)
            runningWinCount.append(winCount)
            runningLossCount.append(lossCount)
            runningTieCount.append(tieCount)
            runningMaxWin.append(maxWin)
            runningMaxLoss.append(maxLoss)

            if (i > 0 and winloss < 0):
                runningWinTotal.append(runningWinTotal[i - 1])
                runningLossTotal.append(winloss + runningLossTotal[i - 1])
            elif (i > 0 and winloss > 0):
                runningWinTotal.append(winloss + runningWinTotal[i - 1])
                runningLossTotal.append(runningLossTotal[i - 1])
            elif (i == 0 and winloss < 0):
                runningWinTotal.append(0)
                runningLossTotal.append(winloss)
            elif (i == 0 and winloss > 0):
                runningWinTotal.append(winloss)
                runningLossTotal.append(0)
            elif (i > 0 and winloss == 0):
                runningWinTotal.append(runningWinTotal[i - 1])
                runningLossTotal.append(runningLossTotal[i - 1])
            elif (i == 0 and winloss == 0):
                runningLossTotal.append(0)
                runningWinTotal.append(0)
            winloss = 0

        self.stats.gt = gt
        self.stats.tradeCount = tradeCount
        self.stats.winCount = winCount
        self.stats.lossCount = lossCount
        self.stats.maxWin = maxWin
        self.stats.maxLoss = maxLoss
        self.stats.runningGt = runningGt
        self.stats.runningWinCount = runningWinCount
        self.stats.runningLossCount = runningLossCount
        self.stats.runningTieCount = runningTieCount
        self.stats.runningTradeCount = runningTradeCount
        self.stats.runningMaxWin = runningMaxWin
        self.stats.runningMaxLoss = runningMaxLoss
        self.stats.runningWinTotal = runningWinTotal
        self.stats.runningLossTotal = runningLossTotal
        self.stats.running30IncVariance = running30IncVariance

    def __calculateCumulativeTotalVersus(self, cuma, cumb):
        self.cumulativeTotal = [cuma[i] - cumb[i] for i in range(len(cuma))] #VS cumulative total calculation

    def __calculateCumulativeTotalConfirmation(self, cuma, cumb):
        self.cumulativeTotal = [-1 if cuma[i] < 0 and cumb[i] < 0 else (1 if cuma[i] > 0 and cumb[i] > 0 else 0) for i in range(len(cuma))]  # conf cumulative total calculation

    def getDivisors(self):
        userinput = input("Enter systems, q to finish. ")
        if 'q' in userinput:
            return None
        elif 'vs' in userinput:
            self.systemType = systemTypes.VERSUS
            sides = userinput.split(" vs ")
            aTokens = [int(item) for item in sides[0].split(" ")]
            bTokens = [int(item) for item in sides[1].split(" ")]
            self.divisors = [aTokens, bTokens]
        elif 'conf' in userinput:
            self.systemType = systemTypes.CONFIRMATION
            sides = userinput.split(" conf ")
            aTokens = [int(item) for item in sides[0].split(" ")]
            bTokens = [int(item) for item in sides[1].split(" ")]
            self.divisors = [aTokens, bTokens]
        else:
            self.systemType = systemTypes.NORMAL
            self.divisors = [int(item) for item in userinput.split(" ")]
        return self.divisors
class Systems:
    dbConnection = None
    datapoints: list[Datapoint] = []
    systems: list[System] = []

    def __init__(self, dbConnection=None):
        self.dbConnection = dbConnection
        self.datapoints = getDatapointsFromDatabase(self.dbConnection)

    def setDbConnection(self, dbConnection):
        self.dbConnection = dbConnection
        self.datapoints = getDatapointsFromDatabase(self.dbConnection)
        for system in self.systems:
            system.datapoints = self.datapoints
            system.calculate()

    def addSystem(self, system: System):
        system.datapoints = self.datapoints
        self.systems.append(system)
        system.calculate()

    def clearSystems(self):
        for system in self.systems:
            self.systems.pop()

class TradingStrategyInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'calculate_cumulative_total') and
                callable(subclass.calculate_cumulative_total))

class NormalMovingAverageTradingStrategy:
    """Extract text from a PDF."""
    def calculate_cumulative_total(self, arg1: str, arg2: str) -> [Datapoint]:
        """Overrides TradingStrategyInterface.calculate_cumulative_total()"""
        pass
