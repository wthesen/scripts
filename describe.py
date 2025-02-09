'''
    PIPESIM Python Toolkit
    Example: Describe the parameter details

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
from sixgill.definitions import Parameters, ModelComponents
from utilities import open_model_from_case_study

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

print("Get the bean size of choke description")
choke = 'choke'
description = model.describe(context = choke, parameter = Parameters.Choke.BEANSIZE)
print("Choke BeanSize engineering unit: '{}'".format(description.units))
print("Choke BeanSize unit symbol: '{}'".format(description.units_symbol))
print("Choke BeanSize unit offset to SI: '{}'".format(description.si_offset))
print("Choke BeanSize unit scale to SI: '{}'".format(description.si_scale))

# Alernatively, use the model component to find out what it is (not supported yet)
# id_desc = model.describe(component=ModelComponents.FLOWLINE, parameter = Parameters.Flowline.INNERDIAMETER)
# print("The flowline inner diameter is in {}".format(id_descr.units))

# Close the model
print("Closing model...")
model.close()
