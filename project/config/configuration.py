import configparser
import os
configFile = 'config.ini'

cwd = os.getcwd()
config = configparser.RawConfigParser()
configPath = os.path.join(cwd, configFile)
config.read(configPath)

def getConfig(section, propName):
    return config.get(section, propName)

runningTotalsFlag = getConfig('FlagSection','flags.runningTotals')