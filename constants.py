import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
SAVED_USER_OPTIONS_PATH = os.path.join(ROOT_DIR, 'systems', 'saved')
DATA_PATH = os.path.join(ROOT_DIR, 'data')

#MaTypes.RalphStyle and MaTypes.NormalStyle
MaTypes = enum(RalphStyle = 1, NormalStyle = 2)