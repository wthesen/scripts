'''
    PIPESIM Python Toolkit
    Example: Create a new PIPESIM Model

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

# Create a new model
model = create_new_model("new workspace.pips", overwrite=True)

# Print the model details
print(model.about())

# Close the model
print("Closing model...")
model.close()
