from typing import List
import abc
import domain
from constants import enum

DataSourceType = enum(OFFLINE="OFFLINE", MARIADB="MARIADB", BIGQUERY="BIGQUERY")

class DataSource(): #metaclass=abc.ABCMeta): #Interface
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

    def __str__(self):
        return str(self.dataSourceType)
