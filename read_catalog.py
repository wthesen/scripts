'''
    PIPESIM Python Toolkit
    Example: Read catalog for ESP model

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
from sixgill.definitions import ModelComponents, Parameters
from utilities import open_model_from_case_study
from pandas import DataFrame

# Open the model directly
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# add ESP1 to well
model.add(ModelComponents.ESP, "Esp1", context="Well", parameters={Parameters.ESP.TOPMEASUREDDEPTH:1500})
model.set_value(context="Well:Esp1", parameter=Parameters.ESP.MANUFACTURER, value="ALNAS")
model.set_value(context="Well:Esp1", parameter=Parameters.ESP.MODEL, value="ANA580")
print("ESP data before reading from catalog")
values = model.get_values(context="Well:Esp1")
print(DataFrame(values))
# read from catalog
model.read_catalog(context="Well:Esp1")
print("The ESP model has been loaded from catalog. New ESP model data:")
values = model.get_values(context="Well:Esp1")
print(DataFrame(values))

model.close()
