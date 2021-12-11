#This is the calculation PACKAGE

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["calculation"] # controls what 'from data import *' does

#control what 'import calculation' actually does.
#.calculation is the calculation.py file. This is also known as a module. project > package > module
from .calculation import calcSysCols, calculateColumnRalphsMA