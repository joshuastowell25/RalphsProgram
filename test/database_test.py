import unittest

from dataIO.dataIO import take_user_data_input
from database.database import getLatest, getDbConnection, getCompanyList


class DbTestClass(unittest.TestCase):

    def test_getLatest(self):
        latest = getLatest(getDbConnection("sp"))
        print(latest)
        self.assertTrue(True)
        pass

    def test_getCompanyList(self):
        companyList = getCompanyList(getDbConnection("sp"))
        print(companyList)
        pass

    def test_data_entry(self):
        take_user_data_input(getDbConnection("sp"))
        pass
