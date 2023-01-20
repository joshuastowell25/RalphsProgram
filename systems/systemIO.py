import constants as const
from string import ascii_uppercase
import re
from domain import System, Systems, systemTypes


class systemKeys:
    DIVISORS = "divisors",
    TYPE = "type"
    CUMULATIVE_TOTAL = "cumulative_total"

#print the users system(s) that are currently entered
def printSystems(systems: Systems):
    headingWidth = 43
    columnWidth = 10
    #print the heading
    line = str("DIVISORS:").ljust(headingWidth)
    for j in range(len(systems.systems)):
        line += ascii_uppercase[j].rjust(columnWidth)
    print(line)

    #print the divisors
    for i in range(max([len(system.divisors) for system in systems.systems])):
        line = str("").ljust(headingWidth)

        for system in systems.systems:
            divisor = system.divisors[i] if i < len(system.divisors) else ''
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
def enterSystemsMenu(systems, versusSystems, confirmationSystems):
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
            printSystems(systems, versusSystems, confirmationSystems)
        keyContinue()

#asks the user to enter the systems to be calculated
def getSystems(dbConnection):
    systems = Systems(dbConnection)

    while True:
        system = System()
        if system.getDivisors():
            systems.addSystem(system)
        else:
            break

    return systems
