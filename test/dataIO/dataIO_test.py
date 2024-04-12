import unittest

import datasource.datasources.DataSource
from dataIO import getDataFromFile
from datasource.datasources.OfflineFlatFileDataSource import OfflineFlatFileDataSource #from the file import the class

class DataIoTestClass(unittest.TestCase):
    def test_getDataFromFile(self):
        getDataFromFile("test.csv")