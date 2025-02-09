'''
    PIPESIM Python Toolkit
    Example: Running a nodal simulation
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
import os.path
from pprint import pprint
# Import the sixgill library and anything else we need
from sixgill.pipesim import Model
from sixgill.definitions import Parameters, Constants
from utilities import open_model_from_case_study

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")
print(model.about())


boundaries = {"Well:VertComp":{ Parameters.Boundary.PRESSURE:3500,
                                Parameters.Boundary.TEMPERATURE:200,
                                Parameters.Boundary.USEGASRATIO: Constants.GasRatioOption.GLR,
                                Parameters.Boundary.GLR: 20,
                                Parameters.Boundary.USEWATERRATIO: Constants.WaterRatioOption.WGR,
                                Parameters.Boundary.WGR: 20}
                    }


print("Setting inlet conditions")

model.tasks.nodalanalysis.set_conditions(producer="Well",inlet_conditions=boundaries)

print("Getting inlet conditions")
general_conditions,inlet_conditions = model.tasks.nodalanalysis.get_conditions(producer="Well")

#get_conditions returns a tuple. The second element of the tuple contains the inlet conditions
pprint("Inlet conditions = {}".format(inlet_conditions))

# Close the model
model.close()
