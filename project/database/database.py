# Module Imports
import mariadb
import sys

#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
#database software: MariaDB
#use the mariaDb MySQL client: HeidiSQL or MySQL Workbench
#login with root:root
#type: use sp2000
#type: show tables
#type select * from _2

# Connect to MariaDB Platform where the database is the name of the data file being used.
def getDbConnection(database):
    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306,
            database=database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        if("Unknown database" in str(e)):
            return createDatabase(database)
        sys.exit(1)
    return conn

def createDatabase(databaseName):
    print("Creating database: "+databaseName)
    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306
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
        cursor.execute("SELECT CAST(value AS INTEGER) FROM " + colName)
        for (item) in cursor:
            column.append(item[0])
    except mariadb.Error as e:
        pass
        #print(f"Error loading column: {e}")

    return column

#inserts new data into the database for the given divisor column.
# conn: the dbConnection
# col: the array of data
# divisorColName: The name of the column in the database, e.g.: "_2", "_4", "_6"
def saveColumn(dbConnection, col, divisorColName):
    cursor = dbConnection.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS "+divisorColName+" (value INT NOT NULL)");

        count = getCount(dbConnection, divisorColName)

        valString = ""
        length = len(col)
        for i in range(count, length, 1000):
            print("Saved "+str(i)+" of "+str(length)+" to db\n")
            for j in range(i , i + 1000):
                if(j < length):
                    valString += "("+str(col[j])+"),"
            valString = valString[:-1]
            if len(valString) > 0:
                cursor.execute("INSERT INTO "+divisorColName+ " (value) values "+valString)
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