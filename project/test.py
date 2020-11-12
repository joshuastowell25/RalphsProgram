def calculateColumnRalphsMA(num, data, result):
    part = num // 2  # integer division is done with //

    originalColLength = len(result)
    offset = max(num, originalColLength)
    print("offset: "+str(offset))

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
        backsum += data[i + originalColLength - num]  #0+1=1
        frontsum += data[i + part + originalColLength - num]  #2+3=5
    print("frontsum:"+str(frontsum)+" backsum: "+str(backsum))

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

result = calculateColumnRalphsMA(4, [1,2,3,4,5,6,7,8,9,10,11,12], []) #->[0, 0, 0, 0, 12, 6, -12, -6]
print(result)