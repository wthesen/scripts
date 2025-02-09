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
from sixgill.definitions import Parameters
from utilities import create_new_model

# Open the model
model = create_new_model("elevations.pips", overwrite=True)

print("Get elevations from a valid location: ")
location = [{Parameters.Location.LATITUDE:30, Parameters.Location.LONGITUDE:30},
            {Parameters.Location.LATITUDE:31, Parameters.Location.LONGITUDE:31}]
locations = model.get_elevations(location)

print("Elevation at ({0}, {1}) is {2}".format(locations[0][Parameters.Location.LATITUDE], locations[0][Parameters.Location.LONGITUDE], locations[0][Parameters.Location.ELEVATION]))
print("Elevation at ({0}, {1}) is {2}".format(locations[1][Parameters.Location.LATITUDE], locations[1][Parameters.Location.LONGITUDE], locations[1][Parameters.Location.ELEVATION]))


print("Get elevations with invalid location: ")
location = [{Parameters.Location.LATITUDE:30, Parameters.Location.LONGITUDE:30},
            {Parameters.Location.LATITUDE:31, Parameters.Location.LONGITUDE:31},
            {Parameters.Location.LATITUDE:999, Parameters.Location.LONGITUDE:999}]

try:
    model.get_elevations(location)
except ValueError as ex:
    print(ex)

# Close the model
print("Closing model...")
model.close()
