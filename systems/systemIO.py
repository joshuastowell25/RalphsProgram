from domain.System import System
from domain.Systems import Systems
from utils import constants, screen_tools

#Lists the names of the saved systems so the user can select one to open
def listSavedSystems():
    import os
    index = 0
    files = os.listdir(constants.SAVED_USER_OPTIONS_PATH)
    for filename in files:
        index = index + 1
        print(index," ", filename)
        printSavedSys(filename)

#prints the saved divisors in the given sys file
def printSavedSys(filename):
    import os
    file_handle = open(os.path.join(constants.SAVED_USER_OPTIONS_PATH, filename), 'r')
    lines_list = file_handle.readlines()
    for line in lines_list:
        print(line)

def showSetup(setup):
    print("")

def keyContinue():
    input("\nPress any key to continue...")
    screen_tools.clearTerminal()

#displays the commands for the systems menu. 
#arg1: systems: Given to the systems menu for printing
def enterSystemsMenu(systems: Systems):
    screen_tools.clearTerminal()
    command = 0
    print("Welcome to the systems menu. Please select from the following options:")
    while command != 'q':
        command = input("SYSTEMS MENU: b=back, v=view saved, s=show current system\n")
        if command == 'q' or command == 'b':
            return
        elif command == 'v':
            listSavedSystems()
        elif command == 's':
            for system in systems.getSystems():
                print(str(system))
        keyContinue()

#asks the user to enter the systems to be calculated
def getSystems():
    systems = Systems()
    while True:
        system = System()
        if system.getDivisors():
            systems.addSystem(system)
        else:
            break

    return systems
