def calculateColumnRalphsMA(num, data, numcol):
    part = num // 2  # integer division is done with //

    startIndex = 0
    if((len(numcol) - num) > 0):
        startIndex = numcol.size - num #10-4 = 6

    #Initial calculation of frontsum and backsum
    backsum = 0
    frontsum = 0
    for i in range(startIndex, part): #0,1,2,3  -> 6,7,8,9,,,, num = 4, length = 10. length - num = 6
        backsum += data[i]  # index 0 to 1 if num is 4
        frontsum += data[i + part]  # index 2 to 3 if num is 4

    #Extend the size of the column to match the size of the data
    originalLength = len(numcol) #10
    extendSize = len(data) - len(numcol)
    numcol.extend([0] * extendSize)

    #Save that first calculation
    numcol[originalLength] = frontsum - backsum

    #Using memoization:
    for i in range(originalLength + 1, len(data)):  # index 20 to 800
        backNum = data[i - num]  # remove index 0
        backsum -= backNum
        transferNum = data[i - part]  # 20 - 10 = index 10
        backsum += transferNum  # add index 10
        frontsum -= transferNum  # remove index 10
        frontNum = data[i]
        frontsum += frontNum  # add index 20
        numcol[i] = frontsum - backsum

    return numcol

result = calculateColumnRalphsMA(4, [0,1,2,3,4,5,6,7,8,9], [])
print(result)