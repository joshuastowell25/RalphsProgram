


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
        print(
            'BALANCE'.ljust(headingWidth) +
            'L/W RATIO'.ljust(headingWidth) +
            'W/L RATIO'.ljust(headingWidth) +
            'MAX LOSS'.ljust(headingWidth) +
            'MAX WIN'.ljust(headingWidth) +
            'AVG LOSS'.ljust(headingWidth) +
            'AVG WIN'.ljust(headingWidth) +
            'LOSS COUNT'.ljust(headingWidth) +
            'WIN COUNT'.ljust(headingWidth) +
            'TRADE COUNT'.ljust(headingWidth) +
            'GRAND TOTAL'.ljust(headingWidth) +
            'DIVISORS'.ljust(headingWidth)
        )
    def print(self, divisors, divsorBalance=1):
        headingWidth = 12
        print(
            str(format(divsorBalance, '.2f')).ljust(headingWidth) +  # Balance
            str(format(float(self.runningLossCount[-1]) / float(self.runningWinCount[-1]), '.2f') if self.runningWinCount[-1] > 0 else "N/A").ljust(headingWidth) +  # LW Ratio
            str(format(float(self.runningWinCount[-1]) / float(self.runningLossCount[-1]), '.2f') if self.runningLossCount[-1] > 0 else "N/A").ljust(headingWidth) +  # WL Ratio
            str(format(self.runningMaxLoss[-1], '.2f')).ljust(headingWidth) +  # Max Loss
            str(format(self.runningMaxWin[-1], '.2f')).ljust(headingWidth) +  # Max Win
            str(format(float(self.runningLossTotal[-1]) / float(self.runningLossCount[-1]), '.2f') if self.runningLossCount[-1] > 0 else '0').ljust(headingWidth) +  # Avg Loss
            str(format(float(self.runningWinTotal[-1]) / float(self.runningWinCount[-1]), '.2f') if self.runningWinCount[-1] > 0 else '0').ljust(headingWidth) +  # Avg Win
            str(self.runningLossCount[-1]).ljust(headingWidth) +  # Loss Count
            str(self.runningWinCount[-1]).ljust(headingWidth) +  # Win Count
            str(self.runningTradeCount[-1]).ljust(headingWidth) +  # Trade Count
            str(format(self.runningGt[-1], '.2f')).ljust(headingWidth) +  #GT
            str(divisors) +  #divisors
            ''
        )