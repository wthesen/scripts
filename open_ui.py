'''
    PIPESIM Python Toolkit
    Example: Opening PIPESIM model in UI

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
from utilities import get_case_study_path, open_model_from_case_study, save_model

# Open the model directly
filename = get_case_study_path("./Network Models/CSN_301_Small Network.pips")
print("Opening model in UI '{}'".format(filename))
Model.open_ui(filename)

# Open a model first and saved it to temp folder
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")

save_model(model, "CSW_101_Basic Oil Well.pips")

# reopen the saved model and open it in UI
print("Opening {} in the UI will save the model and close it".format(model.filename))
model.open_ui()
print("Again, note that the model is not open anymore: 'model.is_open' returns '{}'".format(str(model.is_open)))

model.close()
