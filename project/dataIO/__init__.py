#This is the data module

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["dataIO"] # controls what 'from dataIO import *' does. This is the list of files to include in __all__.

#control what 'import dataIO' actually does.
from .dataIO import getDataFromFile, getDataFromDatabase, saveData, enterDataMenu #now you can call data.getData
