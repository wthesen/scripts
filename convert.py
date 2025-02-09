'''
    PIPESIM Python Toolkit
    Example: Convert junction

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
from sixgill.definitions import ModelComponents
from pandas import DataFrame
from utilities import open_model, save_model

# Open the model
model = open_model("./models/CSN_301_Small Network_Connection.pips")

# Convert to Well
name = 'Manifold'
to_component = ModelComponents.WELL
model.convert(context=name, to_component=to_component)
print("The junction {} is converted to {}".format(name, to_component))

# Convert to Source
name = 'J'
to_component = ModelComponents.SOURCE
model.convert(context=name, to_component=to_component)
print("The junction {} is converted to {}".format(name, to_component))
# Find the converted item in model
print(model.find(context=name, component=ModelComponents.SOURCE))

# Convert to Sink
name = 'J 1'
to_component = ModelComponents.SINK
model.convert(context=name, to_component=to_component)
print("The junction {} is converted to {}".format(name, to_component))
# Find the converted item in model
print(model.find(context=name, component=ModelComponents.SINK))

# Cannot convert Junction with two connections
name = 'J 2'
to_component = ModelComponents.SINK
try:
    model.convert(context=name, to_component=to_component)
except ValueError as ex:
    print("The junction {} cannot be converted to {} due to the following error {}".format(name, to_component, ex))

save_model(model, "CSN_301_Small Network_Connection.pips")

# Close the model
print("Closing model...")
model.close()
