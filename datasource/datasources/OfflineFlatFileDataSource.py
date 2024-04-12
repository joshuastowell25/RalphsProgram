from typing import List
import DataSource
import domain
from dataIO import getDataFromFile
import os
import constants


class OfflineFlatFileDataSource(DataSource):
    dataSourceType: DataSource.DataSourceType = DataSource.DataSourceType.OFFLINE

    def __init__(self):
        pass

    def isAvailable(self) -> bool:
        return True

    def getData(self) -> List[domain.Datapoint]:
        companyChoices = os.listdir(constants.DATA_PATH)
        print(f"data file choices are: {companyChoices}")
        companyName = input("What data file do you want to use? \n")
        return getDataFromFile(companyName+".csv")

    def dataSourceType(self):
        return self.dataSourceType
