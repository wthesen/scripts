'''
    PIPESIM Python Toolkit
    Example: Review a model with different components and parameters

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
from sixgill.definitions import OutputVariables, Parameters, Constants, \
                                ModelComponents, ALL, NONE, NAN
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
model = open_model_from_case_study("./Network Models/CSN_307_Onshore PI Facility.pips")

params = model.get_values(Name=ALL)
print("The model components are\n {}".format(params.keys()))

print("Running a network simulation with Well Performance output variables")
results = model.tasks.networksimulation.run(
                            profile_variables=OutputVariables.Profile.WELL_PERFORMANCE,
                            system_variables=OutputVariables.System.WELL_PERFORMANCE
                            )

# System variable results
print("System Results")
system_df = pd.DataFrame.from_dict(results.system, orient="index")
print(system_df)

# Node results
print("Node Results")
node_df = pd.DataFrame.from_dict(results.node, orient="index")
print(node_df)

# Profile results
for branch, profile in results.profile.items():
    print ("\nProfile result for {}".format(branch))
    profile_df = pd.DataFrame.from_dict(profile)
    print (profile_df)

# Close the model
print("Closing model...")
model.close()
