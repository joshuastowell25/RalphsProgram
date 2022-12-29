import os
import datetime
import database
from constants import DATA_PATH

#Remember each database connection currently represents a company
def getDbConnection():
    dbConnection = None
    while (dbConnection is None):
        companyName = input("What data file do you want to use? \n")
        dbConnection = database.getDbConnection(companyName)
        if dbConnection is None:
            print("No file exists named " + companyName)
    return dbConnection

def getDataFromDatabase(dbConnection = None):
    dbConnection = getDbConnection()
    data, dates = database.loadDataFromDatabase(dbConnection)
    return {'dates': dates, 'data': data, 'dbConnection': dbConnection}


#gets an array of data from a particular flat file instead of the database
def getDataFromFile(filename = None): #filename defaults to None
    file_handle = None
    while(file_handle is None):
        try:
            if filename is None:
                filename = input("What data file do you want to use? \n")
            filename = filename.lower()
            filename += ".dat"
            file_handle = open(os.path.join(DATA_PATH, filename), 'r')
        except Exception as e:
            print("No file exists named "+filename)
            filename = None

    lines_list = file_handle.readlines()
    data = []
    datetimes = []
    for line in lines_list:
        tokens = line.split(",")
        if(len(tokens) > 1):
            data.append(float(tokens[5]))
            dateTimeStr = tokens[0]+" "+tokens[1] #e.g. '06/29/2019 08:15'
            dateTimeObj = datetime.datetime.strptime(dateTimeStr, '%m/%d/%Y %H:%M:%S')
            datetimes.append(dateTimeObj)
        else:
            data.append(float(tokens[0]))
    print ("\n")
    if(len(datetimes) == 0):
        datetimes = None
    return data, filename, datetimes

#saves data to a given filename
def saveDataToFile(data, filename, dates=None):
    hasDates = (dates != None)
    with open(os.path.join(DATA_PATH, filename), 'w') as filehandle:
        for i in range(0, len(data)):
            if hasDates:
                filehandle.write(str(dates[i])+","+str(data[i])+"\n")
            else:
                filehandle.write(str(data[i])+"\n")
        filehandle.close()

def clearTerminal():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')    

#displays the commands for the systems menu. 
def dataMenu(dbConnection = None):
    if dbConnection is None:
        dbConnection = getDbConnection()
    clearTerminal()
    command = 0
    print("Welcome to the data menu. Please select from the following options:")
    while command != 'q':
        command = input("DATA MENU: b=back, v=view companies, e=data entry\n")
        if command == 'q' or command == 'b':
            return
        elif command == 'v':
            print("COMPANY LIST")
            companyList = database.getCompanyList()
            print(companyList)
            return 
            #TODO: list data files
        elif command == 'e':
            print("DATA ENTRY MENU")
            #TODO: determine if the current dbConnection is for daily, hourly, minute, second, etc type data
            #for now, assuming data entry is only for daily data

            date_input = None
            value_input = None
            while date_input is None or value_input is None:
                try:
                    date_input = input("What date is your new data for? Enter in this format: mm/dd/yyyy")
                    datetime_object = datetime.strptime(date_input, '%m/%d/%y')
                    value_input = input("What is the price of the company?")
                    datum = float(value_input)
                    database.writeDatumToDatabase(dbConnection, datetime_object, datum)
                except Exception as e:
                    date_input = None
                    value_input = None
                    print("Malformed date or data input. Try again!")

            return