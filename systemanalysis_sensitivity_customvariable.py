'''
    PIPESIM Python Toolkit
    Example: Running a system analysis
    
    Attention.
    Matplotlib library must be installed manually to successfully proceed 
    with this example.
'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file and matplotlib are not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

matplotlib_spec=importlib.util.find_spec("matplotlib")
if matplotlib_spec is None:
    sys.exit("The script has been terminated. Matplotlib library must be installed manually to successfully proceed with this example")

from collections import defaultdict
import pandas as pd
from sixgill.pipesim import Model
from sixgill.definitions import Parameters, SystemVariables, ProfileVariables, Constants
import math
import tempfile
from typing import Optional
from sixgill.simulation_result import SimulationResult
from math import isclose
import matplotlib.pyplot as plt
from utilities import open_model_from_case_study


def get_matched_cases(results:SimulationResult, variables: Optional[dict] = None):
    matched_cases =  []
    for case in results.cases:
        matched = True
        for variable in variables:
            if not isclose(results.system[variable][case], variables[variable], rel_tol=0.01):
                matched = False
                print(results.system[variable][case])
                break;
        if matched:
            matched_cases.append(case)
    return matched_cases


def _prepare_system_variables():
        variables = [
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
        SystemVariables.OUTLET_VOLUME_FLOWRATE_LIQUID_STOCKTANK,
        SystemVariables.SYSTEM_OUTLET_TEMPERATURE,
        SystemVariables.BOTTOM_HOLE_PRESSURE,
        SystemVariables.OUTLET_GLR_STOCKTANK,
        SystemVariables.OUTLET_WATER_CUT_STOCKTANK
        ]
        return variables

def _prepare_profile_variables():
        variables = [
            ProfileVariables.TEMPERATURE,
            ProfileVariables.ELEVATION,
            ProfileVariables.TOTAL_DISTANCE,
            ProfileVariables.PRESSURE
        ]
        return variables

# Open the model
model = open_model_from_case_study("./Well Models/CSW_135_Multilayer_Well_GL_Design.pips")

#we have thre sens values in X and two in var1. type is "StepWithZ". We expect to get two cases only
parameters = {Parameters.SystemAnalysisSimulation.INLETPRESSURE:2765,
        Parameters.SystemAnalysisSimulation.OUTLETPRESSURE:200,
        Parameters.SystemAnalysisSimulation.FLOWRATETYPE:Constants.FlowRateType.LIQUIDFLOWRATE,
        Parameters.SystemAnalysisSimulation.LIQUIDFLOWRATE:1500,
        Parameters.SystemAnalysisSimulation.SENSITIVITYMETHOD:Constants.SensitivityMethod.STEPWITHXAXIS,
        Parameters.SystemAnalysisSimulation.CALCULATEDVARIABLE:Constants.CalculatedVariable.CUSTOM ,
        Parameters.SystemAnalysisSimulation.CUSTOMVARIABLE: {
        Parameters.SystemAnalysisSimulation.CustomVariable.COMPONENT: "Upper",
        Parameters.SystemAnalysisSimulation.CustomVariable.VARIABLE: Parameters.IPRPIModel.LIQUIDPI,
        Parameters.SystemAnalysisSimulation.CustomVariable.MINVALUE: 1,
        Parameters.SystemAnalysisSimulation.CustomVariable.MAXVALUE: 10,
        Parameters.SystemAnalysisSimulation.CustomVariable.ISDIRECTPROPORTIONALITY: True
        },

    Parameters.SystemAnalysisSimulation.SENSITIVITYVARIABLES:
    [
        {
            Parameters.SystemAnalysisSimulation.SensitivityVariable.COMPONENT:"System Data",
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VARIABLE:Parameters.SystemAnalysisSimulation.LIQUIDFLOWRATE,
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VALUES:[1800,1620,1650]
        },
        {
            Parameters.SystemAnalysisSimulation.SensitivityVariable.COMPONENT:"Upper",
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VARIABLE:Parameters.Completion.WATERCUT,
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VALUES:[50,50,55]
        },
        {
            Parameters.SystemAnalysisSimulation.SensitivityVariable.COMPONENT:"Gas lift data",
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VARIABLE:Parameters.Well.TARGETINJECTIONRATE,
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VALUES:[3,2.5,1.5]
        },
        {
            Parameters.SystemAnalysisSimulation.SensitivityVariable.COMPONENT:"Upper",
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VARIABLE:Parameters.Completion.GOR,
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VALUES:[3500, 3000, 2500]
        },
        {
            Parameters.SystemAnalysisSimulation.SensitivityVariable.COMPONENT:"System Data",
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VARIABLE:Parameters.SystemAnalysisSimulation.OUTLETPRESSURE,
            Parameters.SystemAnalysisSimulation.SensitivityVariable.VALUES:[350, 250, 100]
        },
    ],
    }

model.tasks.systemanalysissimulation.set_conditions("Well",parameters)

results = model.tasks.systemanalysissimulation.run("Well", system_variables=_prepare_system_variables(), profile_variables=_prepare_profile_variables())

pd.DataFrame(results.cases) # print out all cases and system results
pd.DataFrame(results.system)


# compare simulation results- Oil rate for all the cases
# get calibrated PI based on order
PI=[]
for case in results.cases:
    PI.append(results.system['Upper-LiquidPI'][case])
    print(case)

# get calibrated PI on certain well test input
WellTest=[]
PI_2=[]
WellTest.append( {"System Data-" + Parameters.SystemAnalysisSimulation.LIQUIDFLOWRATE:1800})
WellTest.append({"System Data-" + Parameters.SystemAnalysisSimulation.LIQUIDFLOWRATE:1620})
WellTest.append({"System Data-" + Parameters.SystemAnalysisSimulation.LIQUIDFLOWRATE:1650})

for i in range(len(WellTest)):
    #import pdb; pdb.set_trace()
    WellTest_Case=get_matched_cases(results, WellTest[i])
    PI_2.append(results.system['Upper-LiquidPI'][WellTest_Case[0]])


# Plot PI vs WellTest date
WT_Days=[30,61,91]
fig = plt.figure(1, figsize=(12,8))
xs, ys = zip(*sorted(zip( WT_Days, PI)))
plt.plot(xs, ys, 'b')
plt.scatter(WT_Days, PI, s=150, c='b', label='Caculated PI')
plt.legend(loc=1)
fig.suptitle('Calibrated PI with Well Test Data', fontsize=18)
plt.xlabel('Days of the Year 2018', fontsize=14)
plt.ylabel('PI (STB/(d*psi))', fontsize=14)

fig = plt.figure(2, figsize=(12,8))
xs, ys = zip(*sorted(zip( WT_Days, PI_2)))
plt.plot(xs, ys, 'b')
plt.scatter(WT_Days, PI_2, s=150, c='b', label='Caculated PI')
plt.legend(loc=1)
fig.suptitle('Calibrated PI with Well Test Data', fontsize=18)
plt.xlabel('Days of the Year 2018', fontsize=14)
plt.ylabel('PI (STB/(d*psi))', fontsize=14)

if len(sys.argv) == 1:
    plt.show()

    filename = tempfile.gettempdir() + "/ModifiedModelFile_SystemAnalysis2.pips"
    print("Saving model as..." + filename)
    model.save(filename)

model.close()
