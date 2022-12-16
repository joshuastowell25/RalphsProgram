from constants import MaTypes
from database import *
maType = MaTypes.RalphStyle # the default desired moving average type


# returns a collection of columns for each system
# systems: a 2d array of systems [[2,4,6,8],[10,12,14],[16,18,20],[22,24,26]]
# data: The data to calculate the sys cols on
# dbConnection: the connection to the database, given as an argument to allow re-use and avoid disconnecting and reconnecting repeatedly.
def calcSysCols(systems, data, dbConnection):
    cols = []
    for i in range(len(systems)):
        cols.append(calcSysCol(systems[i], data, dbConnection))
    return cols


# given a list of numbers to comprise a system, calculates that system's column
def calcSysCol(sys, data, dbConnection):
    global maType
    import time

    col = [0] * len(data)
    for i in range(len(sys)):
        startMillis = int(round(time.time() * 1000))
        adtl = ""
        if maType == MaTypes.RalphStyle:
            numcol = []
            if(dbConnection is not None):
                numcol = database.loadColumn(dbConnection, "_"+str(sys[i])) #load the calculated column
            if(len(numcol)==len(data)):
                adtl="Via database load. "
            if(len(numcol) < len(data)):
                numcol = calculateColumnRalphsMA(sys[i], data, numcol) #update the calculation
            if(dbConnection is not None):
                database.saveColumn(dbConnection, numcol, "_"+str(sys[i])) #save the updated calculation into the database
        elif maType == MaTypes.NormalStyle:
            numcol = calculateColumnNormalMA(sys[i], data)
        endMillis = int(round(time.time() * 1000))
        print("calculated number: "+str(sys[i])+" in "+str(endMillis - startMillis)+" milliseconds. "+adtl)

        for j in range(len(numcol)):
            col[j] += numcol[j]
    return col


# given a single divisor number calculates the result of that number on the data
# the 'result' is a single array of numbers, aka a column, that divisor's column.
def calculateColumnRalphsMA(num, data, result):
    part = num // 2  # integer division is done with //

    originalColLength = len(result)
    offset = max(num, originalColLength)

    if (result is None):
        result = [0] * len(data)

    #extend the col size
    if(len(result) < len(data)):
        extension = [0] * (len(data) - len(result))
        result = result + extension

    backsum = 0
    frontsum = 0

    # Calculate the first frontsum and backsum
    for i in range(part): #0,1,
        backsum += data[i + offset - num]  #0+1=1
        frontsum += data[i + part + offset - num]  #2+3=5

    #set the data point for that frontsum and backsum calculation
    result[offset - 1] = frontsum - backsum #result[3] = 5-1 = 4

    #calculate the ith index
    for i in range(offset, len(data)):
        backNum = data[i - num]
        backsum -= backNum
        #transferNum goes from the frontsum to the backsum
        transferNum = data[i - part]
        backsum += transferNum
        frontsum -= transferNum
        frontNum = data[i]
        frontsum += frontNum
        result[i] = frontsum - backsum
    return result

# given a single moving average number calculates the result of that number on the data
def calculateColumnNormalMA(num, data):
    col = [0] * len(data)
    sum = 0

    for i in range(num):
        sum += data[i]  # 0 through 19 if the number is 20

    for i in range(num, len(data)):  # 20 through the rest of the data indices
        backNum = data[i - num]  # remove index 0
        sum -= backNum

        frontNum = data[i]
        sum += frontNum  # add index 20
        col[i] = data[i] - (sum / num)  # this ma vs todays close
        # col[i] = (sum/num)            # because regular moving average

    return col