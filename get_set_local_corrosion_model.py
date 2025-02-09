'''
    PIPESIM Python Toolkit
    Example: get/set local corrosion properties

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
from sixgill.definitions import DEFAULT, ModelComponents, Parameters, Constants
from utilities import open_model_from_case_study

from sixgill.core.dewaard import to_dewaard
from sixgill.core.Tpa import to_tpa


# Open the model
model = open_model_from_case_study("./Network Models/CSN_310_Augusta GIS.pips")
print(model.about())

model_settings = model.sim_settings

#############################
#  Dewaard corrosion model  #
#############################

print('')
print('Dewaard corrosion model:')

# Set and get use_global_corrosion_model flag
model_settings.use_global_corrosion_model = False
print ("{} = {}".format(Parameters.SimulationSetting.USEGLOBALCORROSIONMODEL, model_settings.use_global_corrosion_model))

# Set the corrosion model to DeWaard
model_settings.corrosion_model = Constants.CorrosionModels.DEWAARD1995
print ("{} = {}".format('Corrosion model is now:', model_settings.corrosion_model))

# Set some values for all the wells
corrosion_models = model_settings.get_corrosion_models(component=ModelComponents.WELL)
for name, corrosion_model in corrosion_models.items():
    dewaard = to_dewaard(corrosion_model)
    dewaard.corrosion_efficiency = 2.5
    dewaard.calculate_ph = False
    dewaard.PH = 1.23    

    print('Corrosion settings for: {}'.format(name))
    print(dewaard)
    print('')

# Use a dictionary to assign multiple values at once
corrosion_date = {
    DEFAULT:{Parameters.DeWaardCorrosionModel.EFFICIENCY:2.0},
    'Well_1':{Parameters.DeWaardCorrosionModel.EFFICIENCY:2.1},
    'Well_2':{Parameters.DeWaardCorrosionModel.CALCULATEPH:False,Parameters.DeWaardCorrosionModel.PHVALUE:1.24},
}
model_settings.set_corrosion_models(corrosion_date)

# Set the override corrosion to false for Well_1
model.set_value(context='Well_1', component=ModelComponents.WELL, parameter=Parameters.Well.OVERRIDECORROSION, value=False)

#Set some values for flowline "FL-1"
corrosion_models = model_settings.get_corrosion_models(context='FL-1', component=ModelComponents.FLOWLINE)
for name, corrosion_model in corrosion_models.items():
    dewaard = to_dewaard(corrosion_model)
    dewaard.corrosion_efficiency = 1.24
    dewaard.calculate_ph = False
    dewaard.PH = 0.02
    
    print('Corrosion settings for: {}'.format(name))
    print(dewaard)
    print('')

#############################
#  Tpa corrosion model      #
#############################

# Switch to TPA
model_settings.corrosion_model = Constants.CorrosionModels.TPA

corrosion_date = {
    DEFAULT:{Parameters.TpaCorrosionModel.PIPEDEPLOYMENTYEAR:2002}
}
model_settings.set_corrosion_models(corrosion_date)

# Set some values for all the wells
corrosion_models = model_settings.get_corrosion_models(component=ModelComponents.WELL)
for name, corrosion_model in corrosion_models.items():
    tpa = to_tpa(corrosion_model)
    tpa.pipe_deployment_year = 2001
    tpa.corrosion_assessment_year = 2015
    tpa.oxygen_or_bacteria_exists = False
    tpa.pre_existing_corrosion_damage = False
    tpa.black_powder_or_debris_exists = False

    print('Corrosion settings for: {}'.format(name))
    print(tpa)
    print('')
    
# Set some values for flowline "FL-1"
corrosion_models = model_settings.get_corrosion_models(context='FL-1', component=ModelComponents.FLOWLINE)
for name, corrosion_model in corrosion_models.items():
    tpa = to_tpa(corrosion_model)
    tpa.pipe_deployment_year = 2000
    tpa.corrosion_assessment_year = 2016
    tpa.oxygen_or_bacteria_exists = False
    tpa.pre_existing_corrosion_damage = False
    tpa.black_powder_or_debris_exists = False
    
    print('Corrosion settings for: {}'.format(name))
    print(tpa)
    print('')

# Turn off corrosion calculation
model_settings.corrosion_model = Constants.CorrosionModels.NONE

model.close()
