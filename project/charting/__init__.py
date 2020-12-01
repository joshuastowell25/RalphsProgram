#This is the charting package

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["charting"] # controls what 'from charting import *' does

#control what 'import charting' actually does. 
from .charting import chartSystems #now you can call charting.chartSystems