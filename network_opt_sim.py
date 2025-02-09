'''
    PIPESIM Python Toolkit
    Example: Running a network optimizer simulation
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
from sixgill.pipesim import Model
from utilities import open_model_from_case_study
from pprint import pprint

# Open the model
model = open_model_from_case_study("./Network Models/CSN_312_Gas Lift Optimization.pips")
print(model.about())

print("Running network optimization")
results =  model.tasks.networkoptimizersimulation.run()

print("Simulation state = {}".format(results.state))

print("Simulation console messages:")
print(results.messages)
print("Simulation summary:")
print(results.summary)

print("available result variables:")
for key, var_name in results.variable_names.items():
    print("variable:{} {}".format(results.variable_names[key], results.units[key]))

print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
print("WELL RESULTS:")
for well_name, well_results in results.well_results.items():
    print("Well:{}".format(well_name))
    for var_name, value in well_results.items():
        print(" {}                                          :{}".format(var_name, value))

print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
print("FLOWLINE RESULTS:")
for name, flowline_results in results.flowline_results.items():
    print("FLOWLINE:{}".format(name))
    for var_name, value in flowline_results.items():
        print(" {}                                          :{}".format(var_name, value))

print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
print("SINK RESULTS:")
for name, sink_results in results.sink_results.items():
    print("SINK:{}".format(name))
    for var_name, value in sink_results.items():
        print(" {}                                          :{}".format(var_name, value))

model.close()
