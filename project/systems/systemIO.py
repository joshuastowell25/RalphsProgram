from definitions import SAVED_SETUPS_PATH
import json

#To import this file in python do: from systems import systemIO
#Then you can do things like: systemIO.theFuncName()

#print the users system(s)
def printSystems(systems):
    for system in systems:
        print(system)

#Lists the names of the saved systems
def listSavedSystems():
    import os
    index = 0
    arr_txt = [x.replace(".sys", "") for x in os.listdir(SAVED_SETUPS_PATH) if x.endswith(".sys")]
    for item in arr_txt:
        index = index + 1
        print(index," ", item)


def showSystem():
    print("")

def enterSystemsMenu():
    command = 0
    while command != 'q':
        command = input("commands: b=back, v=view saved")
        if command == 'q':
            return
        elif command == 'v':
            listSavedSystems()
