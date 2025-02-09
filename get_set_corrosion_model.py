'''
    PIPESIM Python Toolkit
    Example: get/set corrosion properties

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
            Constants
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
model = open_model_from_case_study("./Network Models/CSN_310_Augusta GIS.pips")
print(model.about())

model_settings = model.sim_settings

#############################
#  Dewaard corrosion model  #
#############################

print('')
print('Dewaard corrosion model:')
print(model_settings.corrosion_model_dewaard)

#set corrosion  values for dewaard
model_settings.corrosion_model_dewaard.corrosion_efficiency = 2.5
model_settings.corrosion_model_dewaard.calculate_ph = True
model_settings.corrosion_model_dewaard.PH = 12.5

print('')
print('Dewaard corrosion model changed:')
print(model_settings.corrosion_model_dewaard)

print('')
print('Setting the corrosion model to dewaard')
model_settings.corrosion_model = Constants.CorrosionModels.DEWAARD1995

#########################
#  Tpa corrosion model  #
#########################

print('')
print('Tpa corrosion model:')
print(model_settings.corrosion_model_tpa)

#set corrosion values for tpa
model_settings.corrosion_model_tpa.oxygen_or_bacteria_exists = False
model_settings.corrosion_model_tpa.pre_existing_corrosion_damage = False
model_settings.corrosion_model_tpa.black_powder_or_debris_exists = False
model_settings.corrosion_model_tpa.pipe_deployment_year = 1998
model_settings.corrosion_model_tpa.corrosion_assessment_year = 2001

print('')
print('Tpa corrosion model changed:')
print(model_settings.corrosion_model_tpa)

print('')
print('Setting the corrosion model to tpa')
model_settings.corrosion_model = Constants.CorrosionModels.TPA

#run simulation and get the erosion/corrosion risk values
profile_variables = [
            ProfileVariables.CORROSION_RISK,
            ProfileVariables.EROSION_RISK,
            ProfileVariables.CORROSION_CUMULATIVE_LOSS,
            ProfileVariables.CORROSION_PIT_RATE,
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

if ProfileVariables.CORROSION_PIT_RATE in results.profile[case_1]:
    corrosion_pit_rate = results.profile[case_1][ProfileVariables.CORROSION_PIT_RATE]
    print('Corrosion pit rate for case:{}:{}'.format(case_1, corrosion_pit_rate))
    

if ProfileVariables.CORROSION_CUMULATIVE_LOSS in results.profile[case_1]:
    corrosion_cum_loss = results.profile[case_1][ProfileVariables.CORROSION_CUMULATIVE_LOSS]
    print('Corrosion cumulative loss for case:{}:{}'.format(case_1, corrosion_cum_loss))


model.close()
