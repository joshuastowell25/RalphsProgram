from typing import List
import abc
import domain
from constants import enum

DataSourceType = enum(OFFLINE="OFFLINE", MARIADB="MARIADB", BIGQUERY="BIGQUERY")

class DataSource(metaclass=abc.ABCMeta): #Interface
    dataSourceType: DataSourceType

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '__init__') and callable(subclass.__init__)) and \
               (hasattr(subclass, 'isAvailable') and callable(subclass.isAvailable)) and \
               (hasattr(subclass, 'getData') and callable(subclass.getData)) and \
               (hasattr(subclass, 'dataSourceType') and callable(subclass.getDataSourceType))

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
    @abc.abstractmethod
    def dataSourceType(self):
        return self.dataSourceType

    def __str__(self):
        return self.dataSourceType

DATA_SOURCES = [DataSource(DataSourceType.OFFLINE), DataSource(DataSourceType.MARIADB), DataSource(DataSourceType.BIGQUERY)]

def machineIsOnline():
    return False #TODO

def detectAvailableDataSources():
    return list(filter(lambda x: x.isAvailable(), DATA_SOURCES))

def getDataSource():
    data_source_list = detectAvailableDataSources()
    selection = input(f"What data source do you want to use? Options are: {list(map(lambda x: str(x), data_source_list))}\n")
    for source in DATA_SOURCES:
        if selection == source.getDataSourceType():
            return source
    return None
