from typing import List
from data_connectors.connectors.ConnectorInterface import DataConnector, DataSourceType #From the file import the interface
import domain
from dataIO import getDataFromFile
import os
import constants


class OfflineFlatFileDataSource(DataConnector):
    dataSourceType: DataSourceType = DataSourceType.OFFLINE

    def __init__(self):
        pass

    def isAvailable(self) -> bool:
        return True

    def getData(self) -> List[domain.Datapoint]:
        companyChoices = os.listdir(constants.DATA_PATH)
        print(f"data file choices are: {companyChoices}")
        companyName = input("What data file do you want to use? \n")
        datapoints = getDataFromFile(companyName+".csv")
        print(f"Loaded {len(datapoints)} datapoints from {companyName}.csv")
        return datapoints
