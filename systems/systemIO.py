import constants as const
from string import ascii_uppercase
import re

#To import this file in python do: from systems import systemIO
#Then you can do things like: systemIO.theFuncName()

#print the users system(s) that are currently entered
def printSystems(systems, versusSystems, confirmationSystems):
    headingWidth = 43
    columnWidth = 10

    line = str("DIVISORS:").ljust(headingWidth)
    for j in range(len(systems)):
        line += ascii_uppercase[j].rjust(columnWidth)
    for system in versusSystems:
        line += (ascii_uppercase[system[0]] + ascii_uppercase[system[1]]).rjust(columnWidth)
    for system in confirmationSystems:
        line += (ascii_uppercase[system[0]] + ascii_uppercase[system[1]]).rjust(columnWidth)
    print(line)


    for i in range(max([len(system) for system in systems])):
        line = str("").ljust(headingWidth)
        for system in systems:
            divisor = system[i] if i < len(system) else ''
            line += str(divisor).rjust(columnWidth)
        print(line)

#Lists the names of the saved systems so the user can select one to open
def listSavedSystems():
    import os
    index = 0
    files = os.listdir(const.SAVED_SETUPS_PATH)
    for filename in files:
        index = index + 1
        print(index," ", filename)
        printSavedSys(filename)

#prints the saved divisors in the given sys file
def printSavedSys(filename):
    import os
    file_handle = open(os.path.join(const.SAVED_SETUPS_PATH, filename), 'r')
    lines_list = file_handle.readlines()
    for line in lines_list:
        print(line)

def clearTerminal():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')    

def showSetup(setup):
    print("")

def keyContinue():
    input("\nPress any key to continue...")
    clearTerminal()

#displays the commands for the systems menu. 
#arg1: systems: Given to the systems menu for printing
def enterSystemsMenu(systems):
    clearTerminal()
    command = 0
    print("Welcome to the systems menu. Please select from the following options:")
    while command != 'q':
        command = input("SYSTEMS MENU: b=back, v=view saved, s=show current system\n")
        if command == 'q' or command == 'b':
            return
        elif command == 'v':
            listSavedSystems()
        elif command == 's':
            printSystems(systems)
        keyContinue()

#asks the user how many number systems they want
def getSystems():
    systems = []
    cols = input("How many systems/columns do you want? \n")
    try:
        cols = int(cols)
    except:
        print ("BAD INPUT!")
        return getSystems()

    print ("\n")
    for i in range(int(cols)):
        systems.append(getSysNumbers(i))

    return systems

#asks the user what numbers they want in a particular system
#sys is the column index into the system columns (0=system A, 1=system B, ...)
def getSysNumbers(sys): 
    system = []
    quit = False
    while quit is False:
        val = input("Enter numbers for system "+str(chr(sys+65)).lower()+" (q to finish) ")

        vals = re.findall(r"[\w']+", val)
        for val in vals:
            try:
                system.append(int(val.replace("q","")))
            except:
                pass
            if "q" in val:
                quit = True

    print ("\n" )
    return system
