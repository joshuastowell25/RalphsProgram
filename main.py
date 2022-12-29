#!/usr/bin/env python
import datetime
import os, sys, traceback
import time
import pandas
import systems as sys
import dataIO as dataIO
import calculation as calculation
import charting 
import shutil               #shell utils to get the terminal height
import settings             #the GOOD way to import from a file
#from settings import *     #The BAD way to import from a file
from constants import MaTypes
from systems import printSystems
from string import ascii_uppercase

#gets the number of lines in the terminal
def screenHeight():
    return shutil.get_terminal_size().lines

def screenWidth():
    return shutil.get_terminal_size().columns

#gets the users desired moving average type
def getMaType(ans = None): #ans defaults to None
    if ans is None:
        ans = input("What type of moving average? (r for RalphStyle, n for NormalStyle)  ")
    mtype = MaTypes.RalphStyle
    
    if ans == 'r':
        mtype = MaTypes.RalphStyle
    elif ans == 'n':
        mtype = MaTypes.NormalStyle
    else:
        print ("Bad moving average type input! Try Again")
        return getMaType()
    print ("\n")
       
    return mtype

#gets the indexes for which to run a versus system on
def getVsIndexes():
    in1 = input("What columns do you want to play against each other? Example: xy \n")
    in1 = in1.upper()
    parts = in1.split(" ")
    if len(parts) == 1:
        teamA = ord(in1[0])-65
        teamB = ord(in1[1])-65
    elif len(parts) == 2:
        teamA = ord(parts[0])-65 #65 is ascii A
        teamB = ord(parts[1])-65 #65 is ascii A
    elif len(parts) != 2:
        print ("BAD INPUT!\n")
        return getVsIndexes()
    return [teamA, teamB]

#gets the indexes to run a confirmation/agreement system on
def getConfirmationIndexes():
    in1 = input("What columns do you want to confirm each other? Example: xy \n")
    in1 = in1.upper()
    parts = in1.split(" ")
    if len(parts) == 1:
        teamA = ord(in1[0])-65
        teamB = ord(in1[1])-65
    elif len(parts) == 2:
        teamA = ord(parts[0])-65 #65 is ascii A
        teamB = ord(parts[1])-65 #65 is ascii A
    elif len(parts) != 2:
        print ("BAD INPUT!\n")
        return getConfirmationIndexes()
    return [teamA, teamB]

#prints all of the data and columns, starting at a particular increment if given
def printCols(data, dates, cols, startInc = None, offset=0):
    colString = ""
    if startInc is None:
        startInc = len(data) - screenHeight()

    for i in range(startInc - 1, startInc + screenHeight()):
        if i < len(cols[0]):
            for j in range(len(cols)):
                colString += "{:>10}".format(cols[j][i])

            increment = '{:>8}, '.format(i+1+offset) #> means align text to the right
            date = str(dates[i])+", "
            dataVal = '{:>10}, '.format(data[i])

            print(increment+date+dataVal+colString)
            colString = ""

#given the system columns and teamA,teamB of vsIndexes, calculates a vs column
def calcVsCol(syscols, vsIndexes):
    col = [0] * len(syscols[0])
    index1 = vsIndexes[0]
    index2 = vsIndexes[1]
    for i in range(len(syscols[0])):
        col[i] += syscols[index1][i]
        col[i] -= syscols[index2][i]
    return col

def calcConfCol(syscols, confIndexes):
    col = [0] * len(syscols[0])
    for i in range(len(syscols[0])):
        if syscols[confIndexes[0]][i] < 0 and syscols[confIndexes[1]][i] < 0:
            col[i] = -1
        elif syscols[confIndexes[0]][i] > 0 and syscols[confIndexes[1]][i] > 0:
            col[i] = 1
        else:
            col[i] = 0
    return col

positions = {
    'long': 1, 
    'short': -1,
    'flat': 0}

