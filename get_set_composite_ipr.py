'''
    Pipesim Python Toolkit
    Example: Get and set Composite IPR attibutes

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
from sixgill.definitions import Parameters, Constants
from utilities import open_model_from_case_study, make_sure_model_has_no_issues

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Set Composite IPR attributes
model.set_value(Well = "Well", Completion = "VertComp", parameter=Parameters.Completion.IPRMODEL, value=Constants.IPRModels.IPRPIMODEL)
model.set_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.ISGASMODEL, value="False")
model.set_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.LIQUIDPI, value=0.1)
model.set_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.USEVOGELBELOWBUBBLEPOINT, value="True")
model.set_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.USEVOGELWATERCUTCORRECTION, value="True")

# Get attributes
completionmodel = model.get_value(Well = "Well", Completion = "VertComp", parameter=Parameters.Completion.IPRMODEL)
gasmodel = model.get_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.ISGASMODEL)
liquidpi = model.get_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.LIQUIDPI)
usevogelbelowbubblepoint = model.get_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.USEVOGELBELOWBUBBLEPOINT)
usevogelwatercutcorrection = model.get_value(Well = "Well", Completion = "VertComp", parameter=Parameters.IPRPIModel.USEVOGELWATERCUTCORRECTION)

print("Completion model: {}".format(completionmodel))
print("gas model: {}".format(gasmodel))
print("Liquid PI model: {}".format(liquidpi))
print("Use Vogel below bubble point: {}".format(usevogelbelowbubblepoint))
print("Use Vogel water cut correction: {}".format(usevogelwatercutcorrection))

# Validate the model
make_sure_model_has_no_issues(model)

# Close the model
print("Closing model...")
model.close()

