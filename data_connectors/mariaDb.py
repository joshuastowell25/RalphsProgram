# Module Imports
import mariadb
import sys

import domain
from config import getConfig

#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
#database software: MariaDB
#use the mariaDb MySQL client: HeidiSQL or MySQL Workbench
#login with root:root
#type: show databases  to see all the available company names
#type: use sp2000, use sp, use es, etc to select a company name
#type: show tables  to see the available tables such as: data, _2, _4, _6, etc.
#type select * from _2

# Connect to MariaDB Platform where the database is the name of the data file being used.
# the database name given is generally a 'company name' e.g.:es, sp1985, etc.
def getDbConnection(companyName):
    conn = None
    #print("Attempting to connect, please wait")
    try:
        conn = mariadb.connect(
            user=getConfig('DatabaseSection','db.user'),
            password=getConfig('DatabaseSection','db.password'),
            host=getConfig('DatabaseSection','db.host'),
            port=int(getConfig('DatabaseSection','db.port')),
            database=companyName,
            connect_timeout=2
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}. Has the database IP address changed or is the server powered down?")

    return conn

def createDatabase(databaseName):
    print("Creating database: "+databaseName)
    try:
        conn = mariadb.connect(
            user=getConfig('DatabaseSection', 'db.user'),
            password=getConfig('DatabaseSection', 'db.password'),
            host=getConfig('DatabaseSection', 'db.host'),
            port=int(getConfig('DatabaseSection', 'db.port'))
        )
        cursor = conn.cursor()
        cursor.execute("create database "+databaseName)
        cursor.execute("use "+databaseName)

        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def loadMaColumn(dbConnection, colName):
    column = []
    cursor = dbConnection.cursor()
    try:
        cursor.execute("SELECT value FROM " + colName)
        for (item) in cursor:
            column.append(item[0])
    except mariadb.Error as e:
        pass
        #print(f"Error loading column: {e}")

    return column

def getCompanyList(dbConnection):
    companyList = []
    cursor = dbConnection.cursor()
    try:
        cursor.execute("show databases")
        companyList = [tup[0] for tup in cursor.fetchall()]
        while 'information_schema' in companyList:
            companyList.remove('information_schema')
        while 'performance_schema' in companyList:
            companyList.remove('performance_schema')
        while 'mysql' in companyList:
            companyList.remove('mysql')
    except mariadb.Error as e:
        pass
    return companyList

#Each "company" aka database has several tables. The 'main' table is called 'data' the other tables are where the calculated moving averages lie.
def load_datapoints(dbConnection):
    datapoints = []
    cursor = dbConnection.cursor()
    try:
        cursor.execute("SELECT time, value FROM data")
        for (line) in cursor:
            datapoints.append(domain.Datapoint(line[0], float(line[1])))
    except mariadb.Error as e:
        pass
        # print(f"Error loading column: {e}")

    return datapoints

#dt is a python datetime type, datum is the price of the stock
def writeDatumToDatabase(dbConnection, dt, datum):
    dt.strftime('%Y-%m-%d %H:%M:%S')
    cursor = dbConnection.cursor()
    try:
        latest = getLatest(dbConnection)
        if(dt > latest['time']):
            query = f"INSERT INTO data (time, value) VALUES ('{dt.strftime('%Y-%m-%d %H:%M:%S')}', {datum})"
            cursor.execute(query)
            dbConnection.commit()
        else:
            print("The given date was not later than the latest date already recorded. Try again.")

    except mariadb.Error as e:
        print(f"Exception occurred inserting data into database: {e}\n")
        pass

def getLatest(dbConnection):
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"select * from data where time = (select max(time) from data);")
        query_result = cursor.fetchone()
        return {"id": query_result[0], "time": query_result[1], "value": query_result[2]}
    except mariadb.Error as e:
        print(f"Exception occurred: {e}")
        return None

#dtList is a list of datetime objects associated with the dataList
def writeDataToDatabase(dbConnection, dtList, dataList):
    pass #TODO

def updateDatumInDatabase(dbConnection, tableName, incrementNumber, dt, datum):
    cursor = dbConnection.cursor()
    try:
        #TODO: need to format dt as yyyy-mm-dd 16:00:00
        ymd = dt.strftime("%Y-%m-%d")
        cursor.execute(f"UPDATE data SET value={datum} WHERE time='{ymd} 16:00:00'")
    except mariadb.Error as e:
        print(f"Error updating column: {e}")
    #TODO: need to be able to update all the already calculated moving average columns when updating an old piece of data.
    #this will involve updating the calculation of all columns from incrementNumber-1 to incrementNumber-1+theDivisorNumber
    #E.g. for updating the _50 column, you would have to update calculated column indicies i-1 to i-1+50


#inserts new data into the database for the given divisor column.
# conn: the dbConnection
# col: the array of data
# tableName: e.g.: "_2", "_4", "_6"
def saveColumn(dbConnection, col, tableName):
    cursor = dbConnection.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS " + tableName + " (value FLOAT NOT NULL)");

        count = getCount(dbConnection, tableName)

        valString = ""
        length = len(col)
        for i in range(count, length, 1000):
            print("Saved "+str(i)+" of "+str(length)+" to db\n")
            for j in range(i , i + 1000):
                if(j < length):
                    valString += "("+str(col[j])+"),"
            valString = valString[:-1]
            if len(valString) > 0:
                cursor.execute("INSERT INTO " + tableName + " (value) values " + valString)
            valString = ""

        dbConnection.commit()
    except mariadb.Error as e:
        print(f"Error saving column: {e}")

def getCount(dbConnection, colName):
    cursor = dbConnection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM " + colName)
        count = cursor.fetchone()[0]  # get the count
        cursor.close()
        return count
    except mariadb.Error as e:
        print(f"Error getting count: {e}")

def tableExists(dbConnection, tableName):
    cursor = dbConnection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM information_schema.TABLE WHERE TABLE_NAME="+tableName)
        count = cursor.fetchone()[0]
        cursor.close()
        return count == 1
    except mariadb.Error as e:
        print(f"Error checking table existance: {e}")