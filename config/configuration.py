import configparser
import os

cwd = os.getcwd().split('RalphsProgram')[0]
config = configparser.RawConfigParser()

configPath = os.path.join(cwd, 'RalphsProgram', 'config.ini')
print(f"Reading config from: {configPath}")
config.read(configPath)

def getConfig(section, propName):
    return config.get(section, propName)

runningTotalsFlag = getConfig('FlagSection','flags.runningTotals') in ['true', 'True', 'TRUE']