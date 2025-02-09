'''
    PIPESIM Python Toolkit
    Example: Running a network optimizer simulation and apply the results
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
from utilities import get_case_study_path
from sixgill.definitions import Parameters

# Open the model
full_path = get_case_study_path("./Network Models/CSN_312_Gas Lift Optimization.pips")
model = Model.open(full_path, in_memory_results=False)
print(model.about())

print("Running network optimization")
results =  model.tasks.networkoptimizersimulation.run()

print("Simulation state = {}".format(results.state))


# First, change the values
gas_rate = model.get_value(context="Well_1:Tubing_Gas lift injection", parameter=Parameters.GasLiftInjection.GASRATE)
print('Well_1:Tubing_Gas lift injection gas rate is now:{}'.format(gas_rate))

print('Setting the gas rate for Well_1:Tubing_Gas lift injection to: 0.66')
model.set_value(context="Well_1:Tubing_Gas lift injection", parameter=Parameters.GasLiftInjection.GASRATE, value=0.66)

gas_rate = model.get_value(context="Well_1:Tubing_Gas lift injection", parameter=Parameters.GasLiftInjection.GASRATE)
print('Well_1:Tubing_Gas lift injection gas rate is now:{}'.format(gas_rate))

#Apply the optimization results to the model
print('Applying optimization results to the model')
model.tasks.networkoptimizersimulation.apply_results()

gas_rate = model.get_value(context="Well_1:Tubing_Gas lift injection", parameter=Parameters.GasLiftInjection.GASRATE)
print('Well_1:Tubing_Gas lift injection gas rate after applying results is:{}'.format(gas_rate))

model.close()
