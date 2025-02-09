'''
    PIPESIM Python Toolkit
    Example: Setting the study conditions and running a simulation
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
from sixgill.definitions import Parameters, SystemVariables, ProfileVariables, \
                                    Constants, NAN
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
print("Opening model to set the study conditions")
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")
print(model.about())

system_variables = [
    SystemVariables.PRESSURE,
    SystemVariables.TEMPERATURE,
    SystemVariables.VOLUME_FLOWRATE_LIQUID_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_OIL_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_WATER_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_GAS_STOCKTANK,
    SystemVariables.GOR_STOCKTANK,
    SystemVariables.WATER_CUT_STOCKTANK,
    SystemVariables.WATER_CUT_INSITU,
    SystemVariables.WELLHEAD_VOLUME_FLOWRATE_FLUID_INSITU,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_GAS_STOCKTANK,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_OIL_STOCKTANK,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_WATER_STOCKTANK,
    SystemVariables.SYSTEM_OUTLET_TEMPERATURE,
    SystemVariables.BOTTOM_HOLE_PRESSURE,
    SystemVariables.OUTLET_GLR_STOCKTANK,
    SystemVariables.OUTLET_WATER_CUT_STOCKTANK,
]

profile_variables = [
    ProfileVariables.TEMPERATURE,
    ProfileVariables.ELEVATION,
    ProfileVariables.TOTAL_DISTANCE,
]

# Check out what the existing study conditions are
# Without arguments it returns the Network Simulation, Study 1
study_conditions = model.tasks.networksimulation.get_conditions(study="Study 1")
print("The current conditions are:\n{}".format(study_conditions))

# Set the new study conditions
boundaries = {"Well:VertComp": {
                    Parameters.Boundary.PRESSURE:NAN,
                    Parameters.Boundary.TEMPERATURE:150,
                    Parameters.Boundary.FLOWRATETYPE:Constants.FlowRateType.LIQUIDFLOWRATE,
                    Parameters.Boundary.LIQUIDFLOWRATE:200
                    }
            }
             
model.tasks.networksimulation.set_conditions(boundaries = boundaries, study="Study 1")
new_study_conditions = model.tasks.networksimulation.get_conditions()
print("The new conditions are:\n{}".format(new_study_conditions))

# Run the simulation. It defaults to the Network Simulation, Study 1
print("Running the simulation with the new conditions.")
results = model.tasks.networksimulation.run(system_variables=system_variables, profile_variables=profile_variables)

# Close the model
model.close()
