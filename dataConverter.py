#!/usr/bin/env python
import os
import sys
import traceback
import dataIO as dataIO

try:
    data, filename, dates = dataIO.getDataFromFile()
    outname = input("what should be the output filename?")
    dataIO.saveDataToFile(data, outname, dates)

except Exception as e:
    print(f"Error: {e}")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(traceback.format_exc())
    input("There was an Error. Press Enter to Exit...")