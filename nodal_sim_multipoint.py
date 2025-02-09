'''
    PIPESIM Python Toolkit
    Example: Running a nodal simulation with multipoint
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

from sixgill.definitions import Parameters, SystemVariables, ProfileVariables, \
                                    Constants, ModelComponents
from utilities import open_model_from_case_study

import pandas as pd

# Open the model
model = open_model_from_case_study("./Well Models/CSW_131_IPO_SC_GL_Design.pips")
print(model.about())

system_variables = [
    SystemVariables.PRESSURE, SystemVariables.TEMPERATURE,
    SystemVariables.VOLUME_FLOWRATE_LIQUID_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_OIL_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_WATER_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_GAS_STOCKTANK,
    SystemVariables.GOR_STOCKTANK, SystemVariables.WATER_CUT_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_GAS_STOCKTANK,
    SystemVariables.WATER_CUT_INSITU,
    SystemVariables.WELLHEAD_VOLUME_FLOWRATE_FLUID_INSITU,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_GAS_STOCKTANK,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_OIL_STOCKTANK,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_WATER_STOCKTANK,
    SystemVariables.SYSTEM_OUTLET_TEMPERATURE,
    SystemVariables.BOTTOM_HOLE_PRESSURE, SystemVariables.OUTLET_GLR_STOCKTANK,
    SystemVariables.OUTLET_WATER_CUT_STOCKTANK,
    SystemVariables.TOTAL_INJECTION_GAS,
    SystemVariables.CASING_HEAD_PRESSURE,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_LIQUID_INSITU
]

diagnostics_variables = [
        SystemVariables.GAS_LIFT_DIAGNOSTICS_PORT_DIAMETER,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_POSITION_STATUS,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_DOME_TEMPERATURE,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_GAS_RATE_NO_THROTTLING,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_STATUS,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_CLOSING_PRESSURE,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_OPENING_PRESSURE,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_PTRO,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_DISCHARGE_COEFFICIENT,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_PORT_TO_BELLOW_AREA,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_OPERATION_MODE,
        SystemVariables.GAS_LIFT_DIAGNOSTICS_PORT_TYPE
        ]

profile_variables = [
    ProfileVariables.TEMPERATURE, ProfileVariables.PRESSURE,
    ProfileVariables.ELEVATION, ProfileVariables.TOTAL_DISTANCE
]



# set the multipointing options on the well
well_params = {
    "Well": {
        Parameters.Well.ISMULTIPOINTING: True,
        Parameters.Well.DIAGNOSTICSTYPE:
        Constants.DiagnosticsType.FIXEDPRESSURE,
        Parameters.Well.THROTTLINGOPTION: Constants.ThrottlingType.ON,
        Parameters.Well.PRESSUREGRADIENTTYPE:
        Constants.PressureGradientType.INCLUDEFRICTIONLOSSES,
        Parameters.Well.SURFACEGASPRESSURE: 1750,
        Parameters.Well.SURFACEGASTEMPERATURE: 116,
    }
}

conditions = {Parameters.NodalAnalysisSimulation.LIMITINFLOW: False,
                          Parameters.NodalAnalysisSimulation.LIMITOUTFLOW: True,
                          Parameters.NodalAnalysisSimulation.OUTFLOWPOINTS: 40,
                          Parameters.NodalAnalysisSimulation.INFLOWPOINTS: 50,
                          Parameters.NodalAnalysisSimulation.MAXFLOWRATETYPE: Constants.FlowRateType.LIQUIDFLOWRATE,
                          Parameters.NodalAnalysisSimulation.MAXLIQUIDRATE: 30000,
                          Parameters.NodalAnalysisSimulation.MAXOUTFLOWPRESSURE: 3000,
                          Parameters.NodalAnalysisSimulation.OUTLETPRESSURE: 600,
                          Parameters.NodalAnalysisSimulation.MAXGASRATE: 300,
                          Parameters.NodalAnalysisSimulation.USEPHASERATIO: True
}

model.set_values(well_params)

# now get the values to make sure they have been set correctly
well_list = model.find(context="Well", component=ModelComponents.WELL)
params = [
    Parameters.Well.ISMULTIPOINTING, Parameters.Well.DIAGNOSTICSTYPE,
    Parameters.Well.THROTTLINGOPTION, Parameters.Well.PRESSUREGRADIENTTYPE,
    Parameters.Well.SURFACEGASPRESSURE, Parameters.Well.SURFACEGASTEMPERATURE
]
well_context = well_list[0]
well_values = model.get_values(context=well_context, parameters=params)
first_key = list(well_values.keys())[0]
well_values_dictionary = well_values[first_key]
print(well_values_dictionary)

# Run the simulation and print out the results
print("Running nodal simulation with multipointing")

#Add the diagnostics variables
for variable in diagnostics_variables:
    system_variables.append(variable)
    
results = model.tasks.nodalanalysis.run(
    producer="Well",
    parameters=conditions,
    system_variables=system_variables,
    profile_variables=profile_variables)

#generate result table like the one on PIPESIM UI:
#system results
system_df = pd.DataFrame.from_dict(results.system, orient="index")
system_df.index.name = "Variable"
print("System result = {}".format(system_df))

print("Cases = {}".format(results.cases))

    
# Diagnostics results
print('')
print('')
print('Diagnostics results')
print('-------------------')
for case, equipm_res in results.node.items():
     print("\nDiagnostics results for {}".format(case))
     for equip_variable in diagnostics_variables:
         print("Equipment variable {}\n".format(equip_variable))
         for equip_key in equipm_res[equip_variable]:
             print("Name {}".format(equip_key))
             print("Value {}".format(equipm_res[equip_variable][equip_key]))

print('-------------------')

#profile results
print('')
print('')
print('Profile results')
print('-------------------')
for case, profile in results.profile.items():
    print("\nProfile result for {}".format(case))
    profile_df = pd.DataFrame.from_dict(profile)
    print(profile_df)

print('-------------------')
# Close the model
model.close()
