from domain import Datapoint
from typing import List
import requests
from app_secrets import app_secrets
from datetime import datetime
#interval = one of: '1min','5min', '15min','30min','60min'
#month = '2009-01'
def getDatapoints(symbol, interval='1min', month = None):
    datapoints: List[Datapoint] = []
    monthQueryParam = f"&month={month}" if month else ""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY{monthQueryParam}&symbol={symbol}&interval={interval}&outputsize=full&apikey={app_secrets.ALPHA_VANTAGE_API_KEY}"
    r = requests.get(url)
    data = r.json()

    data_key = list(data.keys())[1]
    data_value = data.get(data_key)
    date_format = '%Y-%m-%d %H:%M:%S'

    for timestamp_key in reversed(data_value):
        dt = datetime.strptime(timestamp_key, date_format) #'2023-08-18 19:55:00'
        price = float(data_value[timestamp_key]['4. close'])
        datapoints.append(Datapoint(dt, price))

    return datapoints

#gets all the 1 minute data that alpha vantage has for the asset
#free tier is 5reqs/min and max 100 reqs/day
#paid tier has many levels: https://www.alphavantage.co/premium/
#highest tier is 1200 reqs/min which would mean 10 years worth of 1min data can be requested per minute
#lowest tier is 30reqs/min aka 1 req per every 2 seconds
def getAllDatapoints(symbol, maxReqsPerMin = 30):
    months = list(range(1,13))
    datapoints: List[Datapoint] = []
    year = 2000
    month = 1

    datapoints.extend(getDatapoints(symbol, '1min', month=f"{year}-{month:02d}"))

    return datapoints

def saveDatapointsToFileAsJson():
    pass

def get_data():
    symbol = input("What is the symbol of the data you want to use?\n")
    valid_choices = ['1min','5min', '15min','30min','60min']

    while True:
        user_input = input(f"Choose one of {valid_choices}: ")

        if user_input in valid_choices:
            break
        else:
            print("Invalid choice. Please select from the valid options.\n")
    interval = user_input
    return getDatapoints(symbol, interval)