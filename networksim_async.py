'''
    PIPESIM Python Toolkit
    Example: Running a network simulation asynchronously
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
from sixgill.definitions import Units, OutputVariables, SimulationState
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")
print(model.about())

#start the simulation
print("Starting network simulation")
simulation_id = model.tasks.networksimulation.start(profile_variables=OutputVariables.Profile.FLOW_ASSURANCE,
                                                    system_variables=OutputVariables.System.FLOW_ASSURANCE)
print(simulation_id)

try:
    #check the simulation status
    sim_state = model.tasks.networksimulation.get_state(simulation_id)
    import time
    while sim_state == SimulationState.RUNNING:
        print ("Simulation is running...")
        time.sleep(1)
        sim_state = model.tasks.networksimulation.get_state(simulation_id)

    print ("Simulation run status: " + sim_state)
    sim_messages = model.tasks.networksimulation.get_messages(simulation_id)
    for m in sim_messages:
        print (m)

    #get the simulation results
    results = model.tasks.networksimulation.get_results(simulation_id)

    #system results
    system_df = pd.DataFrame.from_dict(results.system, orient="index")
    system_df.index.name = "Variable"
    print ("System result = {}".format(system_df))

    #node results
    node_df = pd.DataFrame.from_dict(results.node, orient="index")
    node_df.index.name = "Variable"
    print ("\nNode result = {}".format(node_df))

    for branch, profile in results.profile.items():
        print ("\nProfile result for {}".format(branch))
        profile_df = pd.DataFrame.from_dict(profile)
        print (profile_df)

finally:
    #always remember to delete the simulation, otherwise, the resource will not be released.
    model.tasks.networksimulation.delete_results(simulation_id)

model.close()
