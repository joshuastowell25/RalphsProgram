import os

from utils.Logger import Logger

APPLICATION_NAME = "RalphsProgram"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
ROOT_DIR = os.path.join(os.getcwd().split(APPLICATION_NAME)[0], APPLICATION_NAME)  # This is your Project Root
#sys.path.append(ROOT_DIR)
LOG_PATH = os.path.join(ROOT_DIR, "logs")
SAVED_USER_OPTIONS_PATH = os.path.join(ROOT_DIR, 'systems', 'saved')
DATA_PATH = os.path.join(ROOT_DIR, 'data')
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.ini')

LOGGER = Logger()