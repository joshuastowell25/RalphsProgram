from definitions import MaTypes
maType = MaTypes.RalphStyle # the default desired moving average type


# returns a collection of columns for each system
def calcSysCols(systems, data):
    cols = []
    for i in range(len(systems)):
        cols.append(calcSysCol(systems[i], data))
    return cols


# given a list of number to comprise a system, calculates that systems column
def calcSysCol(sys, data):
    global maType
    col = [0] * len(data)
    for i in range(len(sys)):
        if maType == MaTypes.RalphStyle:
            numcol = calcNumColRalphsMA(sys[i], data)
        elif maType == MaTypes.NormalStyle:
            numcol = calculateNumColNormalMA(sys[i], data)
        for j in range(len(numcol)):
            col[j] += numcol[j]
    return col


# given a single number calculates the result of that number on the data
def calcNumColRalphsMA(num, data):
    part = num // 2  # integer division is done with //
    col = [0] * len(data)

    backsum = 0
    frontsum = 0
    transferNum = 0
    backnum = 0
    frontnum = 0
    for i in range(part):
        backsum += data[i]  # index 0 to 9 if num is 20
        frontsum += data[i + part]  # index 10 to 19 if num is 20

    col[num - 1] = frontsum - backsum

    # done using memoization:
    for i in range(num, len(data)):  # index 20 to 800
        backnum = data[i - num]  # remove index 0
        backsum -= backnum
        transferNum = data[i - part]  # 20 - 10 = index 10
        backsum += transferNum  # add index 10
        frontsum -= transferNum  # remove index 10
        frontnum = data[i]
        frontsum += frontnum  # add index 20
        col[i] = frontsum - backsum
    return col


# given a single moving average number calculates the result of that number on the data
def calculateNumColNormalMA(num, data):
    col = [0] * len(data)
    sum = 0
    backnum = 0
    frontnum = 0

    for i in range(num):
        sum += data[i]  # 0 through 19 if the number is 20

    for i in range(num, len(data)):  # 20 through the rest of the data indices
        backnum = data[i - num]  # remove index 0
        sum -= backnum

        frontnum = data[i]
        sum += frontnum  # add index 20
        col[i] = data[i] - (sum / num)  # this ma vs todays close
        # col[i] = (sum/num)            #because regular moving average

    return col