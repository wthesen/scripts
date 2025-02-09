'''
    PIPESIM Python Toolkit
    Example: Opening and saving a PIPESIM Model File

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
from utilities import open_model_from_case_study, save_model

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Print the model details
print(model.about())

save_model(model, "NewModelFile.pips")

filename = model.filename

print("Closing model...")
model.close()

print("Opening model...")
model = Model.open(filename)

print("Saving model...")
model.save()

# Close the model
print("Closing model...")
model.close()
