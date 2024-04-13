import datetime
import unittest
import database
from dataIO.mariaDbIO import take_user_data_input, take_user_file_input



class DbTestClass(unittest.TestCase):

    def test_getLatest(self):
        latest = database.getLatest(database.getDbConnection("sp"))
        print(latest)
        self.assertTrue(True)
        pass

    def test_getCompanyList(self):
        companyList = database.getCompanyList(database.getDbConnection("sp"))
        print(companyList)
        pass

    def test_take_user_data_input(self):
        take_user_data_input(database.getDbConnection("sp"))

    def test_take_user_file_input(self):
        take_user_file_input(database.getDbConnection("sp"), "./sp500.csv")

    def test_take_user_file_input(self):
        dbConn = database.getDbConnection("tsla")
        take_user_file_input(dbConn, "C:/Users/joshu/Downloads/.csv")

    def test_writeDatumToDatabase(self):
        conn = database.getDbConnection("sp")
        database.writeDatumToDatabase(conn, datetime.datetime.now(), 9999.99)
        conn.commit()

    def test_loadDatapointsFromDatabase(self):
        datapoints = database.loadDatapointsFromDatabase(database.getDbConnection("sp"))
        assert(len(datapoints)>20)
