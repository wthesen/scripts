'''
    PIPESIM Python Toolkit
    Example: add and update flow control valve

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from utilities import open_model_from_case_study
from sixgill.definitions import ModelComponents, Parameters, Constants

import tempfile

# Open the model
model = open_model_from_case_study("./Tutorial Examples/TUT_9_Advanced Well FCV Final.pips")

print("\nAdding a Flow Control Valve(general valve) to the Well\n")
model.add(ModelComponents.FLOWCONTROLVALVE, "Fcv1", context="Well", \
         parameters={Parameters.FlowControlValve.USEGENERICMODE:True,
                            Parameters.FlowControlValve.SUBCRITICALCORRELATION:Constants.SubCriticalFlowCorrelation.MECHANISTIC,
                            Parameters.FlowControlValve.CALCULATECRITICALPRESSURERATIO:False,
                            Parameters.FlowControlValve.CRITICALPRESSURERATIO:0.53,
                            Parameters.FlowControlValve.LIQUIDFLOWCOEFFICIENT:0.67,
                            Parameters.FlowControlValve.GASFLOWCOEFFICIENT:0.67,
                            Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE:Constants.FlowControlValveMaxFlowRateType.LIQUIDFLOWRATE,
                            Parameters.FlowControlValve.MAXIMUMLIQUIDRATE:4000,
                            Parameters.FlowControlValve.TOPMEASUREDDEPTH:6000,
                            Parameters.FlowControlValve.SIZECALC:Constants.FlowControlValveSizeCalc.CHOKEAREA,
                            Parameters.FlowControlValve.CHOKEAREA:1.2})    

contextname = "Well:Fcv1"
print('Getting values for the flow control valve')
parameters = model.get_values(context=contextname, parameters=[Parameters.FlowControlValve.USEGENERICMODE,
                            Parameters.FlowControlValve.SUBCRITICALCORRELATION,
                            Parameters.FlowControlValve.CALCULATECRITICALPRESSURERATIO,
                            Parameters.FlowControlValve.CRITICALPRESSURERATIO,
                            Parameters.FlowControlValve.LIQUIDFLOWCOEFFICIENT,
                            Parameters.FlowControlValve.GASFLOWCOEFFICIENT,
                            Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE,
                            Parameters.FlowControlValve.MAXIMUMLIQUIDRATE,
                            Parameters.FlowControlValve.TOPMEASUREDDEPTH,
                            Parameters.FlowControlValve.SIZECALC,
                            Parameters.FlowControlValve.CHOKEAREA])
values_map = parameters[contextname]
for key, value in values_map.items():
    print(f'{key}: {value}')

#set liquidflowcoefficient,chokearea,maximumflowratetype and maximumgasrate  new value
print('\nSet new value for parameters: LIQUIDFLOWCOEFFICIENT,CHOKEAREA,MAXIMUMFLOWRATETYPE,MAXIMUMGASRATE')
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.LIQUIDFLOWCOEFFICIENT, value=0.83)
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.CHOKEAREA, value=0.82)
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE, value=Constants.FlowControlValveMaxFlowRateType.GASFLOWRATE)
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.MAXIMUMGASRATE, value=3000)

print('\nGetting LIQUIDFLOWCOEFFICIENT,CHOKEAREA,MAXIMUMFLOWRATETYPE,MAXIMUMGASRATE')
parameters = model.get_values(context=contextname,
                              parameters=[
                                  Parameters.FlowControlValve.LIQUIDFLOWCOEFFICIENT,
                                  Parameters.FlowControlValve.CHOKEAREA,
                                  Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE,
                                  Parameters.FlowControlValve.MAXIMUMGASRATE
                              ])

values_map = parameters[contextname]
for key, value in values_map.items():
    print(f'{key}: {value}')

print('\nSet new value for parameters: MAXIMUMFLOWRATETYPE,MAXIMUMWATERRATE')
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE, value=Constants.FlowControlValveMaxFlowRateType.WATERFLOWRATE)
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.MAXIMUMWATERRATE, value=30) 
print('\nGetting MAXIMUMFLOWRATETYPE,MAXIMUMWATERRATE')
parameters = model.get_values(context=contextname,
                              parameters=[
                                  Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE,
                                  Parameters.FlowControlValve.MAXIMUMWATERRATE
                              ])

values_map = parameters[contextname]
for key, value in values_map.items():
    print(f'{key}: {value}')


# Save and close the model
print("\nAll finished. Saving model...")
filename = tempfile.gettempdir() + "/ExercisingAddAndUpdateFcv.pips"
model.save(filename)
model.close()
