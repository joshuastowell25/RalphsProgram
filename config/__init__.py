#This is the config PACKAGE (a package in python is a directory of python files. Each file is a module)

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["configuration"] # controls what 'from config import *' does

#control what 'import config' actually does.
from .configuration import runningTotalsFlag, getConfig #now you can call config.config to access the configuration settings
