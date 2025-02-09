'''
    PIPESIM Python Toolkit
    Example: Get and set fluid composition

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
import pandas as pd
from sixgill.definitions import Units, Parameters, Constants
from sixgill.definitions import ModelComponents
from utilities import open_model_from_case_study

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips", Units.SI)

print("Getting fluid composition for C-Fluid")
fluid_composition = model.fluids.compositional.get_composition(context="C-Fluid")
print("Fluid composition of C-Fluid:\n{}".format(fluid_composition))

# Create the new fluid composition as a dataframe
comp_names = [
        Constants.MultiflashComponent.METHANE,
        Constants.MultiflashComponent.ETHANE,
        Constants.MultiflashComponent.BUTANE,
        Constants.MultiflashComponent.PROPANE
    ]
comp_fracs = [ 10.0, 20.0, 30.0, 40.0 ]
comp = {
    Parameters.FluidComponentFraction.COMPONENT: comp_names,
    Parameters.FluidComponentFraction.SPECIFIEDFRACTION: comp_fracs
}
new_composition = pd.DataFrame(comp).set_index(Parameters.FluidComponentFraction.COMPONENT)

print("Setting new fluid composition")
model.fluids.compositional.set_composition(context="C-Fluid", value = new_composition)

check_composition = model.fluids.compositional.get_composition(CompositionalFluid="C-Fluid")
print("The fluid composition of C-Fluid is now:\n {}".format(check_composition))

# Add a new compositional fluid
fluid_parameters = {
    Parameters.CompositionalFluid.LIQUIDVISCOSITYCALC:Constants.EmulsionViscosityMethod.CONTINUOUSPHASE,
    Parameters.CompositionalFluid.USERWATERCUTCUTOFF:40,
}
model.add(ModelComponents.COMPOSITIONALFLUID, "Comp1", parameters=fluid_parameters)
# Create the new fluid composition as a dict
composition1 = {
        Constants.MultiflashComponent.METHANE: 20.0,
        Constants.MultiflashComponent.ETHANE: 20.0,
        Constants.MultiflashComponent.BUTANE: 20.0,
        Constants.MultiflashComponent.PROPANE: 20.0,
        Constants.MultiflashComponent.CARBON_DIOXIDE: 20.0
}
model.fluids.compositional.set_composition(CompositionalFluid="Comp1", value = composition1)

check_composition1 = model.fluids.compositional.get_composition(CompositionalFluid="Comp1")
print("The fluid composition of Comp1 is:\n {}".format(check_composition1))

# Close the model
print("Closing model...")
model.close()
