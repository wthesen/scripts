'''
    PIPESIM Python Toolkit
    Example: Export all the wells from a model into the current folder
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
import os

# Open the model
print("Opening model for exporting wells...")
model = open_model_from_case_study("./Network Models/CSN_307_Onshore PI Facility.pips")

# Display its information
print(model.about())

# Create ourselves a folder to store the files
if not os.path.exists("WellExport"):
    os.makedirs("WellExport")
os.chdir("WellExport")

# Export two wells
files = model.export_well(well_names=["ESP_Well","Gas_Lift_Well"])
print (files)
# Export all the wells in the model and show what files were created
files = model.export_well()
print (files)
#export "RP_Well"
files = model.export_well(Well="RP_Well")
print (files)
#export "Ver_ML_WI_Well"
files = model.export_well(context="Ver_ML_WI_Well")
print (files)

# Close the model
print("Closing model...")
model.close()
