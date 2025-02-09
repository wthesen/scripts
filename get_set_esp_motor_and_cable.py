'''
    PIPESIM Python Toolkit
    Example: Update esp motor and cable values

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
from sixgill.definitions import ModelComponents, Parameters, SystemVariables, ProfileVariables

import tempfile

# Open the model
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")

print("\nAdding an ESP to Well_1\n")
model.add(ModelComponents.ESP, "Esp1", context="Well_1", \
         parameters={Parameters.ESP.TOPMEASUREDDEPTH:8370,
                     Parameters.ESP.OPERATINGFREQUENCY:80,
                     Parameters.ESP.MANUFACTURER:"ALNAS",
                     Parameters.ESP.MODEL:"ANA580",
                     Parameters.ESP.NUMBERSTAGES:100,
                     Parameters.ESP.HEADFACTOR:1,
                     Parameters.ESP.POWERFACTOR:0.95,
                     Parameters.ESP.USEVISCOSITYCORRECTION:True,
                     Parameters.ESP.MotorCatalogData.MANUFACTURER:"M",
                     Parameters.ESP.MotorCatalogData.MOTORNAME:"M2",
                     Parameters.ESP.MotorCoefficients.AMPValues:[1, 2, 3], #ampValues for the first three coeffiecients
                     Parameters.ESP.MotorCoefficients.PFValues:[0.1],      #pfValue for the first coefficient
                     Parameters.ESP.MotorCoefficients.EFFValues:[0.7, 2]   #effValues for the first two coefficients
                     },
                     )

print('Setting the effValue for the first motor coefficient\n')

model.set_value(context="Well_1:Esp1",
                parameter=Parameters.ESP.MotorCoefficients.EFFValues,
                value=[0.05])

print('Using model.set_values to set effValues and operating frequency\n')
esp_motor_params = {
    "Well_1:Esp1": {
        Parameters.ESP.MotorCoefficients.EFFValues: [1, 2.5],
        Parameters.ESP.OPERATINGFREQUENCY: 90
    }
}

model.set_values(esp_motor_params)

print('Getting all values for the ESP (including motor, motor coefficients and cable)')
parameters = model.get_values(context="Well_1:Esp1")
values_map = parameters["Well_1:Esp1"]
for key, value in values_map.items():
    print('{}: {}'.format(key, value))

print('\nGetting head factor and motor name')
parameters = model.get_values(context="Well_1:Esp1",
                              parameters=[
                                  Parameters.ESP.HEADFACTOR,
                                  Parameters.ESP.MotorCatalogData.MOTORNAME
                              ])
print(parameters)

print('\nGetting head factor and ampValues')
parameters = model.get_values(context="Well_1:Esp1",
                              parameters=[
                                  Parameters.ESP.HEADFACTOR,
                                  Parameters.ESP.MotorCoefficients.AMPValues
                              ])
print(parameters)

print('\nGetting head factor, effValues, maxamps')
parameters = model.get_values(context="Well_1:Esp1",
                              parameters=[
                                  Parameters.ESP.HEADFACTOR,
                                  Parameters.ESP.MotorCoefficients.EFFValues,
                                  Parameters.ESP.CableCatalogData.MAXAMPS
                              ])
print(parameters)

print('\nGetting head factor')
parameters = model.get_value(context="Well_1:Esp1",
                             parameter=Parameters.ESP.HEADFACTOR)
print(parameters)

print('\nGetting maxamp')
parameters = model.get_value(context="Well_1:Esp1",
                             parameter=Parameters.ESP.CableCatalogData.MAXAMPS)
print(parameters)

print('\nGetting ampValues')
parameters = model.get_value(
    context="Well_1:Esp1",
    parameter=Parameters.ESP.MotorCoefficients.AMPValues)
print(parameters)

print('\nGetting motor name')
parameters = model.get_value(
    context="Well_1:Esp1", parameter=Parameters.ESP.MotorCatalogData.MOTORNAME)
print(parameters)

#Now add some reasonable values for motor and cable and run a simulation
esp_motor_params = {
    "Well_1:Esp1": {
        Parameters.ESP.MotorCoefficients.EFFValues:[-0.0155, 1.5982, -2.3615, 4.3328, -3.7083, 1.1501],
        Parameters.ESP.MotorCoefficients.EFFValues:[-0.0357, 3.6761, -7.9931, 9.8977, -6.4203, 1.6615],
        Parameters.ESP.MotorCoefficients.PFValues:[0.1608, 0.9299, -0.9556, 1.7459, -1.7823, 0.6141],
        Parameters.ESP.MotorCatalogData.MOTORNAME:"ESP STD",
        Parameters.ESP.MotorCatalogData.NPPOWER:2000,
        Parameters.ESP.MotorCatalogData.NPAMPERAGE:15,
        Parameters.ESP.MotorCatalogData.NPVOLTAGE:435,
        Parameters.ESP.MotorCatalogData.FLOOREFFICIENCY:1,
        Parameters.ESP.MotorCatalogData.FLOORPOWERFACTOR:1,
        Parameters.ESP.CableCatalogData.NAME:"#3/0 Cu",
        Parameters.ESP.CableCatalogData.VDROP:0.11,
        Parameters.ESP.CableCatalogData.MAXAMPS:166,
        Parameters.ESP.CABLELENGTHBELOWPUMP:True,
        Parameters.ESP.POWERCORRECTION:True,
        Parameters.ESP.ISPOWERCORRECTIONCALCULATED:True,
    }
}

model.set_values(esp_motor_params)

#run the pt profile simulation
sys_variables = [
    SystemVariables.PRESSURE_DIFFERENCE,  # dp
    SystemVariables.POWER,  #total power
    SystemVariables.SURFACEPOWER,  #Surface power
    SystemVariables.OUTLET_PRESSURE,  #Pout
    SystemVariables.MOTOR_LOAD,
    SystemVariables.MOTOR_EFFICIENCY,
    SystemVariables.MOTOR_CURRENT,
    SystemVariables.MOTOR_VOLTAGE,
    SystemVariables.MOTOR_POWER_FACTOR,
    SystemVariables.CABLE_VOLTAGE_DROP
]

profile_variables = [
    ProfileVariables.TEMPERATURE,
    ProfileVariables.ELEVATION,
    ProfileVariables.TOTAL_DISTANCE,
]

print("\nRunning PT/Profile simulation...")
results = model.tasks.ptprofilesimulation.run(
    producer="Well_1",
    system_variables=sys_variables,
    profile_variables=profile_variables,
    study="Study 1")

case = results.cases[0]
node = results.node[case]

def _print_result(node, system_variable, variable_display_name):
    value = node[system_variable]["Esp1"]
    unit = node[system_variable]["Unit"]
    print("{0}: {1} {2}".format(variable_display_name, value, unit))

print()
_print_result(node, SystemVariables.SURFACEPOWER, "Surface power")

print("\nESP motor results")
_print_result(node, SystemVariables.MOTOR_LOAD, "Motor load")
_print_result(node, SystemVariables.MOTOR_EFFICIENCY, "Motor efficiency")
_print_result(node, SystemVariables.MOTOR_CURRENT, "Motor current")
_print_result(node, SystemVariables.MOTOR_VOLTAGE, "Motor voltage")
_print_result(node, SystemVariables.MOTOR_POWER_FACTOR, "Motor power factor")
_print_result(node, SystemVariables.CABLE_VOLTAGE_DROP, "Cable voltage drop")

# Save and close the model
print("\nAll finished. Saving model...")
filename = tempfile.gettempdir() + "/ExercisingAddAndUpdateEspMotor.pips"
model.save(filename)
model.close()