stat = {
    'gt': 0,
    'trades': 1,
    'winCount': 2,
    'lossCount': 3,
    'maxWin': 4,
    'maxLoss': 5,
    'runningGt': 6,
    'runningWinCount': 7,
    'runningLossCount': 8,
    'runningTies': 9,
    'runningTrades': 10,
    'runningMaxWin': 11,
    'runningMaxLoss': 12,
    'runningWinTotal': 13,
    'runningLossTotal': 14
}    

#minus Index is the index of the stats to NOT count in what gets printed
def printStats(stats, index, minusIndex = 0):
    headingWidth = 43
    width = screenWidth()
    splitter = "*"*screenWidth()
    print(splitter+"\n")
    banner = str("GRAND TOTAL:").ljust(headingWidth)
    for i in range(len(stats)):
        value = round(stats[i][stat['runningGt']][index] - stats[i][stat['runningGt']][minusIndex], 2)
        banner += str(value).rjust(10)  # data is adjusted prior to this to have pennies to the left of the decimal, move them back right by dividing by 100
    print(banner)
    
    banner = str("TRADE COUNT:").ljust(headingWidth)
    for i in range(len(stats)):
        value = stats[i][stat['runningTrades']][index] - stats[i][stat['runningTrades']][minusIndex]
        banner += str(value).rjust(10)
    print(banner)
    
    banner = str("WIN COUNT:").ljust(headingWidth)
    for i in range(len(stats)):
        value = stats[i][stat['runningWinCount']][index] - stats[i][stat['runningWinCount']][minusIndex]
        banner += str(value).rjust(10)
    print(banner)
    
    banner = str("LOSS COUNT:").ljust(headingWidth)
    for i in range(len(stats)):
        value = stats[i][stat['runningLossCount']][index] - stats[i][stat['runningLossCount']][minusIndex]
        banner += str(value).rjust(10)
    print(banner)

    banner = str("AVG WIN:").ljust(headingWidth)
    for i in range(len(stats)):
        total = stats[i][stat['runningWinTotal']][index] - stats[i][stat['runningWinTotal']][minusIndex]
        count = stats[i][stat['runningWinCount']][index] - stats[i][stat['runningWinCount']][minusIndex]
        value = total / count
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)

    banner = str("AVG LOSS:").ljust(headingWidth)
    for i in range(len(stats)):
        total = stats[i][stat['runningLossTotal']][index] - stats[i][stat['runningLossTotal']][minusIndex]
        count = stats[i][stat['runningLossCount']][index] - stats[i][stat['runningLossCount']][minusIndex]
        value = total / count
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)

    banner = str("MAX WIN:").ljust(headingWidth)
    for i in range(len(stats)):
        value = stats[i][stat['runningMaxWin']][index] - stats[i][stat['runningMaxWin']][minusIndex]
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)
    
    banner = str("MAX LOSS:").ljust(headingWidth)
    for i in range(len(stats)):
        value = stats[i][stat['runningMaxLoss']][index] - stats[i][stat['runningMaxLoss']][minusIndex]
        banner += str(format(value, '.2f')).rjust(10)
    print(banner)
	
    banner = str("W/L RATIO:").ljust(headingWidth)
    for i in range(len(stats)):
        winCount = stats[i][stat['runningWinCount']][index] - stats[i][stat['runningWinCount']][minusIndex]
        lossCount = stats[i][stat['runningLossCount']][index] - stats[i][stat['runningLossCount']][minusIndex]
        if(lossCount != 0):
            banner += str(format(float(winCount)/float(lossCount), '.2f')).rjust(10)
        else:
            banner += str("N/A").rjust(10)
    print(banner)
    
    banner = str("L/W RATIO:").ljust(headingWidth)
    for i in range(len(stats)):
        winCount = stats[i][stat['runningWinCount']][index] - stats[i][stat['runningWinCount']][minusIndex]
        lossCount = stats[i][stat['runningLossCount']][index] - stats[i][stat['runningLossCount']][minusIndex]
        if(winCount != 0):
            banner += str(format(float(lossCount)/float(winCount), '.2f')).rjust(10)
        else:
            banner += str("N/A").rjust(10)
    print(banner)
    
