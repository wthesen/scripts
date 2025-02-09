'''
    PIPESIM Python Toolkit
    Example: Export a well into a folder
'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

# Import the sixgill library and anything else we need
from sixgill.pipesim import Model
from utilities import open_model_from_case_study

# Open the model
wellname="Well"
wellfolder="~/AppData/Local/Temp"
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Display its information
print(model.about())

# Export all the wells in the model and show what files were created
print("Exporting well '{}' into '{}'".format(wellname, wellfolder))
files = model.export_well(context=wellname, folder=wellfolder)
print (files)

# Close the model
print("Closing model...")
model.close()
