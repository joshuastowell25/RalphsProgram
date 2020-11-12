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

result = calculateColumnRalphsMA(4, [0,1,2,3,4,5,6,7,8,9])
print(result)