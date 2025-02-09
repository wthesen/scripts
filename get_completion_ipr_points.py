'''
    PIPESIM Python Toolkit
    Example: Get completion ipr points

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
from utilities import open_model_from_case_study
from sixgill.definitions import ModelComponents, Parameters, Constants


# Open the model
model = open_model_from_case_study("./Well Models/CSW_141_Vert Multilayer Producer.pips")

# Uppler_Layer Completion
print("Getting upper layer completion ipr points for Well_1")
results = model.get_completion_ipr_points(context='Well_1:Upper_Layer')
print("Well completion ipr points of Upper_Layer completion in Well_1 :\n {}".format(results.ipr_points))

#Change the completion to a distributed one, where there is no ipr calculation available
model.set_value(Well = "Well_1", Completion = "Upper_Layer", parameter=Parameters.Completion.IPRMODEL, value=Constants.IPRModels.IPRHORIZONTALPI)


results = model.get_completion_ipr_points(context='Well_1:Upper_Layer')
print("Well completion ipr points of Upper_Layer completion in Well_1 :\n {}".format(results.ipr_points))
print("Ipr calculation messages:")
for msg in results.messages:
    print(msg)


# Close the model
print("Closing model...")
model.close()
