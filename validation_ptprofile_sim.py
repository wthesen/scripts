'''
    PIPESIM Python Toolkit
    Example: Validating a pt profile simulation
'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

# Import the sixgill library and anything else we need
from sixgill.pipesim import Model
from sixgill.definitions import SystemVariables, ProfileVariables, ModelComponents, Parameters, NAN, Constants
from utilities import open_model
import pandas as pd


def invalidate_conditions(model):
    conditions = {Parameters.PTProfileSimulation.OUTLETPRESSURE: -30000}
    model.tasks.ptprofilesimulation.set_conditions(producer="Well2 - Oil", study = "Study 1", parameters = conditions)

def add_invalid_well(model):
    model.add(ModelComponents.WELL, "Well invalid", parameters = {Parameters.Well.AMBIENTTEMPERATURE:60})

def print_issues(issues, title):
    print('-----------{}----------------'.format(title))
    counter = 1
    for issue in issues:
        print("Issue {}".format(counter))
        print("Path: {}".format(issue.path))
        print("Message: {}".format(issue.message))
        print("Property: {}".format(issue.property_name))
        counter = counter + 1

def make_sure_model_has_no_issues(model):
     
    conditions = {Parameters.PTProfileSimulation.OUTLETPRESSURE: 250}
    model.tasks.ptprofilesimulation.set_conditions(producer="Well2 - Oil", study = "Study 1", parameters = conditions)
    #Get validation issues
    issues = model.tasks.ptprofilesimulation.validate(producer="Well2 - Oil")
    if len(issues) > 0:
        raise RuntimeError("Model has validation issues") 

def invalid_boundary_condition_generates_error(model):
    invalidate_conditions(model)
    #Get validation issues
    issues = model.tasks.ptprofilesimulation.validate(producer="Well2 - Oil")
    if len(issues) != 1:
        raise RuntimeError("Model failed to catch boundary condition issues") 
    print_issues(issues, 'invalid_boundary_condition_generates_error')

def invalid_well_condition_generates_error(model):
    invalidate_conditions(model)
    add_invalid_well(model)
    #Get validation issues
    issues = model.tasks.ptprofilesimulation.validate(producer="Well2 - Oil")
    if len(issues) != 2:
        raise RuntimeError("Model failed to catch boundary condition/Well issues") 
    print_issues(issues,'invalid_well_condition_generates_error')

# Open the model
model = open_model("./models/Nodal_example.pips")
print(model.about())

print("Validating network simulation")
#First make sure the model has no validation issues
make_sure_model_has_no_issues(model)

#Now set a bad value for one of the boundary conditions and catch the issue
invalid_boundary_condition_generates_error(model)

#Add a well that is invalid and expect the issues to be displayed
invalid_well_condition_generates_error(model)

model.close()
