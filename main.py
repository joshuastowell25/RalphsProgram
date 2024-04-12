#!/usr/bin/env python
import os, sys, traceback
import shutil
import terminal
from domain import Systems, Stat, Datapoint
from systems import getSystems, enterSystemsMenu
from datasource import alphaVantage, datasource_utils
from datasource.datasources import DataSource


# gets the number of lines in the terminal
def screenHeight():
    return shutil.get_terminal_size().lines


def screenWidth():
    return shutil.get_terminal_size().columns


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

def printStats(systems: Systems):
    Stat.printStatsHeading()
    for system in systems.systems:
        system.stats.print(system.getDivisorString(), system.divisorBalance)

def isValidDecimal(input):
    try:
        float(input)
    except ValueError:
        return False
    else:
        return True

def main():
    datasource = datasource_utils.getDataSource()
    #datapoints: list[Datapoint] = alphaVantage.get_data()
    datapoints = datasource.getData()
    systems: Systems = getSystems()
    systems.setDatapoints(datapoints)
    currentLine = len(systems.datapoints) - screenHeight()
    printCumulativeTotals(systems, currentLine)
    printStats(systems)

    command = 0
    while command != 'q':
        command = input(
            "commands: 6=page, c=change company, g=grand_totals, q=quit, r=restart, t=time window, s=systems menu, chart=chart")
        if command == 'q':
            return
        elif command == 'c':
            terminal.clearTerminal()
            datapoints: list[Datapoint] = alphaVantage.get_data()
            systems.setDatapoints(datapoints)
            currentLine = len(systems.datapoints) - screenHeight()
            printCumulativeTotals(systems, currentLine)
            printStats(systems)
        elif command == 'chart':
            import charting
            whichSys = int(input("Which system do you want to chart? (e.g. 1, 2, 3, etc) "))
            charting.chartSystem(systems.systems[whichSys-1])
        elif command == '6':
            whichInc = input("What increment do you want to go to? (q to exit, e for end increment) ")
            if (whichInc == "e"):
                currentLine = len(systems.datapoints) - screenHeight()
                whichInc = len(systems.datapoints)
            else:
                currentLine = int(whichInc) - screenHeight()

            printCumulativeTotals(systems, currentLine)
            printStats(systems)
        elif command == 'r':  # Restart
            systems.clearSystems()
            terminal.clearTerminal()
            main()
        elif command == 's':
            enterSystemsMenu(systems)
            printCumulativeTotals(systems, currentLine)
            printStats(systems)

if __name__ == "__main__":
    try:
        terminal.clearTerminal()
        main()
    except Exception as e:
        print(f"Error: {e}")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        input("There was an Error. Press Enter to Exit...")