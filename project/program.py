#!/usr/bin/env python
import os, sys, traceback
import time

import systems as sys
import dataIO as dataIO
import calculation as calculation
import database
import config
import charting 
import shutil               #shell utils to get the terminal height
import settings             #the GOOD way to import from a file
#from settings import *     #The BAD way to import from a file
from definitions import MaTypes

#gets the number of lines in the terminal
def screenHeight():
    return shutil.get_terminal_size().lines

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

#prints a column
def printCol(col):
    for i in range(len(col)):
        print ("inc "+str(i+1)+": "+str(col[i]))

#prints all of the data and columns, starting at a particular increment if given
def printCols(data, cols, startInc = None):
    datastring = ""
    if startInc is None:
        for i in range(len(cols[0])):
            for j in range(len(cols)):
                datastring += "{0:10d}".format(cols[j][i])
            
            print ("inc"+str(i+1)+", price="+str(data[i]/100).ljust(10)+datastring)
            datastring = ""
    else:
        for i in range(startInc - 1, startInc + screenHeight()):
            if i < len(cols[0]):
                for j in range(len(cols)):
                    datastring += "{0:10d}".format(cols[j][i])
                print ("inc"+str(i+1)+", price="+str(data[i]/100).ljust(10)+datastring)
                datastring = ""

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
    'runningWins': 7,
    'runningLosses': 8,
    'runningTies': 9,
    'runningTrades': 10,
    'runningMaxWin': 11,
    'runningMaxLoss': 12
}    
    
def printStats(stats, index):
    print("\n")
    banner = str("GRAND TOTAL:").ljust(26)
    for i in range(len(stats)):
        if (config.runningTotalsFlag):
            banner += str(stats[i][stat['runningGt']][index] / 100).rjust(10)  # data is adjusted prior to this to have pennies to the left of the decimal, move them back right by dividing by 100
        else:
            banner += str(stats[i][stat['gt']] / 100).rjust(10)  # data is adjusted prior to this to have pennies to the left of the decimal, move them back right by dividing by 100
    print(banner)
    
    banner = str("TRADE COUNT:").ljust(26)
    for i in range(len(stats)):
        if (config.runningTotalsFlag):
            banner += str(stats[i][stat['runningTrades']][index]).rjust(10)
        else:
            banner += str(stats[i][stat['trades']]).rjust(10)
    print(banner)
    
    banner = str("WIN COUNT:").ljust(26)
    for i in range(len(stats)):
        if (config.runningTotalsFlag):
            banner += str(stats[i][stat['runningWins']][index]).rjust(10)
        else:
            banner += str(stats[i][stat['winCount']]).rjust(10)
    print(banner)
    
    banner = str("LOSS COUNT:").ljust(26)
    for i in range(len(stats)):
        if(config.runningTotalsFlag):
            banner += str(stats[i][stat['runningLosses']][index]).rjust(10)
        else:
            banner += str(stats[i][stat['lossCount']]).rjust(10)
    print(banner)

    banner = str("MAX WIN:").ljust(26)
    for i in range(len(stats)):
        if(config.runningTotalsFlag):
            banner += str(stats[i][stat['runningMaxWin']][index]).rjust(10)
        else:
            banner += str(stats[i][stat['maxWin']]).rjust(10)
    print(banner)
    
    banner = str("MAX LOSS:").ljust(26)
    for i in range(len(stats)):
        if (config.runningTotalsFlag):
            banner += str(stats[i][stat['runningMaxLoss']][index]).rjust(10)
        else:
            banner += str(stats[i][stat['maxLoss']]).rjust(10)
    print(banner)    
	
    banner = str("W/L RATIO:").ljust(26)
    for i in range(len(stats)):
        if(config.runningTotalsFlag):
            winCount = stats[i][stat['runningWins']][index]
            lossCount = stats[i][stat['runningLosses']][index]
        else:
            winCount = stats[i][stat['winCount']]
            lossCount = stats[i][stat['lossCount']]
        banner += str(format(float(winCount)/float(lossCount), '.2f')).rjust(10)
    print(banner)
    
    banner = str("L/W RATIO:").ljust(26)
    for i in range(len(stats)):
        if (config.runningTotalsFlag):
            winCount = stats[i][stat['runningWins']][index]
            lossCount = stats[i][stat['runningLosses']][index]
        else:
            winCount = stats[i][stat['winCount']]
            lossCount = stats[i][stat['lossCount']]
        banner += str(format(float(lossCount)/float(winCount), '.2f')).rjust(10)
    print(banner)
    
