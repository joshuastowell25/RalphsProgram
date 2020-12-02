import configparser

config = configparser.RawConfigParser()
config.read('../config.ini')

def getConfig(section, propName):
    return config.get(section, propName)