import datetime
import unittest

from dataIO.dataIO import take_user_data_input, take_user_file_input
from database.database import getLatest, getDbConnection, getCompanyList, writeDatumToDatabase


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

    def test_take_user_data_input(self):
        take_user_data_input(getDbConnection("sp"))

    def test_take_user_file_input(self):
        take_user_file_input(getDbConnection("sp"), "./sp500.csv")

    def test_writeDatumToDatabase(self):
        conn = getDbConnection("sp")
        writeDatumToDatabase(conn, datetime.datetime.now(), 9999.99)
        conn.commit()