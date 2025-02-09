'''
    PIPESIM Python Toolkit
    Example: Get and set relative permeability data for Darcy IPR model

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
from sixgill.definitions import Parameters

well_name = 'Well_1'
completion_name = 'Completion'

def _create_relative_permeability_data():
    data = {}
    data[Parameters.RelativePermeability.WATERSATURATION] = [0, 0.3, 0.7]
    data[Parameters.RelativePermeability.RELATIVEPERMEABILITYOIL] = [0.3, 0.5, 1]
    data[Parameters.RelativePermeability.RELATIVEPERMEABILITYWATER] = [0.12, 0.2, 0.25]
    return pd.DataFrame(data)

def _fetch_and_display_relative_permeability_data(model):
    relative_permeability_data = model.get_relative_permeability_data(Well = well_name, Completion = completion_name)
    _display_relative_permeability_data(relative_permeability_data)

def _display_relative_permeability_data(relative_permeability_data):
    print("Relative permeability data for '{0}' :\n {1}".format(completion_name, relative_permeability_data))

# Open the model
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")

# Get relative permeability
print("\n*** Get relative permeability data ***")
relative_permeability_data = model.get_relative_permeability_data(Well = well_name, Completion = completion_name)
_display_relative_permeability_data(relative_permeability_data)

# Set relative permeability data
print("\n*** Set relative permeability data ***")
data_frame = _create_relative_permeability_data()
model.set_relative_permeability_data(Well = well_name, Completion = completion_name, value = data_frame)
_fetch_and_display_relative_permeability_data(model)

# Delete the relative permeability data
print('\n*** Deleting relative permeability data ***')
model.delete_relative_permeability_data(Well = well_name, Completion = completion_name)
_fetch_and_display_relative_permeability_data(model)

# Close the model
print("\nClosing model...")
model.close()
