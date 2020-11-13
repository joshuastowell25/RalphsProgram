import dataIO as dataIO
from calculation import calculateColumnRalphsMA

def testCalculate(num, data, result):
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
        print("adding to backsum, index: "+str(i + offset - num))
        print("adding to frontsum, index: "+str(i +part+ offset - num))
        backsum += data[i + offset - num]  #0+1=1
        frontsum += data[i + part + offset - num]  #2+3=5
    print("frontsum:"+str(frontsum)+" backsum: "+str(backsum)) # backsum: 32993, frontsum: 32791. f-b = -202

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

data, filename = dataIO.getData()
print(data[:10])
result1 = testCalculate(4, data[:100], []) #->[0, 0, 0, 0, 12, 6, -12, -6]
print(result1)

result2 = calculateColumnRalphsMA(4, data[:100])
print(result2)