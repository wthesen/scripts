'''
    PIPESIM Python Toolkit
    Example: Get and set value

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

print("Get the bean size of choke")
choke = 'choke'
value = model.get_value(context=choke, parameter=Parameters.Choke.BEANSIZE)
print('The bean size of {0} is {1}'.format(choke, value))

print("Set the bean size of choke")
new_value = 3.0
model.set_value(Choke='choke', parameter=Parameters.Choke.BEANSIZE, value=new_value)
value = model.get_value(context='choke', parameter=Parameters.Choke.BEANSIZE)
print('The bean size of {0} is set to {1}'.format(choke, value))

# Close the model
print("Closing model...")
model.close()
