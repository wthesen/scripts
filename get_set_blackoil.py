'''
    Pipesim Python Toolkit
    Example: Get and set Source Black Oil Parameters

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

# Import the sixgill library
from sixgill.pipesim import Model
from sixgill.definitions import Parameters, ModelComponents, Constants
from utilities import open_model_from_case_study
import pandas

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Black oil fluid
# Change the fluid used
print("Get the associated black oil fluid for the source")
value = model.get_value(context="Source", parameter=Parameters.Source.ASSOCIATEDBLACKOILFLUID)
print('The source is using {} fluid definition. Changing it to "BOFluid".'.format(value))

model.add(ModelComponents.BLACKOILFLUID, "BOFluid", parameters = {Parameters.BlackOilFluid.GOR:200, Parameters.BlackOilFluid.WATERCUT:5})
model.set_value(context="Source", parameter=Parameters.Source.ASSOCIATEDBLACKOILFLUID, value="BOFluid")

# Change the Rate Type
changeto = Constants.FlowRateType.LIQUIDFLOWRATE
value = model.get_value(context="Source", parameter=Parameters.Source.SELECTEDRATETYPE)
print('The source is setting {}, changing it to {}'.format(value, changeto))
model.set_value(context="Source", parameter=Parameters.Source.SELECTEDRATETYPE, value=changeto)

# Close the model
print("Closing model...")
model.close()
