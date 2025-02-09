'''
    PIPESIM Python Toolkit
    Example: Capture elevation

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
from utilities import create_new_model

# Open the model
model = create_new_model("elevation.pips", overwrite=True)

print("Get elevation from a valid location: ")
lat = 30.123456789123456789
long = 30.123456789123456789
elevation = model.get_elevation(lat, long)
print("Elevation at ({0}, {1}) is {2}".format(lat, long, elevation))

print("Get the elevation from an invalid location will return NaN: ")
try:
    model.get_elevation(lat = 999, long = 999)
except ValueError as ex:
    print(ex)

# Close the model
print("Closing model...")
model.close()
