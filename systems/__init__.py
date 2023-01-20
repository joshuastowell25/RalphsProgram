#This is the systems PACKAGE (a package in python is a directory of python files. Each file is a module)

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["systemIO"] # controls what 'from systems import *' does. This is the list of files to include in __all__.

#control what 'import systems' actually does. 
from .systemIO import *
