#This is the data package

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["dataIO"] # controls what 'from data import *' does

#control what 'import dataIO' actually does.
from .dataIO import getData, saveData, enterDataMenu #now you can call data.getData