# Module Imports
import mariadb
import sys

#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
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
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

# requires a mariaDB cursor (the thing that represents your connection to MariaDB)
def loadColumn(cursor, colName):
    column = []

    try:
        cursor.execute("SELECT CAST(value AS INTEGER) FROM " + colName)
        for (item) in cursor:
            column.append(item[0])
    except mariadb.Error as e:
        print(f"Error: {e}")

    return column

#inserts new data into the database for the given column.
def saveColumn(conn, col, colName):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS "+colName+" (value INT NOT NULL)");

    cursor.execute("SELECT COUNT(*) FROM WORKED")
    count = cursor.fetchone()[0]

    for i in range(count, len(col)): #indices 4 to 9
        cursor.execute("INSERT INTO "+colName+ " (value) values ("+str(col[i])+")")

    conn.commit()


#probably need an update to the DB schema where each datafile has it's own DB then each divisor has it's own table and the column name is something
#plain and generic like "data" or "value"
conn = getDbConnection("sp2000")
#column = getColumn(cursor, "_2")
#print(column)

saveColumn(conn, [1,2,3,4,5,6,7,8,9,10], "worked")