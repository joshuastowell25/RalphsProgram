#This is the systems package

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["systemIO"] # controls what 'from systems import *' does

#control what 'import systems' actually does. 
from .systemIO import printSystems, getSystems, enterSystemsMenu #now you can call systems.printSystems