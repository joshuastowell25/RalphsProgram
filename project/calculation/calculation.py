from definitions import MaTypes
maType = MaTypes.RalphStyle # the default desired moving average type


# returns a collection of columns for each system
def calcSysCols(systems, data):
    cols = []
    for i in range(len(systems)):
        cols.append(calcSysCol(systems[i], data))
    return cols


# given a list of numbers to comprise a system, calculates that system's column
def calcSysCol(sys, data):
    global maType
    col = [0] * len(data)
    for i in range(len(sys)):
        if maType == MaTypes.RalphStyle:
            numcol = calculateColumnRalphsMA(sys[i], data)
        elif maType == MaTypes.NormalStyle:
            numcol = calculateColumnNormalMA(sys[i], data)
        for j in range(len(numcol)):
            col[j] += numcol[j]
    return col


# given a single divisor number calculates the result of that number on the data
# the 'result' is a single array of numbers, aka a column, that divisor's column.
def calculateColumnRalphsMA(num, data):
    part = num // 2  # integer division is done with //
    col = [0] * len(data)

    backsum = 0
    frontsum = 0

    # Calculate the first frontsum and backsum
    for i in range(part):
        backsum += data[i]  # index 0 to 9 if num is 20
        frontsum += data[i + part]  # index 10 to 19 if num is 20

    col[num - 1] = frontsum - backsum

    # Using memoization:
    for i in range(num, len(data)):  # index 20 to 800
        backNum = data[i - num]  # remove index 0
        backsum -= backNum
        transferNum = data[i - part]  # 20 - 10 = index 10
        backsum += transferNum  # add index 10
        frontsum -= transferNum  # remove index 10
        frontNum = data[i]
        frontsum += frontNum  # add index 20
        col[i] = frontsum - backsum
    return col

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

# Saves a computed column to the database under a particular id
# ids can relate to whole systems e.g. 'sys239842'
# or divisors 'div20'
# the length of the column always matches the length of the data at the time of computation so there's no need to save how long the data was
# We will have to save the data file name in the id though. e.g. sys239842_sp1985, div20_sp1985
def saveColumnToDB(col, database, colName): #e.g. (col, "sp1985", "_2")
    pass