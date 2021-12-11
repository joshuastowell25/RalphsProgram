import configparser
import os
configFile = 'config.ini'

cwd = os.getcwd()
config = configparser.RawConfigParser()
configPath = os.path.join(cwd, "project")
configPath = os.path.join(configPath, configFile)
config.read(configPath)

def getConfig(section, propName):
    print(f"Getting config from {configPath}")
    return config.get(section, propName)

runningTotalsFlag = getConfig('FlagSection','flags.runningTotals') in ['true', 'True', 'TRUE']