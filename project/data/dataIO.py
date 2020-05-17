import os
from definitions import DATA_PATH

#gets an array of data from a particular file
def getData(filename = None): #filename defaults to None
    if filename is None:
        filename = input("What data file do you want to use? \n")
    filename = filename.lower()
    filename += ".dat"
    file_handle = open(os.path.join(DATA_PATH, filename), 'r')
    lines_list = file_handle.readlines()
    data = []
    for line in lines_list:
        data.append(int(float(line)))
    print ("\n")
    return data, filename

#saves data to a given filename
def saveData(data, filename):
    with open(os.path.join(DATA_PATH, filename), 'w') as filehandle:
        for datum in data:
            filehandle.write('%s\n' % datum)
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