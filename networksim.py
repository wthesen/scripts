'''
    PIPESIM Python Toolkit
    Example: Running a network simulation
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
from sixgill.definitions import SystemVariables, ProfileVariables, Constants
from utilities import open_model_from_case_study
import pandas as pd
import os.path

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
            SystemVariables.OUTLET_WATER_CUT_STOCKTANK,
            SystemVariables.EROSIONAL_VELOCITY_MAXIMUM,
]

profile_variables = [
            ProfileVariables.TEMPERATURE,
            ProfileVariables.ELEVATION,
            ProfileVariables.TOTAL_DISTANCE,
]
profile_variables_shear_stress = [
            ProfileVariables.GAS_WALL_SHEAR_STRESS,
            ProfileVariables.OIL_WALL_SHEAR_STRESS,
            ProfileVariables.WATER_WALL_SHEAR_STRESS,
            ProfileVariables.LIQUID_WALL_SHEAR_STRESS,
]

def change_to_olga(model):
    model.sim_settings.global_flow_correlation.horizontal_correlation = Constants.MultiphaseFlowCorrelation.OLGAS.OLGASV731_3PHASE
    model.sim_settings.global_flow_correlation.horizontal_source = Constants.MultiphaseFlowCorrelationSource.OLGAS
    
    model.sim_settings.global_flow_correlation.vertical_correlation = Constants.MultiphaseFlowCorrelation.OLGAS.OLGASV731_3PHASE
    model.sim_settings.global_flow_correlation.vertical_source = Constants.MultiphaseFlowCorrelationSource.OLGAS

def print_results(results):
    print("Simulation state = {}".format(results.state))

    print("Simulation console messages:")
    print(results.messages)
    print("Simulation summary:")
    print(results.summary)
    
    #generate result table like the one on PIPESIM UI:
    #system results
    system_df = pd.DataFrame.from_dict(results.system, orient="index")
    system_df.index.name = "Variable"
    print ("System result = {}".format(system_df))
    
    #node results
    node_df = pd.DataFrame.from_dict(results.node, orient="index")
    node_df.index.name = "Variable"
    print ("\nNode result = {}".format(node_df))
    
    #profile results
    for branch, profile in results.profile.items():
        print ("\nProfile result for {}".format(branch))
        profile_df = pd.DataFrame.from_dict(profile)
        print (profile_df)
    
print("Running network simulation")
results =  model.tasks.networksimulation.run(system_variables=system_variables, profile_variables=profile_variables)
print_results(results)

print("Running network simulation using OLGAS correlations")
change_to_olga(model)
results =  model.tasks.networksimulation.run(system_variables=system_variables, profile_variables=profile_variables_shear_stress)
print_results(results)

model.close()

