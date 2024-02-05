#This is the data PACKAGE (a package in python is a directory of python files. Each file is a module)

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["mariaDb.py"] # controls what 'from database import *' does. This is the list of files to include in __all__.

#control what 'import dataIO' actually does.
from .mariaDb import *
