'''
    Pipesim Python Toolkit
    Example: Set model fluid to MFL fluid

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from sixgill.definitions import Parameters, ModelComponents, Constants
from utilities import open_model_from_case_study, get_case_study_path


# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")


print('The model is using {} fluid".'.format(model.fluids.fluid_type))


#define a name for the fluid
fluid_name = "My mfl fluid"

print("Get the associated compositional fluid for the source")
value = model.get_value(context="Source", parameter=Parameters.Source.ASSOCIATEDCOMPOSITIONALFLUID)
print('The source is using {} fluid definition. Changing it to {}.'.format(value, fluid_name))

#Get the full path to fluid file
fluid_file_path = get_case_study_path("./Fluid Files/Medium_Oil_B.mfl")

#Create an MFL fluid
model.add(ModelComponents.MFLFLUID, fluid_name, parameters = {Parameters.MFLFluid.FLUIDFILENAME:fluid_file_path})
model.set_value(context="Source", parameter=Parameters.Source.ASSOCIATEDMFLFLUID, value=fluid_name)


#Create a second mfl fluid and assign it to completion

fluid_file_path = get_case_study_path("./Fluid Files/Medium_Oil_A.mfl")
fluid_name = "My second mfl fluid"
model.add(ModelComponents.MFLFLUID, fluid_name, parameters = {Parameters.MFLFluid.FLUIDFILENAME:fluid_file_path})
model.set_value(context="VertComp", parameter=Parameters.Completion.ASSOCIATEDMFLFLUID, value=fluid_name)

#Set the model fluid type to MFL
model.fluids.fluid_type = Constants.FluidType.MFL
print('The model is now using {} fluid".'.format(model.fluids.fluid_type))

# Close the model
print("Closing model...")
model.close()
