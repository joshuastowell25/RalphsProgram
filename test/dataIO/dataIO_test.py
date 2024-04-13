import unittest

import data_connectors.connectors.ConnectorInterface
from dataIO import getDataFromFile
from data_connectors.connectors.FlatFileConnector import OfflineFlatFileDataSource #from the file import the class

class DataIoTestClass(unittest.TestCase):
    def test_getDataFromFile(self):
        getDataFromFile("test.csv")