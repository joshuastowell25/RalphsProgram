# Module Imports
import mariadb
import sys
import config

#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
#database software: MariaDB
#use the mariaDb MySQL client: HeidiSQL or MySQL Workbench
#login with root:root
#type: use sp2000
#type: show tables
#type select * from _2

# Connect to MariaDB Platform where the database is the name of the data file being used.
# the database name given is generally a 'company name' e.g.:es, sp1985, etc.
def getDbConnection(database):
    conn = None
    try:
        conn = mariadb.connect(
            user=config.getConfig('DatabaseSection','db.user'),
            password=config.getConfig('DatabaseSection','db.password'),
            host=config.getConfig('DatabaseSection','db.host'),
            port=int(config.getConfig('DatabaseSection','db.port')),
            database=database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")

    return conn

def createDatabase(databaseName):
    print("Creating database: "+databaseName)
    try:
        conn = mariadb.connect(
            user=config.getConfig('DatabaseSection', 'db.user'),
            password=config.getConfig('DatabaseSection', 'db.password'),
            host=config.getConfig('DatabaseSection', 'db.host'),
            port=int(config.getConfig('DatabaseSection', 'db.port'))
        )
        cursor = conn.cursor()
        cursor.execute("create database "+databaseName)
        cursor.execute("use "+databaseName)

        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def loadColumn(dbConnection, colName):
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

def loadDataFromDatabase(dbConnection):
    data=[]
    dates=[]
    cursor = dbConnection.cursor()
    try:
        cursor.execute("SELECT time, value FROM data")
        for (line) in cursor:
            dates.append(line[0])
            data.append(float(line[1]))
    except mariadb.Error as e:
        pass
        # print(f"Error loading column: {e}")

    return data, dates

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