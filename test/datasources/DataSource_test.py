import unittest

import datasource.datasources.DataSource
from datasource.datasources.OfflineFlatFileDataSource import OfflineFlatFileDataSource #from the file import the class


class DataSourceTestClass(unittest.TestCase):
    def test_get_datasource(self):
        datasource.datasources.DataSource.getDataSource()

    def test_OfflineFlatFileDataSource(self):
        source = OfflineFlatFileDataSource()
        data = source.getData()

        print(list(map(lambda x: str(x), data)))