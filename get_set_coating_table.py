'''
    PIPESIM Python Toolkit
    Example: Get and set pipe coating table

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from utilities import open_model_from_case_study
import pandas as pd

# Import the sixgill library
from sixgill.definitions import Parameters

def _create_coating_table_With_Description():
    survey = {}
    survey[Parameters.CoatingHeatTransfer.THERMALCONDUCTIVITY] = [0.15, 0.17, 0.11]
    survey[Parameters.CoatingHeatTransfer.THICKNESS] = [0.1, 0.02, 0.15]
    survey[Parameters.CoatingHeatTransfer.DESCRIPTION] = ["First","Second","Third"]
    return pd.DataFrame(survey)

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

flowline = 'FL-3'
print("\n*** Get coating table ***")
coating_table = model.get_coating(Flowline=flowline)
print("Coating table of {0}:\n {1}".format(flowline, coating_table))

#Delete the coating table
model.delete_coating(Flowline=flowline)
#Try to get the coating table after delete(should come back with zero points)
coating_table = model.get_coating(Flowline=flowline)
print("Coating table of {0}:\n has now {1} points".format(flowline, coating_table.size))

print("\n*** Set coating table ***")
data_frame = _create_coating_table_With_Description()

model.set_coating(Flowline=flowline, value=data_frame)
check_coating_table = model.get_coating(context=flowline)

print("The coating table is now:\n {}".format(check_coating_table))

print('\n*** Deleting coating table ***')
#Delete the coating table
model.delete_coating(Flowline=flowline)
check_coating_table = model.get_coating(context=flowline)
print("The coating table is now:\n {}".format(check_coating_table))

# Close the model
print("\nClosing model...")
model.close()
