'''
    PIPESIM Python Toolkit
    Example: Setting the study conditions and running a simulation
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
from sixgill.definitions import Parameters, SystemVariables, ProfileVariables, \
                                    Constants, NAN
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
print("Opening model to set the study conditions")
model = open_model_from_case_study("./Network Models/CSN_303_Looped Network.pips")
print(model.about())

system_variables = [
    SystemVariables.PRESSURE,
    SystemVariables.TEMPERATURE,
    SystemVariables.VOLUME_FLOWRATE_LIQUID_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_OIL_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_WATER_STOCKTANK,
    SystemVariables.VOLUME_FLOWRATE_GAS_STOCKTANK,
    SystemVariables.GOR_STOCKTANK,
    SystemVariables.WATER_CUT_STOCKTANK,
    SystemVariables.WATER_CUT_INSITU,
    SystemVariables.WELLHEAD_VOLUME_FLOWRATE_FLUID_INSITU,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_GAS_STOCKTANK,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_OIL_STOCKTANK,
    SystemVariables.OUTLET_VOLUME_FLOWRATE_WATER_STOCKTANK,
    SystemVariables.SYSTEM_OUTLET_TEMPERATURE,
    SystemVariables.BOTTOM_HOLE_PRESSURE,
    SystemVariables.OUTLET_GLR_STOCKTANK,
    SystemVariables.OUTLET_WATER_CUT_STOCKTANK,
]

profile_variables = [
    ProfileVariables.TEMPERATURE,
    ProfileVariables.ELEVATION,
    ProfileVariables.TOTAL_DISTANCE,
]

# Check out what the existing study conditions are
# Without arguments it returns the Network Simulation, Study 1
study_constraints = model.tasks.networksimulation.get_constraints(study="Study 1")
print("The current constraints are:\n{}".format(study_constraints))

# Set the new study conditions
boundaries = {"Alpha_1:AVWell_1": {
                    Parameters.Boundary.PRESSURE:2500,
                    Parameters.Boundary.TEMPERATURE:150
                    }
            }      


# Set the new study rate constraints
constraints = {
    "Alpha_1": {Parameters.RateConstraint.LIQUIDFLOWRATE:333 },
    "Alpha_2": {Parameters.RateConstraint.LIQUIDFLOWRATE:555 },
    "Beta_1": {Parameters.RateConstraint.LIQUIDFLOWRATE:111, Parameters.RateConstraint.WATERFLOWRATE:150 },
    }
             
model.tasks.networksimulation.set_conditions(boundaries = boundaries, constraints=constraints, study="Study 1")
new_study_constraints = model.tasks.networksimulation.get_constraints()
print("The new constraints are:\n{}".format(new_study_constraints))


#Delete the constraints for "Beta_1"
delete_beta_1_constraints = {
    "Beta_1": {Parameters.RateConstraint.LIQUIDFLOWRATE:NAN, Parameters.RateConstraint.WATERFLOWRATE:NAN },
    }
model.tasks.networksimulation.set_conditions(boundaries = boundaries, constraints=delete_beta_1_constraints, study="Study 1")
new_study_constraints = model.tasks.networksimulation.get_constraints()
print("The new constraints are:\n{}".format(new_study_constraints))

# Run the simulation with constraints. It defaults to the Network Simulation, Study 1
print("Running the simulation with the new conditions.")
results = model.tasks.networksimulation.run(system_variables=system_variables, profile_variables=profile_variables)

#print results

print("Simulation state = {}".format(results.state))


print("Simulation summary:")
print(results.summary)

#generate result table like the one on PIPESIM UI:
#node results
node_df = pd.DataFrame.from_dict(results.node, orient="index")
node_df.index.name = "Variable"
print ("\nNode result = {}".format(node_df))

# compare well liquid rate with constraints
for  well in ["Alpha_1","Alpha_2"]:
    well_liq_flowrate=results.node[SystemVariables.VOLUME_FLOWRATE_LIQUID_STOCKTANK][well]
    well_liq_constraint=constraints[well][Parameters.RateConstraint.LIQUIDFLOWRATE]
    if well_liq_flowrate<well_liq_constraint:
        print("Well {0} has flowrate {1:5.2f}. Constraint {2:5.2f} was not reached ".format(well,well_liq_flowrate,well_liq_constraint))
    else:
        print("Well {0} has flowrate {1:5.2f}. Well was constrained by limit {2:5.2f}".format(well,well_liq_flowrate,well_liq_constraint))



    
#delete all the rate constraints
model.tasks.networksimulation.delete_constraints(study="Study 1")
new_study_constraints = model.tasks.networksimulation.get_constraints()
print("The new constraints are:\n{}".format(new_study_constraints))
# Close the model
model.close()
