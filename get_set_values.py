'''
    PIPESIM Python Toolkit
    Example: Getting values from a model

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
from sixgill.definitions import ModelComponents, Parameters, ALL
import pandas as pd
from collections import defaultdict
from utilities import open_model_from_case_study

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Get the values of a choke
beansize = model.get_value(Name="Choke", parameter=Parameters.Choke.BEANSIZE)
print("The bean size for choke 'Choke' is {}".format(beansize))

# Get all the parameters of the choke
params = model.get_values(Name="Choke")
print("The choke named 'Choke' is parameterized as follows:")
print(params)

# Get units for a given parameter
beansize_unit = model.describe(context="Choke", parameter=Parameters.Choke.BEANSIZE)
print("The bean size units symble for choke 'Choke' is '{}'".format(beansize_unit.units_symbol))

# Get all the parameters of the choke and include the unit symbols
params = model.get_values(context="Choke", show_units=True)
print("The choke named 'Choke' is parameterized as follows:")
print(params)

# Get the canvass locations for all the equipment on the sheet
locations = model.get_values(component=ALL, parameters=[Parameters.SurfaceComponent.X_COORD, Parameters.SurfaceComponent.Y_COORD])
print("The canvass location for each component is:")
for k,v in locations.items():
    print(k,v)

# Get all the parameters for all the compressors
params = model.get_values(Compressor=ALL)
print("The compressors are parameterized as:")
print(params)

# Check the thickness for all the flowline tubings
print("The current thickness of the flowline walls are:")
values = model.get_values(component=ModelComponents.FLOWLINE, parameters=[Parameters.Flowline.WALLTHICKNESS])
print(values)

# Set the thickness for all the flowline walls
print("Set the thickness value of all flowlines")
model.set_all_value(component=ModelComponents.FLOWLINE, parameter=Parameters.Flowline.WALLTHICKNESS, value=0.4)

# Check the thickness again an alternative way
print("The thickness of the flowline walls is now:")
flowlines = model.find(Flowline=ALL)
for flowline in flowlines:
    thickness = model.get_value(Flowline=flowline, parameter=Parameters.Flowline.WALLTHICKNESS)
    print("Flowline: {}, Thickness: {}".format(flowline, thickness))

# Set values
values = defaultdict(dict)
values['FL-1'][Parameters.Flowline.ROUGHNESS] = 1.0
values['FL-1'][Parameters.Flowline.WALLTHICKNESS] = 0.5
values['FL-1'][Parameters.Flowline.INNERDIAMETER] = 6.0
values['FL-2'][Parameters.Flowline.ROUGHNESS] = 2.0
values['FL-2'][Parameters.Flowline.WALLTHICKNESS] = 0.6
values['FL-2'][Parameters.Flowline.INNERDIAMETER] = 7.0
values['FL-3'][Parameters.Flowline.ROUGHNESS] = 3.0
values['FL-3'][Parameters.Flowline.WALLTHICKNESS] = 0.7
values['FL-3'][Parameters.Flowline.INNERDIAMETER] = 5.0
values['LL-1'][Parameters.Flowline.ROUGHNESS] = 2.0
values['LL-1'][Parameters.Flowline.WALLTHICKNESS] = 0.25
values['LL-1'][Parameters.Flowline.INNERDIAMETER] = 4.5

print("Set values from dictionary")
model.set_values(values)

# Check the roughness, thickness and innder diameter for all the flowline tubings
print("The current roughness, thickness and innder diameter of all the flowlines:")
new_values = model.get_values(component=ModelComponents.FLOWLINE, parameters=[Parameters.Flowline.ROUGHNESS, Parameters.Flowline.WALLTHICKNESS, Parameters.Flowline.INNERDIAMETER])
print(new_values)

# Check the roughness, thickness and innder diameter for all the flowline tubings showing units
print("The current roughness, thickness and innder diameter of all the flowlines with extra collon for unit symbol:")
new_values = model.get_values(show_units=True, component=ModelComponents.FLOWLINE, parameters=[Parameters.Flowline.ROUGHNESS, Parameters.Flowline.WALLTHICKNESS, Parameters.Flowline.INNERDIAMETER])
print(new_values)

# Close the model
print("Closing model...")
model.close()
