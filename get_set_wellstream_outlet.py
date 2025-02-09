'''
    Pipesim Python Toolkit
    Example: Get and set wellstream outlet

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
from sixgill.definitions import Parameters, ModelComponents, Constants
from utilities import open_model_from_case_study
import pandas

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Black oil fluid
# Get and set wellstream outlet
print("Get the source(wellstream outlet) for well")
well_name = 'Well'
print("Wellstream outlet: " + model.get_value(Well = well_name, parameter = Parameters.Well.WELLOUTLETEQUIPMENT))

# Set the choke as the wellstream outlet
model.set_value(Well = well_name, parameter = Parameters.Well.WELLOUTLETEQUIPMENT, value = "Choke")
print("Wellstream outlet: " + model.get_value(Well = well_name, parameter = Parameters.Well.WELLOUTLETEQUIPMENT))

# Set the flowline as the wellstream outlet
model.set_value(Well = well_name, parameter = Parameters.Well.WELLOUTLETEQUIPMENT, value = "FL-1")
print("Wellstream outlet: " + model.get_value(Well = well_name, parameter = Parameters.Well.WELLOUTLETEQUIPMENT))

# Set the well head as the wellstream outlet
well = model.find_components(Well = well_name, component = ModelComponents.WELL)[0]
model.set_value(Well = well_name, parameter = Parameters.Well.WELLOUTLETEQUIPMENT, value = well)
print("Wellstream outlet: " + model.get_value(Well = well_name, parameter = Parameters.Well.WELLOUTLETEQUIPMENT))

#set the source fluid to 'C-Fluid'
sources = model.find_components(Well = well_name, component = ModelComponents.SOURCE)
source_name = sources[0].name
model.set_value(Source = source_name, parameter = Parameters.Well.ASSOCIATEDCOMPOSITIONALFLUID, value = "C-Fluid")
print("Associated compositional fluid: " + model.get_value(Source = source_name, parameter = Parameters.Well.ASSOCIATEDCOMPOSITIONALFLUID))

# Close the model
print("Closing model...")
model.close()
