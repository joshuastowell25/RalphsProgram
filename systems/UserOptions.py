import os
import json
from utils import constants

#'{"name": "mySystem1", "maType": "r", "systems": [[2], [4,10,20], [6]]}'
class UserOptions:
    name=""
    maType=""
    systems=[]

    def __init__(self, name, maType, systems):
        self.name = name
        self.maType = maType
        self.systems = systems

    #prints the JSON representation of this object
    def print(self):
        asJson = json.dump(self)
        print(asJson)

    #Setups are stored as JSON
    def loadFromFile(self, filepath):
        file = open(filepath, 'r')
        jsonString = file.readlines()
        asJson = json.load(jsonString)
        self.name = asJson["name"]
        self.maType = asJson["maType"]
        self.systems = asJson["systems"]

    #writes this setup to the setup file with its name
    def writeToFile(self):
        file = open(os.path.join(constants.SAVED_USER_OPTIONS_PATH, self.name, ".sys"), 'w')
        asJson = json.dump(self)
        file.write(asJson)
        file.close()