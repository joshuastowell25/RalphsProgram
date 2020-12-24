import os
import datetime
import string

import database
import pandas
from definitions import DATA_PATH

def getDataFromDatabase(dbConnection = None):
    while(dbConnection is None):
        companyName = input("What data file do you want to use? \n")
        dbConnection = database.getDbConnection(companyName)
        if dbConnection is None:
            print("No file exists named " + companyName)

    data, dates = database.loadDataFromDatabase(dbConnection)
    return {'dates': dates, 'data': data, 'dbConnection': dbConnection}



#gets an array of data from a particular file
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
    dates = []
    for line in lines_list:
        tokens = line.split(",")
        if(len(tokens) > 1):
            data.append(float(tokens[5])*100) #multiply by 100 to get rid of the pennies
            dateTimeStr = tokens[0]+" "+tokens[1] #e.g. '06/29/2019 08:15'
            dateTimeObj = datetime.datetime.strptime(dateTimeStr, '%m/%d/%Y %H:%M:%S')
            dates.append(dateTimeObj)
        else:
            data.append(int(100*float(tokens[0])))
    print ("\n")
    if(len(dates) == 0):
        dates = None
    return data, filename, dates

#saves data to a given filename
def saveData(data, filename, dates=None):
    hasDates = (dates != None)
    with open(os.path.join(DATA_PATH, filename), 'w') as filehandle:
        for i in range(0, len(data)):
            if hasDates:
                filehandle.write(str(dates[i])+","+str(float(data[i])/100)+"\n")
            else:
                filehandle.write(str(float(data[i])/100)+"\n")
        filehandle.close()

def clearTerminal():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')    

#displays the commands for the systems menu. 
def enterDataMenu():
    clearTerminal()
    command = 0
    print("Welcome to the data menu. Please select from the following options:")
    while command != 'q':
        command = input("DATA MENU: b=back, v=view companies\n")
        if command == 'q' or command == 'b':
            return
        elif command == 'v':
            return 
            #TODO: list data files