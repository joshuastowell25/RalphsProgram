#!/usr/bin/env python
import os, sys, traceback
import charting
import shutil
import settings
from constants import MaTypes
from dataIO.dataIO import getDbConnection
from domain import Systems
from systems import printSystems, getSystems, enterSystemsMenu


# gets the number of lines in the terminal
def screenHeight():
    return shutil.get_terminal_size().lines


def screenWidth():
    return shutil.get_terminal_size().columns


# gets the users desired moving average type
def getMaType(ans=None):  # ans defaults to None
    if ans is None:
        ans = input("What type of moving average? (r for RalphStyle, n for NormalStyle)  ")
    mtype = MaTypes.RalphStyle

    if ans == 'r':
        mtype = MaTypes.RalphStyle
    elif ans == 'n':
        mtype = MaTypes.NormalStyle
    else:
        print("Bad moving average type input! Try Again")
        return getMaType()
    print("\n")

    return mtype

# prints all of the data and cumulative total columns, starting at a particular increment if given
def printCumulativeTotals(systems: Systems, startInc=None, offset=0):
    datapoints = systems.datapoints
    cols = [system.cumulativeTotal for system in systems.systems]
    lineString = ""
    if startInc is None:
        startInc = len(datapoints) - screenHeight()

    for i in range(startInc - 1, startInc + screenHeight()):
        if i < len(cols[0]):
            for col in cols:
                lineString += "{:>10}".format(int(col[i] * 100))

            increment = '{:>8}, '.format(i + 1 + offset)  # > means align text to the right
            date = str(datapoints[i].datetime) + ", "
            dataVal = '{:>10}, '.format(datapoints[i].price)

            print(increment + date + dataVal + lineString)
            lineString = ""

def printStats(systems: Systems, startIndex=0):
    endIndex = len(systems.datapoints) -1
    stats = [system.stats for system in systems.systems]
    headingWidth = 43
    splitter = "*" * screenWidth()
    print(splitter + "\n")

    # print the grant total for each stat in stats
    banner = str('GRAND TOTAL:').ljust(headingWidth)
    for stat in stats:
        value = stat.runningGt[endIndex] - stat.runningGt[startIndex]
        banner += str(format(value, '.2f')).rjust(10)  # data is adjusted prior to this to have pennies to the left of the decimal, move them back right by dividing by 100
    print(banner)

    banner = str('TRADE COUNT:').ljust(headingWidth)
    for stat in stats:
        value = stat.runningTradeCount[endIndex] - stat.runningTradeCount[startIndex]
        banner += str(value).rjust(10)
    print(banner)

    banner = str('WIN COUNT:').ljust(headingWidth)
    for stat in stats:
        value = stat.runningWinCount[endIndex] - stat.runningWinCount[startIndex]
        banner += str(value).rjust(10)
    print(banner)

    banner = str('LOSS COUNT:').ljust(headingWidth)
    for stat in stats:
        value = stat.runningLossCount[endIndex] - stat.runningLossCount[startIndex]
        banner += str(value).rjust(10)
    print(banner)

    banner = str('AVG WIN:').ljust(headingWidth)
    for stat in stats:
        total = stat.runningWinTotal[endIndex] - stat.runningWinTotal[startIndex]
        count = stat.runningWinCount[endIndex] - stat.runningWinCount[startIndex]
        value = total/count if count != 0 else 0
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)

    banner = str('AVG LOSS:').ljust(headingWidth)
    for stat in stats:
        total = stat.runningLossTotal[endIndex] - stat.runningLossTotal[startIndex]
        count = stat.runningLossCount[endIndex] - stat.runningLossCount[startIndex]
        value = total/count if count != 0 else 0
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)

    banner = str('MAX WIN:').ljust(headingWidth)
    for stat in stats:
        value = stat.runningMaxWin[endIndex] - stat.runningMaxWin[startIndex]
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)

    banner = str('MAX LOSS:').ljust(headingWidth)
    for stat in stats:
        value = stat.runningMaxLoss[endIndex] - stat.runningMaxLoss[startIndex]
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)

    banner = str('W/L RATIO:').ljust(headingWidth)
    for stat in stats:
        winCount = stat.runningWinCount[endIndex] - stat.runningWinCount[startIndex]
        lossCount = stat.runningLossCount[endIndex] - stat.runningLossCount[startIndex]
        banner += str('N/A' if lossCount == 0 else format(float(winCount) / float(lossCount), '.2f')).rjust(10)
    print(banner)

    banner = 'L/W RATIO:'.ljust(headingWidth)
    for stat in stats:
        winCount = stat.runningWinCount[endIndex] - stat.runningWinCount[startIndex]
        lossCount = stat.runningLossCount[endIndex] - stat.runningLossCount[startIndex]
        banner += str('N/A' if winCount == 0 else format(float(lossCount) / float(winCount), '.2f')).rjust(10)
    print(banner)

def clearTerminal():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def isValidDecimal(input):
    try:
        float(input)
    except ValueError:
        return False
    else:
        return True

def main():
    global maType
    maType = getMaType(settings.defaultMaType)  # gets and sets the global moving average type
    systems = getSystems(getDbConnection())
    currentLine = len(systems.datapoints) - screenHeight()
    printCumulativeTotals(systems, currentLine)
    printSystems(systems)
    printStats(systems)

    command = 0
    while command != 'q':
        command = input(
            "commands: 6=page, c=change company, g=grand_totals, q=quit, r=restart, t=time window, s=systems menu, chart=chart")
        if command == 'q':
            return
        elif command == 'c':
            clearTerminal()
            systems.setDbConnection(getDbConnection())
            currentLine = len(systems.datapoints) - screenHeight()
            printCumulativeTotals(systems, currentLine)
            printSystems(systems)
            printStats(systems)
        elif command == 'chart':
            whichSys = int(input("Which system do you want to chart? (e.g. 0, 1, 2, etc) "))
            charting.chartSystem(systems.systems[whichSys])
        elif command == '6':
            whichInc = input("What increment do you want to go to? (q to exit, e for end increment) ")
            if (whichInc == "e"):
                currentLine = len(systems.datapoints) - screenHeight()
                whichInc = len(systems.datapoints)
            else:
                currentLine = int(whichInc) - screenHeight()

            printCumulativeTotals(systems, currentLine)
            printSystems(systems)
            printStats(systems, int(whichInc) - 1)
        elif command == 'r':  # Restart
            clearTerminal()
            main()
        elif command == 's':
            enterSystemsMenu(systems)
            printCumulativeTotals(systems, currentLine)
            printSystems(systems)
            printStats(systems, len(systems.datapoints) - 1)

if __name__ == "__main__":
    try:
        clearTerminal()
        main()
    except Exception as e:
        print(f"Error: {e}")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        input("There was an Error. Press Enter to Exit...")