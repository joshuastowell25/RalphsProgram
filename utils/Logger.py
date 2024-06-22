import sys
import traceback
from typing import IO
from utils import constants
import os

class Logger():
    logfile: IO = None

    def __init__(self):
        run_id = self.generate_run_id() #not sure why it forces me to access a static method through self
        self.logfile = open(os.path.join(constants.LOG_PATH, f"{run_id}.txt"), "a+")

    @staticmethod
    def generate_run_id():
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%m_%d_%Y_%H_%M_%S")
        return dt_string

    def log(self, message: str = "", err: BaseException = None):
        if err is not None:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            exception_origin_file = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
            message = f"{message}\nException: {traceback.format_exc()}\nType: {exception_type}\nFile: {exception_origin_file}\nLine: {exception_traceback.tb_lineno}\n"
        self.logfile.writelines(message)
        print(message)