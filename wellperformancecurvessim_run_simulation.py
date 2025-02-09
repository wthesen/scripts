
'''
    PIPESIM Python Toolkit
    Example: Running a Well Performance Curves simulation
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
from sixgill.definitions import Parameters, SystemVariables, \
                                Constants
from utilities import open_model_from_case_study
import pandas as pd
import os.path
import tempfile

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")
print(model.about())

parameters = {Parameters.WellPerformanceCurvesSimulation.BRANCHTERMINATOR:"FL-2",
              Parameters.WellPerformanceCurvesSimulation.FLOWRATEPOINTS: 50,
              Parameters.WellPerformanceCurvesSimulation.SENSITIVITYVARIABLES:
             [
                 {
                     Parameters.WellPerformanceCurvesSimulation.SensitivityVariable.COMPONENT:"FL-2",
                     Parameters.WellPerformanceCurvesSimulation.SensitivityVariable.VARIABLE:Parameters.Flowline.INNERDIAMETER,
                     Parameters.WellPerformanceCurvesSimulation.SensitivityVariable.VALUES:[4,5,6] #in
                 },
             ],              
            }

system_variables = [
    SystemVariables.WELL_CURVE_PERFORMANCE_PWI,
    SystemVariables.SYSTEM_PRESSURE_LOSS,
    SystemVariables.SYSTEM_TEMPERATURE_DIFFERENCE,
    SystemVariables.PRESSURE,
    SystemVariables.TEMPERATURE
    ]
model.tasks.wellperformancecurvessimulation.set_conditions(producer="Well", study = "Study 1", parameters = parameters)


print("Running Well Performance Curves simulation")
results = model.tasks.wellperformancecurvessimulation.run(producer="Well",parameters=parameters,system_variables=system_variables)

# Get PWI File content from simulation results
pwi=[]
for key in results.system[SystemVariables.WELL_CURVE_PERFORMANCE_PWI].keys():
    if not key == 'Unit':
        pwi.append(results.system[SystemVariables.WELL_CURVE_PERFORMANCE_PWI][key])
pwi_content = pwi[0]

# Save PWI file to temporary folder
tmp = tempfile.NamedTemporaryFile(delete=False)
pwi_filename = tmp.name + ".pwi"
print("Saving PWI File to: \n{0}".format(pwi_filename))
with open(pwi_filename, 'w') as file:
    file.write(pwi_content.replace("\n", "")) 

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

model.close()
