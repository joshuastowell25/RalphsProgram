import configparser
import os
configFile = 'config.ini'

cwd = os.getcwd()
print("cwd: "+cwd)
#assert os.path.exists(configPath)

config = configparser.RawConfigParser()
config.read(configFile)

def getConfig(section, propName):
    print("cwd: " + cwd + "\n")
    actualPath = os.path.join(cwd, configFile)
    print("configPath: "+actualPath)
    print("config path exists? "+str(os.path.exists(actualPath)))
    print("Got config: "+str(config))

    return config.get(section, propName)