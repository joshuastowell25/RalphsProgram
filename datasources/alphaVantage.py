from domain import Datapoint
from typing import List
import requests
from app_secrets import app_secrets
from datetime import datetime
#interval = '5min'
def getDatapoints(symbol, interval):
    datapoints: List[Datapoint] = []
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize=full&apikey={app_secrets.ALPHA_VANTAGE_API_KEY}"
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