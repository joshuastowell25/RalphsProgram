#This is the calculation package

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["calculation"] # controls what 'from data import *' does

#control what 'import calculation' actually does.
from .calculation import calcSysCols