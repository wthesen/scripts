'''
    Pipesim Python Toolkit
    Example: Get and set Annulus flow Parameters

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
from utilities import open_model_from_case_study, make_sure_model_has_no_issues

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

# Set annulus flow attributes
flowline = 'GL-1'
print("Set flow line '{}' to Annulus".format(flowline))
model.set_value(Flowline=flowline, parameter=Parameters.Flowline.ANNULUSFLOW, value=True)
model.set_value(Flowline=flowline, parameter=Parameters.Flowline.INNERPIPEOUTSIDEDIAMETER, value=2.0)
model.set_value(Flowline=flowline, parameter=Parameters.Flowline.OUTERPIPEINSIDEDIAMETER, value=4.0)
model.set_value(Flowline=flowline, parameter=Parameters.Flowline.OUTERPIPEWALLTHICKNESS, value=0.25)
model.set_value(Flowline=flowline, parameter=Parameters.Flowline.ROUGHNESS, value=0.0018)

# Get annulus flow attributes
annulusflow = model.get_value(context=flowline, parameter=Parameters.Flowline.ANNULUSFLOW)
innerpipeoutsidediameter = model.get_value(context=flowline, parameter=Parameters.Flowline.INNERPIPEOUTSIDEDIAMETER)
outerpipeinsidediameter = model.get_value(context=flowline, parameter=Parameters.Flowline.OUTERPIPEINSIDEDIAMETER)
outerpipewallthickness = model.get_value(context=flowline, parameter=Parameters.Flowline.OUTERPIPEWALLTHICKNESS)
roughness = model.get_value(context=flowline, parameter=Parameters.Flowline.ROUGHNESS)

print("Annulus flow: {}".format(annulusflow))
print("Inner pipe outside diameter: {}".format(innerpipeoutsidediameter))
print("Outer pipe inside diameter: {}".format(outerpipeinsidediameter))
print("Outer pipe wall thickness: {}".format(outerpipewallthickness))
print("Roughness: {}".format(roughness))

# Validate the model
make_sure_model_has_no_issues(model)

# Close the model
print("Closing model...")
model.close()
