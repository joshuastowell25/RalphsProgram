#This is the config package

#__init__.py files make python treat the directory they are in as a 'module'
__all__ = ["configuration"] # controls what 'from config import *' does

#control what 'import config' actually does.
from .configuration import config #now you can call config.config to access the configuration settings