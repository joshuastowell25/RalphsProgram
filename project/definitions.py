import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
SAVED_SETUPS_PATH = os.path.join(ROOT_DIR, 'systems', 'saved')
DATA_PATH = os.path.join(ROOT_DIR, 'data')

def enum(**named_values):
    return type('Enum', (), named_values)

#MaTypes.RalphStyle and MaTypes.NormalStyle
MaTypes = enum(RalphStyle = 1, NormalStyle = 2)