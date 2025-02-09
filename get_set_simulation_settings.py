'''
    PIPESIM Python Toolkit
    Example: Get and set simulation settings

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

# Import the sixgill library
from sixgill.pipesim import Model
from sixgill.definitions import Parameters
from utilities import open_model_from_case_study

import tempfile
import os.path

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

sim_settings = model.sim_settings

#print the current simulation settings
for k, v in sim_settings.items():
    print ( "{} = {}".format(k, v))

#set the ambient temperature:
sim_settings[Parameters.SimulationSetting.AMBIENTTEMPERATURE] = 65  #degF

#get the ambient temperature:
ambient_temperature = sim_settings[Parameters.SimulationSetting.AMBIENTTEMPERATURE]
print ("{} = {}".format(Parameters.SimulationSetting.AMBIENTTEMPERATURE, ambient_temperature))

#another way of setting and getting ambient temperature
sim_settings.ambient_temperature = 70   #degF
print ("{} = {}".format(Parameters.SimulationSetting.AMBIENTTEMPERATURE, sim_settings.ambient_temperature))

#setting and getting UseGlobalFlowCorrelations flag
sim_settings[Parameters.SimulationSetting.USEGLOBALFLOWCORRELATIONS] = True
print ("{} = {}".format(Parameters.SimulationSetting.USEGLOBALFLOWCORRELATIONS, sim_settings[Parameters.SimulationSetting.USEGLOBALFLOWCORRELATIONS]))

filename = tempfile.gettempdir() + "/TestSimulationSettings.pips"
print("Saving model as..." + filename)
model.save(filename)

model.close()
