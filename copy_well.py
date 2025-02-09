'''
    PIPESIM Python Toolkit
    Example: Copy an existing well

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from sixgill.pipesim import Model
from utilities import open_model_from_case_study, save_model


# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

model.copy('Well', 'Sixgill')

print(model.find(Well='Sixgill'))

save_model(model, "copy_well.pips")


model.close()
