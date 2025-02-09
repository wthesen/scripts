'''
    PIPESIM Python Toolkit
    Example: Export engine files

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from sixgill.pipesim import Model
from utilities import open_model
import os
import tempfile

model = open_model("./models/CSN_301_Small Network_MFL.pips")

# Export network simulation files to current pipesim file folder
files = model.tasks.networksimulation.generate_engine_files(study="Study 1")
print("The exported network simulation files are:")
print(files)

# Export p/t profile simulation files to a specified folder
folder = os.path.join(tempfile.gettempdir(), 'pipesim')
files = model.tasks.ptprofilesimulation.generate_engine_files(producer="Well", study="Study 1", folder_path=folder)
print("The exported P/T profile simulation files are:")
print(files)

model.close()
