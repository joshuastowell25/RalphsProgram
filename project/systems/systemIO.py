from .. import definitions.SYSTEMS_PATH
import json

x = '{"name": "mySystem1", "maType": "r", "divisors": [2, 4, 6]}'

y = json.loads(x)

print(y["name"])
print(top_package)

def test():
    print("test works!")