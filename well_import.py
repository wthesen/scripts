'''
    PIPESIM Python Toolkit
    Example: Import a previously exported well
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
from utilities import open_model_from_case_study, save_model
import os.path

# Open the file
print("Opening model for importing well")
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Display its information
print(model.about())

# Import the well that was previously exported (well_export.py)
well = os.path.expanduser("~/AppData/Local/Temp/Well.pips")

print("Importing well '{}'".format(well))    
model.import_well(filename=well, \
    name="Well1", fluid_override=False, overwrite_existing=True)

save_model(model, "CSN_301_Small Network_Compositional.pips")

print("Closing model...")
model.close()
