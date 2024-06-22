from typing import List
import abc
import domain
from utils.data_types import enum
from domain.Datapoint import Datapoint #from the file import the class

DataSourceType = enum(OFFLINE="OFFLINE", MARIADB="MARIADB", BIGQUERY="BIGQUERY")

class DataConnector():
    dataSourceType: DataSourceType

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def isAvailable(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def getData(self) -> List[domain.Datapoint]:
        raise NotImplementedError

    @property
    def dataSourceType(self):
        return self.dataSourceType

    @abc.abstractmethod
    def writeDatapoint(self, datapoint: Datapoint):
        raise NotImplementedError

    def __str__(self):
        return str(self.dataSourceType)
