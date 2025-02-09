
'''
    PIPESIM Python Toolkit
    Example: Running a Gas Lift Diagnostics simulation
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
import pandas as pd

# Open the model
model = open_model_from_case_study("./Well Models/CSW_136_GL_Design_FlowlineRiser.pips")
print(model.about())

profile_variables = [
            ProfileVariables.TEMPERATURE,
            ProfileVariables.PRESSURE,
            ProfileVariables.TOTAL_DISTANCE,
]

parameters = {
    Parameters.GLDiagnosticsSimulation.OUTLETPRESSURE:600,  #psia
    Parameters.GLDiagnosticsSimulation.DIAGNOSTICSTYPE:Constants.GasLift.DiagnosticsOperationDiagnostics.FIXEDINJECTION,
    Parameters.GLDiagnosticsSimulation.THROTTLING:Constants.GasLift.DiagnosticsOperationThrottling.ON,
    Parameters.GLDiagnosticsSimulation.INJECTIONGRADIENT:Constants.GasLift.PressureGradient.STATIC,
    Parameters.GLDiagnosticsSimulation.TARGETINJECTIONRATE:2.85,
    Parameters.GLDiagnosticsSimulation.SURFACEINJECTIONTEMPERATURE:116,
    Parameters.GLDiagnosticsSimulation.PRODUCER:"Well",
    Parameters.GLDiagnosticsSimulation.SENSITIVITYVARIABLE:   {
         Parameters.GLDiagnosticsSimulation.SensitivityVariable.COMPONENT:"Completion",
         Parameters.GLDiagnosticsSimulation.SensitivityVariable.VARIABLE:Parameters.Completion.RESERVOIRPRESSURE,
         Parameters.GLDiagnosticsSimulation.SensitivityVariable.VALUES:[2000,3000,4000] #
    }
}

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

model.tasks.gldiagnosticssimulation.set_conditions("Well", parameters)
# Run the simulation and print out the results
print("Running Gas lift diagnostics simulation")
results = model.tasks.gldiagnosticssimulation.run(producer="Well",
                               parameters=parameters,
                               system_variables=diagnostics_variables,
                               profile_variables=profile_variables)


# System results
system_df = pd.DataFrame.from_dict(results.system, orient="index")
system_df.index.name = "Variable"
print("State {}".format(results.state))
print ("System result = {}".format(system_df))

# Node results
for case, node_res in results.node.items():
    print ("\nNode result for {}".format(case))
    node_df = pd.DataFrame.from_dict(node_res, orient="index")
    node_df.index.name = "Variable"
    print (node_df)

# Diagnostics results
for case, equipm_res in results.node.items():
     print("\nDiagnostics results for {}".format(case))
     for equip_variable in diagnostics_variables:
         print("Equipment variable {}\n".format(equip_variable))
         for equip_key in equipm_res[equip_variable]:
             print("Name {}".format(equip_key))
             print("Value {}".format(equipm_res[equip_variable][equip_key]))

# Profile results
for case, profile in results.profile.items():
    print ("\nProfile result for {}".format(case))
    profile_df = pd.DataFrame.from_dict(profile)
    print (profile_df)

model.close()
