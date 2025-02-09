'''
    PIPESIM Python Toolkit
    Example: Running a nodal simulation with sensitivities
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

# Import the sixgill library and anything else we need
from sixgill.definitions import Parameters, OutputVariables, SystemVariables, ProfileVariables, \
            Constants
from utilities import open_model, open_model_from_case_study

# Open the model
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")
print(model.about())


well_name = "Well_1"
completion_name = "Completion"

conditions = {Parameters.NodalAnalysisSimulation.LIMITINFLOW: False,
                          Parameters.NodalAnalysisSimulation.LIMITOUTFLOW: True,
                          Parameters.NodalAnalysisSimulation.OUTFLOWPOINTS: 30,
                          Parameters.NodalAnalysisSimulation.INFLOWPOINTS: 30,
                          Parameters.NodalAnalysisSimulation.MAXFLOWRATETYPE: Constants.FlowRateType.LIQUIDFLOWRATE,
                          Parameters.NodalAnalysisSimulation.OUTLETPRESSURE: 300,
                          Parameters.NodalAnalysisSimulation.USEPHASERATIO: False,
                          Parameters.NodalAnalysisSimulation.SENSITIVITYVARIABLES:
                          [
                             
                              {
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.COMPONENT:completion_name,
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.VARIABLE:Parameters.Completion.RESERVOIRPRESSURE,
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.VALUES:[3000,4000], #psia
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.TYPE:Constants.SensitivityVariableType.INFLOW
                              },
                              {
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.COMPONENT:"Tubing",
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.VARIABLE:Parameters.Tubing.INNERDIAMETER,
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.VALUES:[3.2,3.4], #in
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.TYPE:Constants.SensitivityVariableType.OUTFLOW
                              },
                          ],

            }

boundaries = {"{}:{}".format(well_name, completion_name):{ Parameters.Boundary.PRESSURE:2500,
                                Parameters.Boundary.TEMPERATURE:200 }
                    }

nodal_point_settings = {
                         Parameters.NodalPoint.NODALTYPE: Constants.NodalPointType.DOWNHOLE,
                         Parameters.NodalPoint.DEPTH: 9817,
                         Parameters.NodalPoint.WELLSTRINGTYPE: Constants.TubingSectionType.CASING,
                         Parameters.NodalPoint.NAME: 'NodalPoint'}

# Run the simulation 
print("Running nodal simulation")

results = model.tasks.nodalanalysis.run(producer=well_name, parameters=conditions,nodal_point_settings=nodal_point_settings,
                                        inlet_conditions=boundaries,
                                        system_variables=OutputVariables.System.WELL_PERFORMANCE, 
                                        profile_variables=OutputVariables.Profile.WELL_PERFORMANCE)


#system results
system_df = pd.DataFrame.from_dict(results.system, orient="index")
system_df.index.name = "Variable"
print("State {}".format(results.state))
print ("System result = {}".format(system_df))

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

# Close the model
model.close()
