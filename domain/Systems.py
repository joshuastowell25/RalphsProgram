import abc
from domain.Datapoint import Datapoint
from domain.System import System
from utils.data_types import enum

class Systems:
    dbConnection = None
    datapoints: list[Datapoint] = []
    systems: list[System] = []

    def __init__(self):
        self.systems = []
        self.datapoints = []
        pass

    def setDatapoints(self, datapoints: list[Datapoint]):
        self.datapoints = datapoints
        for system in self.systems:
            system.datapoints = self.datapoints
            system.calculate()

    def addSystem(self, system: System):
        system.datapoints = self.datapoints
        self.systems.append(system)
        system.calculate()

    def clearSystems(self):
        self.systems = []

    def getSystems(self):
        return self.systems

class TradingStrategyInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'calculate_cumulative_total') and
                callable(subclass.calculate_cumulative_total))

class NormalMovingAverageTradingStrategy:
    """Extract text from a PDF."""
    def calculate_cumulative_total(self, arg1: str, arg2: str) -> [Datapoint]:
        """Overrides TradingStrategyInterface.calculate_cumulative_total()"""
        pass
