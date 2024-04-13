import unittest

import data_connectors.connectors.ConnectorInterface
from data_connectors.connectors.FlatFileConnector import OfflineFlatFileDataSource #from the file import the class


class DataSourceTestClass(unittest.TestCase):
    def test_get_datasource(self):
        data_connectors.datasources.DataSource.getDataSource()

    def test_OfflineFlatFileDataSource(self):
        source = OfflineFlatFileDataSource()
        data = source.getData()

        print(list(map(lambda x: str(x), data)))