#calculates and returns a list of stats for every column given in syscols
def calcStats(data, syscols):
    start = time.time()
    result = []
    for i in range(len(syscols)):
        result.append(getColStats(data, syscols[i], data, data)) #for now just use market data as bid and ask price
    stop = time.time()
    diff = stop - start
    print("Calculated stats in " + "{:.2f}".format(diff) + " seconds")
    return result
    
#calculates and returns stats for a particular column
def getColStats(data, syscol, bid, ask):
    gt = 0
    runningGt=[]
    runningWinCount=[]
    runningLossCount=[]
    runningTradeCount=[]
    runningTieCount=[]
    runningMaxWin=[]
    runningMaxLoss=[]
    runningWinTotal=[]
    runningLossTotal=[]
    tradeCount = 0
    winCount = 0
    lossCount = 0
    tieCount = 0
    position = positions['flat']
    positionPrice = 0
    price = 0
    winloss = 0
    maxWin = 0
    maxLoss = 0
    for i in range(len(syscol)):
        price = data[i]
        bidPrice = bid[i]
        askPrice = ask[i]
        if(syscol[i] > 0): #the system is long
            if(position == positions['flat']):
                position = positions['long']
                positionPrice = askPrice #you're going long so you're buying from the ASK
            elif(position == positions['short']):
                #you've exited a short position and you're going long. Short selling aka 'Shorting' is selling a stock you down own by borrowing it from your broker.
                #So to exit a short position, in which you have sold a stock, you must now buy one back (at the asking price) to exit the position
                winloss = positionPrice - askPrice
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                position = positions['long']
                positionPrice = askPrice #you're going long so you're buying from the ASK
        elif(syscol[i] < 0): #The system is short
            if(position == positions['flat']):
                position = positions['short']
                positionPrice = bidPrice #Short selling aka 'Shorting' is selling a stock you down own by borrowing it from your broker. You can only sell NOW at the highest bid price.
            elif(position == positions['long']):
                #you've exited a long position to go short
                winloss = bidPrice - positionPrice #sell what you owned at the bidPrice
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                position = positions['short']
                positionPrice = bidPrice #Short selling aka 'Shorting' is selling a stock you down own by borrowing it from your broker. You can only sell NOW at the highest bid price.
        elif(syscol[i] == 0): #The system is FLAT (no position)
            if(position == positions['long']):
                #you've exited a long position to go flat
                winloss = bidPrice - positionPrice #sell what you owned at the bidPrice
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
            elif(position == positions['short']):
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
            position = positions['flat']
            positionPrice = price #it's irrelevant what you make the positionPrice in a flat position. We'll just set it to the market price here.
        if(winloss > maxWin):
            maxWin = winloss
        elif(winloss < maxLoss):
            maxLoss = winloss

        runningGt.append(gt)
        runningTradeCount.append(tradeCount)
        runningWinCount.append(winCount)
        runningLossCount.append(lossCount)
        runningTieCount.append(tieCount)
        runningMaxWin.append(maxWin)
        runningMaxLoss.append(maxLoss)

        if(i > 0 and winloss < 0):
            runningWinTotal.append(runningWinTotal[i - 1])
            runningLossTotal.append(winloss + runningLossTotal[i - 1])
        elif(i > 0 and winloss > 0):
            runningWinTotal.append(winloss + runningWinTotal[i - 1])
            runningLossTotal.append(runningLossTotal[i - 1])
        elif(i == 0 and winloss < 0):
            runningWinTotal.append(0)
            runningLossTotal.append(winloss)
        elif(i == 0 and winloss > 0):
            runningWinTotal.append(winloss)
            runningLossTotal.append(0)
        elif(i > 0 and winloss == 0):
            runningWinTotal.append(runningWinTotal[i-1])
            runningLossTotal.append(runningLossTotal[i-1])
        elif(i == 0 and winloss == 0):
            runningLossTotal.append(0)
            runningWinTotal.append(0)
        winloss = 0

    return [gt, tradeCount, winCount, lossCount, maxWin, maxLoss, runningGt, runningWinCount, runningLossCount, runningTieCount, runningTradeCount, runningMaxWin, runningMaxLoss, runningWinTotal, runningLossTotal] #internal representation of pennies is left of the decimal point

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
    maType = getMaType(settings.defaultMaType) #gets and sets the global moving average type
    result = dataIO.getDataFromDatabase()
    dbConnection = result['dbConnection']
    data = result['data']
    dates = result['dates']

    systems = sys.getSystems()
    syscols = calculation.calcSysCols(systems, data, dbConnection)

    count = 0
    doVersus = settings.doVersusDefault
    versusSystems = []
    while doVersus == 'y' or doVersus != 'n':
        if doVersus != 'y' and doVersus != 'n':
            print ("BAD INPUT!")
        a_another = "another" if count>0 else "a"
        doVersus = input("Do you want to create "+a_another+" versus column? (y or n) \n")
        if doVersus == 'y':
            indexes = getVsIndexes()            #if they choose ab, returns list of those indices: [0,1]
            versusSystems.append(indexes)
            vscol = calcVsCol(syscols, indexes)
            print ("\'"+ascii_uppercase[indexes[0]]+" confirming "+ascii_uppercase[indexes[1]]+"\' was placed in column "+ascii_uppercase[len(syscols)]+"\n\n")
            syscols.append(vscol)
            count += 1
            
    count = 0
    doConfirmation = settings.doConfirmationDefault
    confirmationSystems = []
    while doConfirmation == 'y' or doConfirmation != 'n':
        if doConfirmation != 'y' and doConfirmation != 'n':
            print ("BAD INPUT!")
        a_another = "another" if count>0 else "a"    
        doConfirmation = input("\nDo you want to create "+a_another+" confirmation column? (y or n) \n")
        if doConfirmation == 'y':
            indexes = getConfirmationIndexes()      #if they choose ab, returns list of those indices: [0,1]
            confirmationSystems.append(indexes)
            confcol = calcConfCol(syscols, indexes)
            print ("\'"+ascii_uppercase[indexes[0]]+" confirming "+ascii_uppercase[indexes[1]]+"\' was placed in column "+ascii_uppercase[len(syscols)]+"\n\n")
            syscols.append(confcol)   
            count += 1

    if(settings.immediateResults == False):      
        input("\nPress Enter to view columns...\n")
    currentLine = len(data)-screenHeight()
    printCols(data, dates, syscols, currentLine)
    stats = calcStats(data, syscols)
    printSystems(systems, versusSystems, confirmationSystems)
    printStats(stats, len(data) - 1)
    
    command = 0
    while command != 'q':
        command = input("commands: 6=page, c=change company, g=grand_totals, q=quit, r=restart, t=time window, s=systems menu, chart=chart")
        if command == 'q':
            return
        elif command == 'c':
            clearTerminal()
            dbConnection.close()
            result = dataIO.getDataFromDatabase()
            dbConnection = result['dbConnection']
            data = result['data']
            dates = result['dates']

            clearTerminal()
            syscols = calculation.calcSysCols(systems, data, dbConnection)
            for indexes in versusSystems:
                vscol = calcVsCol(syscols, indexes)
                syscols.append(vscol)
            for indexes in confirmationSystems:
                confcol = calcConfCol(syscols, indexes)
                syscols.append(confcol)
            printCols(data, dates, syscols, currentLine)
            stats = calcStats(data, syscols)
            printSystems(systems, versusSystems, confirmationSystems)
            printStats(stats, len(data) - 1)
        elif command == 'chart':
            whichSys = 1
            if(len(stats) > 1):
                whichSys = int(input("Which system do you want to chart? (e.g. 1, 2, 5, etc) "))
            runningGt = stats[whichSys-1][stat['runningGt']]
            charting.chartData(runningGt, dates)
        elif command == '6':
            whichInc = input("What increment do you want to go to? (q to exit, e for end increment) ")
            if(whichInc == "e"):
                currentLine = len(data) - screenHeight()
                whichInc = len(data)
            else:
                currentLine = int(whichInc) - screenHeight()

            printCols(data, dates, syscols, currentLine)
            printSystems(systems, versusSystems, confirmationSystems)
            printStats(stats, int(whichInc) - 1)
        elif command == 'r': #Restart
            clearTerminal()
            main()
        elif command == 's':
            sys.enterSystemsMenu(systems)
            #now they've returned
            printCols(data, dates, syscols, currentLine)
            printSystems(systems, versusSystems, confirmationSystems)
            printStats(stats, len(data) - 1)
        elif command == 't':
            earliestDate = dates[0]
            latestDate = dates[len(dates) - 1]
            print("You can choose time windows between " + \
                  str(earliestDate.strftime('%m/%d/%Y %H:%M:%S')) + " and " + \
                  str(latestDate.strftime('%m/%d/%Y %H:%M:%S')))
            startDate = None
            endDate = None

            while (startDate is None):
                try:
                    timeA = input("Enter the start date for your time window in format MM/DD/YYYY\n")
                    if(len(timeA) < 11):
                        timeA = timeA + " 00:00:00"
                    startDate = datetime.datetime.strptime(timeA, '%m/%d/%Y %H:%M:%S')
                    # make sure startDate is on or after the 0th date
                    if (not (startDate >= earliestDate)):
                        print("BAD DATE: You can only choose time windows between " + str(earliestDate) + " and " + str(
                            latestDate) + "\n")
                        startDate = None
                except Exception as e:
                    print(f"BAD DATE: {e}")
                    startDate = None

            while (endDate is None):
                try:
                    timeB = input("Enter the end date for your time window in format MM/DD/YYYY\n")
                    if (len(timeB) < 11):
                        timeB = timeB + " 00:00:00"
                    endDate = datetime.datetime.strptime(timeB, '%m/%d/%Y %H:%M:%S')
                    # make sure endDate is on or before the last date
                    if (not (endDate <= latestDate)):
                        print("BAD DATE: You can only choose time windows between " + str(earliestDate) + " and " + str(
                            latestDate) + "\n")
                        endDate = None
                    if (not (endDate > startDate)):
                        print("BAD DATE: The end date must be AFTER the start date.\n")
                        endDate = None
                except Exception as e:
                    print(f"BAD DATE: {e}")
                    endDate = None

            dates_df = pandas.to_datetime(dates).to_frame()
            dates_df = dates_df.truncate(before=startDate, after=endDate)
            firstDate = dates_df[0].iloc[0]
            lastDate = dates_df[0].iloc[len(dates_df.index) - 1]
            startIndex = dates.index(firstDate)
            endIndex = dates.index(lastDate)
            syscolsTrimmed = [subcol[startIndex:endIndex+1] for subcol in syscols]
            printCols(data[startIndex:endIndex+1], dates[startIndex:endIndex+1], syscolsTrimmed, currentLine, startIndex)
            stats = calcStats(data, syscols)
            printSystems(systems, versusSystems, confirmationSystems)
            printStats(stats, endIndex+1, startIndex)
        elif command == 'g': #Grand Totals
            printCols(data, dates, syscols, currentLine)
            stats = calcStats(data, syscols)
            printSystems(systems, versusSystems, confirmationSystems)
            printStats(stats, len(data) - 1)

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