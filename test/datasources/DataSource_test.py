import unittest

import datasource.datasources.DataSource


class DataSourceTestClass(unittest.TestCase):
    def test_get_datasource(self):
        datasource.datasources.DataSource.getDataSource()

    def test_OfflineFlatFileDataSource(self):
