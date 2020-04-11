from .. import definitions
import json

x = '{"name": "mySystem1", "maType": "r", "divisors": [2, 4, 6]}'

y = json.loads(x)

print(y["name"])

def getSystem(sysName):
    with open('data.txt', 'r') as file:
        data = file.read().replace('\n', '')