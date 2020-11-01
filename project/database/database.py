# Module Imports
import mariadb
import sys

#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
# Connect to MariaDB Platform where the database is the name of the data file being used.
def connectToMariaDb(database):
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
    return conn.cursor()

# requires a mariaDB cursor (the thing that represents your connection to MariaDB)
def getColumn(cursor, table, colName):
    column = []
    cursor.execute("SELECT CAST(_4 AS INTEGER) FROM columns")
    for (item) in cursor:
        column.append(item[0])
    return column


cursor = connectToMariaDb("columns")
column = getColumn(cursor, "columns", "_4")
print(column)