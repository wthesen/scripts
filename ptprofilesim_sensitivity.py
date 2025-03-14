'''
    PIPESIM Python Toolkit
    Example: Running a PT Profile simulation
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
                                    Constants
from utilities import open_model_from_case_study
from collections import defaultdict
import pandas as pd

# Open the model
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
            SystemVariables.VOLUME_FLOWRATE_GAS_STOCKTANK,
            SystemVariables.WATER_CUT_INSITU,
            SystemVariables.WELLHEAD_VOLUME_FLOWRATE_FLUID_INSITU,
            SystemVariables.OUTLET_VOLUME_FLOWRATE_GAS_STOCKTANK,
            SystemVariables.OUTLET_VOLUME_FLOWRATE_OIL_STOCKTANK,
            SystemVariables.OUTLET_VOLUME_FLOWRATE_WATER_STOCKTANK,
            SystemVariables.SYSTEM_OUTLET_TEMPERATURE,
            SystemVariables.BOTTOM_HOLE_PRESSURE,
            SystemVariables.OUTLET_GLR_STOCKTANK,
            SystemVariables.OUTLET_WATER_CUT_STOCKTANK
]

profile_variables = [
            ProfileVariables.TEMPERATURE,
            ProfileVariables.PRESSURE,
            ProfileVariables.ELEVATION,
            ProfileVariables.TOTAL_DISTANCE
]

parameters = {
    Parameters.PTProfileSimulation.INLETPRESSURE:2600,  #psia
    Parameters.PTProfileSimulation.OUTLETPRESSURE:200,  #psia
    Parameters.PTProfileSimulation.CALCULATEDVARIABLE:Constants.CalculatedVariable.FLOWRATE,
    Parameters.SystemAnalysisSimulation.BRANCHTERMINATOR:"Manifold",
    Parameters.PTProfileSimulation.FLOWRATETYPE:Constants.FlowRateType.LIQUIDFLOWRATE,
    Parameters.PTProfileSimulation.SENSITIVITYVARIABLE:{
        Parameters.PTProfileSimulation.SensitivityVariable.COMPONENT:"VertComp",
        Parameters.PTProfileSimulation.SensitivityVariable.VARIABLE:"ReservoirPressure",
        Parameters.PTProfileSimulation.SensitivityVariable.VALUES:[2000,3000,4000] #psia
        }
    }

# Out of curiosity, find out what sensitivity variables that we could run
sens_vars = model.tasks.ptprofilesimulation.get_sensitivity_variables("Well")
print('The available sensivity variables for well "Well" are:')
for k,v in sens_vars.items():
    print(k,v)

# Run the simulation and print out the results
print("Running PT profile simulation")
results = model.tasks.ptprofilesimulation.run(producer="Well",
                               parameters=parameters,
                               system_variables=system_variables,
                               profile_variables=profile_variables)

#generate result table like the one on PIPESIM UI:
#system results
system_df = pd.DataFrame.from_dict(results.system, orient="index")
system_df.index.name = "Variable"
print ("System result = {}".format(system_df))

print ("Cases = {}".format(results.cases))

#node results
for case, node_res in results.node.items():
    print ("\nNode result for {}".format(case))
    node_df = pd.DataFrame.from_dict(node_res, orient="index")
    node_df.index.name = "Variable"
    print (node_df)

#profile results
for case, profile in results.profile.items():
    print ("\nProfile result for {}".format(case))
    profile_df = pd.DataFrame.from_dict(profile)
    print (profile_df)

# node pressure for each case
choke_outlet_pressure = [results.node[case]['Pressure']['Choke'] for case in results.cases]
print('pressure = {}'.format(choke_outlet_pressure))

# Close the model
model.close()
