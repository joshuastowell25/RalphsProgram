#This is the data PACKAGE (a package in python is a directory of python files. Each file is a module)

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["alphaVantage", "mariaDb"] # controls what 'from alphaVantage import *' does. This is the list of files to include in __all__.

#control what 'import datasources' actually does.
from .alphaVantage import *
from .mariaDb import *