#calculates and returns a list of stats for every column given in syscols
def calcStats(data, syscols):
    start = time.time()
    result = []
    for i in range(len(syscols)):
        result.append(getColStats(data, syscols[i]))
    stop = time.time()
    diff = stop - start
    print("Calculated results in " + "{:.2f}".format(diff) + " seconds")
    return result
    
#calculates and returns stats for a particular column
def getColStats(data, syscol):
    gt = 0
    runningGt=[]
    runningWinCount=[]
    runningLossCount=[]
    runningTradeCount=[]
    runningTieCount=[]
    runningMaxWin=[]
    runningMaxLoss=[]
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
        if(syscol[i] > 0):
            if(position == positions['flat']):
                position = positions['long']
                positionPrice = price
            elif(position == positions['short']):
                #you've exited a short position
                winloss = positionPrice - price
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                position = positions['long']
                positionPrice = price
        elif(syscol[i] < 0):
            if(position == positions['flat']):
                position = positions['short']
                positionPrice = price
            elif(position == positions['long']):
                #you've exited a long position
                winloss = price - positionPrice
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
                position = positions['short']
                positionPrice = price
        elif(syscol[i] == 0):
            if(position == positions['long']):
                #you've exited a long position
                winloss = price - positionPrice
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
            elif(position == positions['short']):
                #you've exited a short position
                winloss = positionPrice - price
                if winloss == 0:
                    tieCount += 1
                elif winloss < 0:
                    lossCount += 1
                elif winloss > 0:
                    winCount += 1
                gt += winloss
                tradeCount += 1
            position = positions['flat']
            positionPrice = price
        if(winloss > maxWin):
            maxWin = winloss
        elif(winloss < maxLoss):
            maxLoss = winloss
        if(config.runningTotalsFlag):
            runningGt.append(gt)
            runningTradeCount.append(tradeCount)
            runningWinCount.append(winCount)
            runningLossCount.append(lossCount)
            runningTieCount.append(tieCount)
            runningMaxWin.append(maxWin/100)
            runningMaxLoss.append(maxLoss/100)

    return [gt, tradeCount, winCount, lossCount, maxWin/100, maxLoss/100, runningGt, runningWinCount, runningLossCount, runningTieCount, runningTradeCount, runningMaxWin, runningMaxLoss] #internal representation of pennies is left of the decimal point

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
            print ("\'"+str(chr(indexes[0]+65)).lower()+" played against "+str(chr(indexes[1]+65)).lower()+"\' was placed in column "+str(chr(len(syscols)+65)).lower()+"\n\n")
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
            print ("\'"+str(chr(indexes[0]+65)).lower()+" confirming "+str(chr(indexes[1]+65)).lower()+"\' was placed in column "+str(chr(len(syscols)+65)).lower()+"\n\n")
            syscols.append(confcol)   
            count += 1

    if(settings.immediateResults == False):      
        input("\nPress Enter to view columns...\n")
    currentLine = len(data)-screenHeight()
    printCols(data, syscols, currentLine)
    stats = calcStats(data, syscols)
    printStats(stats, len(data) - 1)
    
    command = 0
    while command != 'q':
        command = input("commands: 6=page, c=change company, g=grand_totals, q=quit, r=restart, s=systems menu, chart=chart")
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
            printCols(data, syscols, currentLine)
            stats = calcStats(data, syscols)
            printStats(stats, len(data) - 1)
        elif command == 'chart':
            whichSys = int(input("Which system do you want to chart? (e.g. 1, 2, 5, etc) "))
            stats = calcStats(data, syscols)
            runningGt = stats[whichSys-1][stat['runningGt']]
            charting.chartData(runningGt, dates)
        elif command == '6':
            whichInc = input("What increment do you want to go to? (q to exit, e for end increment) ")
            if(whichInc == "e"):
                currentLine = len(data) - screenHeight()
                whichInc = len(data)
            else:
                currentLine = int(whichInc) - screenHeight()

            printCols(data, syscols, currentLine)
            printStats(stats, int(whichInc) - 1)
        elif command == 'r': #Restart
            clearTerminal()
            main()
        elif command == 's':
            sys.enterSystemsMenu(systems)
            #now they've returned
            printCols(data, syscols, currentLine)
            printStats(stats, len(data) - 1)
        elif command == 'g': #Grand Totals
            printCols(data, syscols, currentLine)
            stats = calcStats(data, syscols)
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