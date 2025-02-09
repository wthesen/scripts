'''
    Pipesim Python Toolkit
    Example: Get and set completion test points

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

import pandas as pd
from utilities import open_model_from_case_study

# Import the sixgill library
from sixgill.pipesim import Model
from sixgill.definitions import Units, ModelComponents, Parameters, Constants

# Open the model
model = open_model_from_case_study("./Well Models/CSW_105_Horizontal Oil Well.pips", Units.SI)

# Query what completion and IPR models are being used
ipr = model.get_values(component=ModelComponents.COMPLETION, parameters=[Parameters.Completion.IPRMODEL])
print("The current IPR model is \n {}".format(ipr))

print("Changing the IPR model to Darcy")
#Make sure the "Fluid entry type" and "Geometry profile" are set correctly
model.set_value("Hor_Well:Completion", value=Constants.CompletionFluidEntry.SINGLEPOINT, parameter=Parameters.Completion.FLUIDENTRYTYPE)
model.set_value("Hor_Well:Completion", value=Constants.Orientation.VERTICAL, parameter=Parameters.Completion.GEOMETRYPROFILETYPE)
model.set_value("Hor_Well:Completion", value=ModelComponents.IPRDARCY, parameter=Parameters.Completion.IPRMODEL)

# And now check every completion in the model
completions = model.get_values(component=ModelComponents.COMPLETION)
print("The parameterization of the completions is \n {}".format(completions))


print("Changing the IPR model to TriLinear")
model.set_value("Hor_Well:Completion", value=Constants.CompletionFluidEntry.DISTRIBUTED, parameter=Parameters.Completion.FLUIDENTRYTYPE)
model.set_value("Hor_Well:Completion", value=Constants.Orientation.HORIZONTAL, parameter=Parameters.Completion.GEOMETRYPROFILETYPE)
model.set_value("Hor_Well:Completion", value=ModelComponents.IPRTRILINEAR, parameter=Parameters.Completion.IPRMODEL)

# And now check every completion in the model
completions = model.get_values(component=ModelComponents.COMPLETION)
print("The parameterization of the completions is \n {}".format(completions))

model.close()
