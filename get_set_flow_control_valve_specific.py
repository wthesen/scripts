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
from sixgill.definitions import ModelComponents, Parameters, ProfileVariables,Constants

import tempfile

# Open the model
model = open_model_from_case_study("./Tutorial Examples/TUT_9_Advanced Well FCV Final.pips")

print("\nAdding a Flow Control Valve(specific valve) to the Well\n")
model.add(ModelComponents.FLOWCONTROLVALVE, "Fcv1", context="Well", \
                parameters={Parameters.FlowControlValve.USEGENERICMODE:False,
                            Parameters.FlowControlValve.ValveCatalogData.MANUFACTURER:"Schlumberger",
                            Parameters.FlowControlValve.ValveCatalogData.MODEL:"HD-3500-001",
                            Parameters.FlowControlValve.SUBCRITICALCORRELATION:Constants.SubCriticalFlowCorrelation.MECHANISTIC,
                            Parameters.FlowControlValve.CALCULATECRITICALPRESSURERATIO:False,
                            Parameters.FlowControlValve.CRITICALPRESSURERATIO:0.53,
                            Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE:Constants.FlowControlValveMaxFlowRateType.LIQUIDFLOWRATE,
                            Parameters.FlowControlValve.MAXIMUMLIQUIDRATE:4000,
                            Parameters.FlowControlValve.TOPMEASUREDDEPTH:1500})    

contextname = "Well:Fcv1"

# read from catalog
model.read_catalog(context=contextname)
print('Getting values for the flow control valve')
parameters = model.get_values(context=contextname, parameters=[Parameters.FlowControlValve.USEGENERICMODE,
                            Parameters.FlowControlValve.ValveCatalogData.MANUFACTURER,
                            Parameters.FlowControlValve.ValveCatalogData.MODEL,
                            Parameters.FlowControlValve.SUBCRITICALCORRELATION,
                            Parameters.FlowControlValve.CALCULATECRITICALPRESSURERATIO,
                            Parameters.FlowControlValve.CRITICALPRESSURERATIO,
                            Parameters.FlowControlValve.MAXIMUMFLOWRATETYPE,
                            Parameters.FlowControlValve.MAXIMUMLIQUIDRATE,
                            Parameters.FlowControlValve.TOPMEASUREDDEPTH])
values_map = parameters[contextname]
for key, value in values_map.items():
    print(f'{key}: {value}')   

print('\nGetting value from default catalog')
parameters = model.get_values(context=contextname,
                              parameters=[
                                  Parameters.FlowControlValve.ValveCatalogData.MANUFACTURER,
                                  Parameters.FlowControlValve.ValveCatalogData.DIAMETER,
                                  Parameters.FlowControlValve.ValveCatalogData.MODEL,
                                  Parameters.FlowControlValve.ValveCatalogData.TYPE,
                                  Parameters.FlowControlValve.ValveCatalogData.POSITION
                              ])
values_map = parameters[contextname]
for key, value in values_map.items():
    print(f'{key}: {value}')   


print('\nSetting the flow control valve position')
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.ValveCatalogData.POSITION, value=6)
valve_position = model.get_value(context=contextname, parameter=Parameters.FlowControlValve.ValveCatalogData.POSITION)
openingarea = model.get_value(context=contextname, parameter=Parameters.FlowControlValve.ValveCoefficient.OPENINGAREA)
print(f'Position now:{valve_position}, opening area now:{openingarea}')


#set valve type
print('\nSet new value for valve Position')
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.ValveCatalogData.POSITION, value=7)
print('\nGetting valve position')
valvePosition = model.get_value(context=contextname,
                             parameter=Parameters.FlowControlValve.ValveCatalogData.POSITION)
print(f'Position now:{valvePosition}') 

#set valve type
print('\nSet new value for valve type')
model.set_value(context=contextname, parameter=Parameters.FlowControlValve.ValveCatalogData.TYPE, value='TRFC-HD-AI (Odin)')
print('\nGetting valve type')
valveType = model.get_value(context=contextname,
                             parameter=Parameters.FlowControlValve.ValveCatalogData.TYPE)
print(f'Valve type now:{valveType}') 

#set values array
print('\nSet new values for valve catalog')
valve_params = {
    contextname: {
        Parameters.FlowControlValve.ValveCatalogData.MANUFACTURER:"Test",
        Parameters.FlowControlValve.ValveCatalogData.MODEL:"HDM-4500-003",
        Parameters.FlowControlValve.ValveCatalogData.DIAMETER:4.5,
        Parameters.FlowControlValve.ValveCatalogData.TYPE:'TRFC-HDM',
        Parameters.FlowControlValve.ValveCatalogData.POSITION:'3',
    }
}

model.set_values(valve_params)
print('\nGetting values for valve catalog')
parameters = model.get_values(context=contextname,
                              parameters=[
                                  Parameters.FlowControlValve.ValveCatalogData.MANUFACTURER,
                                  Parameters.FlowControlValve.ValveCatalogData.DIAMETER,
                                  Parameters.FlowControlValve.ValveCatalogData.MODEL,
                                  Parameters.FlowControlValve.ValveCatalogData.TYPE,
                                  Parameters.FlowControlValve.ValveCatalogData.POSITION
                              ])
for key, value in parameters[contextname].items():
    print(f'{key}: {value}')
    
    

# Save and close the model
print("\nAll finished. Saving model...")
filename = tempfile.gettempdir() + "/ExercisingAddAndUpdateFcv.pips"
model.save(filename)
model.close()
