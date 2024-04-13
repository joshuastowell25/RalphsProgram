import copy
import random

from calculation import calculateNormalMaCumulativeTotal
from domain import systemTypes, Stat, Datapoint, positions

class System:
    dbConnection = None
    datapoints: list[Datapoint] = []
    divisors = []
    systemType = None
    cumulativeTotal = []
    stats: Stat = None
    divisorBalance: float = 1

    def __init__(self, divisors=None, systemType=None):
        self.divisors = divisors
        self.systemType = systemType
        self.stats = Stat()

    def __str__(self):
        return f"TODO: systemType:{self.systemType}, divisors:{self.divisors}"

    def getDivisorString(self):
        if self.systemType == systemTypes.NORMAL:
            return ' '.join([str(divisor) for divisor in self.divisors])
        elif self.systemType == systemTypes.VERSUS:
            return ' '.join([str(divisor) for divisor in self.divisors[0]]) + " vs " + ' '.join([str(divisor) for divisor in self.divisors[1]])
        elif self.systemType == systemTypes.CONFIRMATION:
            return ' '.join([str(divisor) for divisor in self.divisors[0]]) + " conf " + ' '.join([str(divisor) for divisor in self.divisors[1]])

    def calculate(self):
        data = [point.price for point in self.datapoints]
        if self.systemType == systemTypes.NORMAL:
            self.cumulativeTotal = calculateNormalMaCumulativeTotal(self.divisors, data, self.dbConnection)
        elif self.systemType == systemTypes.VERSUS:
            self.__calculateCumulativeTotalVersus(calculateNormalMaCumulativeTotal(self.divisors[0], data, self.dbConnection), calculateNormalMaCumulativeTotal(self.divisors[1], data, self.dbConnection))
        elif self.systemType == systemTypes.CONFIRMATION:
            self.__calculateCumulativeTotalConfirmation(calculateNormalMaCumulativeTotal(self.divisors[0], data, self.dbConnection), calculateNormalMaCumulativeTotal(self.divisors[1], data, self.dbConnection))
        self.__calculateStats()

    @staticmethod
    def generateRandomDivisors(self):
        aParts = []
        bParts = []
        divisorCount = random.randint(1,10)
        for i in range(divisorCount):
            divisor = random.randint(1, 10) * 2 #random 2 through 20
            aParts.append(divisor)

    equivalencies = {
        4: [[2]*4],
        6: [[2]*9],
        8: [[2]*16, [4]*4],
        10: [[2]*25],
        12: [[2]*36, [6]*4],
        14: [[2]*49],
        16: [[2]*64, [8]*4, [4]*16],
        18: [[2]*81, [6]*9],
        20: [[2]*100, [10]*4]
    }
    def determineAllEquivalentDivisors(self, divisors: [int], depth = 0):
        equivalentDivisors = []

        for i in range(len(divisors)):
            newDivisors = copy.deepcopy(divisors)
            divisor = newDivisors.pop(i)

            if divisor != 2:
                for equivalency in self.equivalencies[divisor]:
                    sys = copy.deepcopy(newDivisors) + equivalency

                    if sys not in equivalentDivisors: #We don't want to append duplicates
                        equivalentDivisors.append(sys)

                        if depth > 0:
                            eqs = self.determineAllEquivalentDivisors(sys, depth-1)
                            for item in eqs:
                                if item not in equivalentDivisors:
                                    equivalentDivisors.append(item)

        return equivalentDivisors

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
        userinput = input("Enter system, q to finish.\nVersus Example: 10 space 20 space vs space 30 enter.\nPlain Example: 90 enter\n").strip()
        if 'q' in userinput:
            return None
        elif 'vs' in userinput:
            self.systemType = systemTypes.VERSUS
            sides = userinput.split("vs")
            aTokens = [int(item.strip()) for item in sides[0].strip().split()]
            bTokens = [int(item.strip()) for item in sides[1].strip().split()]
            self.divisors = [aTokens, bTokens]
            self.divisorBalance = sum([token * token for token in aTokens]) / sum([token * token for token in bTokens])
        elif 'conf' in userinput:
            self.systemType = systemTypes.CONFIRMATION
            sides = userinput.split("conf")
            aTokens = [int(item.strip()) for item in sides[0].strip().split()]
            bTokens = [int(item.strip()) for item in sides[1].strip().split()]
            self.divisors = [aTokens, bTokens]
            self.divisorBalance = sum([token * token for token in aTokens]) / sum([token * token for token in bTokens])
        else:
            self.systemType = systemTypes.NORMAL
            self.divisors = [int(item) for item in userinput.split(" ")]
        return self.divisors