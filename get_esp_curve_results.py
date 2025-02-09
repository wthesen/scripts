'''
    PIPESIM Python Toolkit
    Example: Getting ESP pump curve results by Running PT Profile and Nodal analysis simulations
'''

import os.path

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

# Import the sixgill library and anything else we need
from sixgill.pipesim import Model
from sixgill.definitions import Parameters, SystemVariables, ProfileVariables, \
            Constants, EspCurvesVariables
from utilities import open_model_from_case_study


print("Running example file '{}'".format(__file__))

def print_results(esp_curve_results, pump_name):
    for case_name, esp_results in esp_curve_results.items():
        unit = esp_results[pump_name][EspCurvesVariables.INPUTS][EspCurvesVariables.FREQUENCY][
            EspCurvesVariables.UNIT]
        print("FREQUENCY:{} {}".format(
            esp_results[pump_name][EspCurvesVariables.INPUTS][EspCurvesVariables.FREQUENCY][
                EspCurvesVariables.VALUE], unit))
        print("MANUFACTURER:{}".format(esp_results[pump_name][EspCurvesVariables.INPUTS][
            EspCurvesVariables.MANUFACTURER][EspCurvesVariables.VALUE]))
        print("MODEL:{}".format(esp_results[pump_name][EspCurvesVariables.INPUTS][
            EspCurvesVariables.MODEL][EspCurvesVariables.VALUE]))
        minFlow = esp_results[pump_name][EspCurvesVariables.INPUTS][EspCurvesVariables.MINFLOWRATE][
            EspCurvesVariables.VALUE]
        maxFlow = esp_results[pump_name][EspCurvesVariables.INPUTS][EspCurvesVariables.MAXFLOWRATE][
            EspCurvesVariables.VALUE]
        print("MAXFLOWRATE:{}".format(maxFlow))
        print("MINFLOWRATE:{}".format(minFlow))
        print("STAGES:{}".format(esp_results[pump_name][EspCurvesVariables.INPUTS][
            EspCurvesVariables.STAGES][EspCurvesVariables.VALUE]))
        rate = esp_results[pump_name][EspCurvesVariables.INPUTS][EspCurvesVariables.FLOWRATE][
            EspCurvesVariables.VALUE]
        print("Flowrate:{}".format(rate))

        #Print frequency curves
        for freq_name, speed_curve_xy in esp_results[pump_name][
                EspCurvesVariables.VARIABLESPEEDCURVE][
                    EspCurvesVariables.FREQUENCIES].items():
            print("FREQUENCY: {}".format(freq_name))
            for name, curve in speed_curve_xy.items():
                print("{} Values:{}".format(name,
                                            curve[EspCurvesVariables.VALUES]))

        #Print QMin, BEP. QMax curves
        for freq_name, freq_curve in esp_results[pump_name][
                EspCurvesVariables.VARIABLESPEEDCURVE][
                    EspCurvesVariables.OPERATINGENVELOPE].items():
            print("{} flowrate Values:{}".format(freq_name,
                                        freq_curve[EspCurvesVariables.FLOWRATE][EspCurvesVariables.VALUES]))
            print("{} pressure Values:{}".format(freq_name,
                                        freq_curve[EspCurvesVariables.FLOWRATE][EspCurvesVariables.VALUES]))


# Open the model
model = open_model_from_case_study("./Well Models/CSW_124_Dual ESP Well.pips")
print(model.about())

system_variables = [
    SystemVariables.PRESSURE,
    SystemVariables.TEMPERATURE,
]

profile_variables = [
    ProfileVariables.TEMPERATURE,
    ProfileVariables.PRESSURE,
    ProfileVariables.ELEVATION,
    ProfileVariables.TOTAL_DISTANCE,
]

# Run the simulation and print out the results
print("Running PT profile simulation")
results = model.tasks.ptprofilesimulation.run(
    producer="Well_1",
    profile_variables=profile_variables,
    system_variables=system_variables)

esp_curve_results = results.esp_curves

print_results(esp_curve_results, "B-ESP")

print("Running Nodal analysis simulation")
results = model.tasks.nodalanalysis.run(producer="Well_1",
                                        profile_variables=profile_variables,
                                        system_variables=system_variables)

esp_curve_results = results.esp_curves

print_results(esp_curve_results, 'B-ESP')

# Close the model
model.close()
