'''
    PIPESIM Python Toolkit
    Example: get/set erosion corrosion risk limits

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

import os.path

# Import the sixgill library and anything else we need
from sixgill.pipesim import Model
from sixgill.definitions import Parameters, SystemVariables, ProfileVariables, \
            Constants, EspCurvesVariables
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
model = open_model_from_case_study("./Network Models/CSN_310_Augusta GIS.pips")
print(model.about())

model_settings = model.sim_settings

print('')
print('Erosion risk limits:')
print(model_settings.erosion_limits)
print('')
print('Corrosion risk limits tpa:')
print(model_settings.corrosion_model_tpa.corrosion_limits)
print('')
print('Corrosion risk limits dewaard:')
print(model_settings.corrosion_model_dewaard.corrosion_limits)

#set erosion risk values
model_settings.erosion_limits.negligible = 0.02
model_settings.erosion_limits.low = 0.5
model_settings.erosion_limits.moderate = 0.9
model_settings.erosion_limits.high = 0.95

#set corrosion risk values for dewaard
dewaard_model = model_settings.corrosion_model_dewaard
dewaard_risk_limits = dewaard_model.corrosion_limits
dewaard_model.corrosion_limits.negligible = 0.0403694
dewaard_risk_limits.low = 4.93694
#direct calling should work too
model_settings.corrosion_model_dewaard.corrosion_limits.moderate = 40.3694
model_settings.corrosion_model_dewaard.corrosion_limits.high = 192.847

#set corrosion risk values for tpa
model_settings.corrosion_model_tpa.corrosion_limits.negligible = 0.003694
model_settings.corrosion_model_tpa.corrosion_limits.low = 0.12
model_settings.corrosion_model_tpa.corrosion_limits.moderate = 0.9
model_settings.corrosion_model_tpa.corrosion_limits.high = 4.2


print('')
print('Erosion risk limits:')
print(model_settings.erosion_limits)

print('')
print('Corrosion risk limits tpa:')
print(model_settings.corrosion_model_tpa.corrosion_limits)

print('')
print('Corrosion risk limits dewaard:')
print(model_settings.corrosion_model_dewaard.corrosion_limits)


print('')
print('Setting the corrosion model to dewaard')
model_settings.corrosion_model = Constants.CorrosionModels.DEWAARD1995

#run simulation and get the erosopn/corrosion risk values
profile_variables = [
            ProfileVariables.CORROSION_RISK,
            ProfileVariables.EROSION_RISK
]

system_variables = [
    SystemVariables.MAXIMUM_CORROSION_RISK,
    SystemVariables.MAXIMUM_EROSION_RISK
]

parameters = {Parameters.PTProfileSimulation.OUTLETPRESSURE:200}
              
                   

results = model.tasks.ptprofilesimulation.run(
    producer="Well_12",
    study='Study 1 - Reservoir Conditions',
    parameters = parameters,
    profile_variables=profile_variables,
    system_variables=system_variables)

# System results
system_df = pd.DataFrame.from_dict(results.system, orient="index")
system_df.index.name = "Variable"
print("State {}".format(results.state))
print ("System result = {}".format(system_df))


# Profile results
for case, profile in results.profile.items():
    print ("\nProfile result for {}".format(case))
    profile_df = pd.DataFrame.from_dict(profile)
    print (profile_df)
    
#Directly get erosion/corrosion risk values:
case_1 = results.cases[0]
max_erosion_risk_1 = results.system[SystemVariables.MAXIMUM_EROSION_RISK][case_1]
print('Max erosion limit for case:{}:{}'.format(case_1,max_erosion_risk_1))

erosion_risk_1 = results.profile[case_1][ProfileVariables.EROSION_RISK]
corrosion_risk_1 = results.profile[case_1][ProfileVariables.CORROSION_RISK]
print('Erosion risk for case:{}:{}'.format(case_1, erosion_risk_1))
print('Corrosion risk for case:{}:{}'.format(case_1, corrosion_risk_1))


model.close()
