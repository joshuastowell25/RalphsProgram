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
    timeWindowing = None
    while(timeWindowing != 'y' and timeWindowing != 'n'):
        timeWindowing = input("Do you want to select a time window (y or n)?\n").lower()

    if timeWindowing == 'y':
        earliestDate = dates[0]
        latestDate = dates[len(dates)-1]
        print("You can choose time windows between "+str(earliestDate)+" and "+str(latestDate))
        startDate = datetime.datetime.strptime("12/12/1950 00:00:00", '%m/%d/%Y %H:%M:%S')
        endDate = datetime.datetime.strptime("12/12/1980 00:00:00", '%m/%d/%Y %H:%M:%S')

        while(startDate is None):
            try:
                timeA = input("Enter the start date for your time window\n")
                timeA = timeA + " 00:00:00"
                startDate = datetime.datetime.strptime(timeA, '%m/%d/%Y %H:%M:%S')
                #make sure startDate is on or after the 0th date
                if(not(startDate >= earliestDate)):
                    print("BAD DATE: You can only choose time windows between "+str(earliestDate)+" and "+str(latestDate)+"\n")
                    startDate = None
            except Exception as e:
                print(f"BAD DATE: {e}")
                startDate = None

        while (endDate is None):
            try:
                timeB = input("Enter the end date for your time window\n")
                timeB = timeB + " 00:00:00"
                endDate = datetime.datetime.strptime(timeB, '%m/%d/%Y %H:%M:%S')
                #make sure endDate is on or before the last date
                if (not(endDate <= latestDate)):
                    print("BAD DATE: You can only choose time windows between " + str(earliestDate) + " and " + str(
                        latestDate)+"\n")
                    endDate = None
                if(not(endDate > startDate)):
                    print("BAD DATE: The end date must be AFTER the start date.\n")
                    endDate = None
            except Exception as e:
                print(f"BAD DATE: {e}")
                endDate = None

        #convert timestamps to datetimes using list comprehension
        dates_df = pandas.to_datetime(dates).to_frame()
        data_df = pandas.DataFrame(data)
        dates_df = dates_df.truncate(before=startDate, after=endDate)

        cols = dates_df.columns.values
        thing = dates_df[0]
        firstDate = dates_df[0].iloc[0]
        lastDate = dates_df[0].iloc[len(dates_df.index) - 1]
        #find the index of the startTime and endTimes
        startIndex = dates.index(firstDate)
        endIndex = dates.index(lastDate)

        dates = dates[startIndex:endIndex]
        data = data[startIndex:endIndex]

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