import os
from datetime import datetime
from typing import List

import database
import domain
import terminal
from constants import DATA_PATH

def get_data():
    companyName = input("What data file do you want to use? \n")
    dbConnection = database.getDbConnection(companyName)
    if dbConnection is None:
        print(f"No database entry exists for file named {companyName}, checking local files.")
    else:
        return getDatapointsFromDatabase(dbConnection)
    return getDataFromFile(companyName+".csv")

#Remember each database connection currently represents a company
def getDbConnection():
    dbConnection = None
    while (dbConnection is None):
        companyName = input("What data file do you want to use? \n")
        dbConnection = database.getDbConnection(companyName)
        if dbConnection is None:
            print("Company name not in database: " + companyName)
    terminal.clearTerminal()
    return dbConnection

def getDatapointsFromDatabase(dbConnection = None):
    return database.load_datapoints(dbConnection)

#gets an array of data from a particular flat file instead of the database
def getDataFromFile(filename = None) -> List[domain.Datapoint]: #filename defaults to None
    file_handle = None
    while(file_handle is None):
        try:
            if filename is None:
                filename = input("What data file do you want to use? \n")
            filename = filename.lower()
            file_path = os.path.join(DATA_PATH, filename)
            file_handle = open(file_path, mode='r', encoding='utf-8-sig')
        except Exception as e:
            print("File does not exist: "+file_path)
            filename = None

    lines_list = file_handle.readlines()
    datapoints: List[domain.Datapoint] = []
    for line in lines_list:
        tokens = line.split(",")

        if(len(tokens) > 5): #OHLCV: open, high, low, close, vol
            dateTimeStr = tokens[0]+" "+tokens[1] #e.g. '06/29/2019 08:15'
            dateTimeObj = datetime.strptime(dateTimeStr, '%m/%d/%Y %H:%M:%S')
            datapoints.append(domain.Datapoint(dateTimeObj, float(tokens[5])))
        elif len(tokens) == 3: #tokens = ['1000', '08/18/2023', '\n']
            dateTimeStr = tokens[1] + " 16:00:00"
            dateTimeObj = datetime.strptime(dateTimeStr, '%m/%d/%Y %H:%M:%S')
            datapoints.append(domain.Datapoint(dateTimeObj, float(tokens[0])))
        elif len(tokens) == 2: #tokens = ['1000', '\n']
            datapoints.append(domain.Datapoint(datetime.now(), float(tokens[0])))

    return datapoints

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
        command = input("DATA MENU: b=back, v=view companies, e=data entry, l=load from file\n")
        if command == 'q' or command == 'b':
            return
        elif command == 'v':
            print("COMPANY LIST")
            companyList = database.getCompanyList()
            print(companyList)
            return 
        elif command == 'e':
            take_user_data_input(dbConnection)
        elif command == 'l':
            pass #TODO

def take_user_file_input(dbConnection, file_path=None):
    print("DATA FILE INPUT MENU")
    if file_path is None:
        file_path = input("Enter the fully qualified file path containing data in the form mm/dd/yyyy, price")
    with open(file_path) as file:
        line = file.readline()
        while line is not None:
            if len(line) > 10:
                data = line.split(",")
                datetime_object = datetime.strptime(data[0], '%m/%d/%Y').replace(hour=16,minute=00)  # assume closing time (4pm eastern time)
                price = data[1]
                database.writeDatumToDatabase(dbConnection, datetime_object, price)
                line = file.readline()
    dbConnection.commit()


def take_user_data_input(dbConnection):
    print("DATA ENTRY MENU")
    # TODO: determine if the current dbConnection is for daily, hourly, minute, second, etc type data
    # for now, assuming data entry is only for daily data

    date_input = None
    value_input = None
    while date_input is None or value_input is None:
        try:
            date_input = input("Provide the price associated with your date in this format: mm/dd/yyyy (q to quit)")
            if date_input == 'q':
                return
            datetime_object = datetime.strptime(date_input, '%m/%d/%Y').replace(hour=16,minute=00)  # assume closing time (4pm eastern time)
            value_input = input("What is the price? (q to quit)")
            if value_input == 'q':
                return
            while True:
                try:
                    datum = float(value_input)
                    break
                except:
                    print(f"Invalid price input! {value_input} Try Again.")

            confirm_input = input(f"Does this look right? The price at {datetime_object} was {datum}. Enter y or n")
            if confirm_input == 'y':
                database.writeDatumToDatabase(dbConnection, datetime_object, datum)
                dbConnection.commit()
            else:
                take_user_data_input(dbConnection)

        except Exception as e:
            date_input = None
            value_input = None
            print(f"Malformed date or data input. Try again! {e}")
    return
