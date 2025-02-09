'''
    PIPESIM Python Toolkit
    Example: Setting nodal simulation conditions
'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from pprint import pprint
# Import the sixgill library and anything else we need

from sixgill.definitions import Parameters, Constants
from utilities import open_model_from_case_study

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")
print(model.about())

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
                                  Parameters.NodalAnalysisSimulation.SensitivityVariable.COMPONENT:"VertComp",
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

print("Setting conditions")

model.tasks.nodalanalysis.set_conditions(producer="Well",parameters=conditions)

print("Getting conditions")
general_conditions,inlet_conditions = model.tasks.nodalanalysis.get_conditions(producer="Well")

#get_conditions returns a tuple. The first element of the tuple contains the general conditions
pprint("conditions = {}".format(general_conditions))

# Close the model
model.close()
