'''
    PIPESIM Python Toolkit
    Example: Create a compositional fluid

'''
print("Running example file '{}'".format(__file__))

from sixgill.pipesim import Model
from sixgill.definitions import ModelComponents, Parameters, Constants
import tempfile
import pandas as pd

# Open the model
filename = tempfile.gettempdir() + "/NewCompositionalFluidModel.pips"
print("Opening model '{}'".format(filename))
model = Model.new(filename, overwrite=True)

print ("Set compositional fluid model level settings. This only needs to be done once per model...")

#set the model to use compositional fluid.
model.fluids.fluid_type = Constants.FluidType.COMPOSITIONAL

#set the compositional fluid model settings. This only needs to be done once per model
model.fluids.compositional.pvt_package = Constants.PVTPackage.MULTIFLASH
model.fluids.compositional.equation_of_state = Constants.EquationOfState.Multiflash.CUBICPLUSASSOCIATION
model.fluids.compositional.salinity_model = Constants.SalinityModel.IONANALYSIS

#create a custom fluid component
c7plus_component_params = {
    Parameters.FluidComponent.HYDROCARBONFORM:Constants.FluidComponentType.HYDROCARBON,
    Parameters.FluidComponent.MOLECULARWEIGHT:234,
    Parameters.FluidComponent.TBOIL:250,
}

model.fluids.compositional.add_pseudocomponent("C7Plus", parameters=c7plus_component_params)

#select the components
selected_components = [
    Constants.MultiflashComponent.METHANE,
    Constants.MultiflashComponent.ETHANE,
    Constants.MultiflashComponent.HEXANE,
    Constants.MultiflashComponent.ETHANOL,
    Constants.MultiflashComponent.PROPANE,
    Constants.MultiflashComponent.WATER,
    "C7Plus",
]
model.fluids.compositional.select_components(selected_components)

print ("End of compositional fluid model level settings")
################################################################################

#create a compositional fluid Comp1 with salt component
print ("Create compositional fluid Comp1 with salt component...")
fluid_parameters = {
    Parameters.CompositionalFluid.LIQUIDVISCOSITYCALC:Constants.EmulsionViscosityMethod.CONTINUOUSPHASE,
    Parameters.CompositionalFluid.USERWATERCUTCUTOFF:40,
    Parameters.CompositionalFluid.IONSODIUM:1000,
    Parameters.CompositionalFluid.IONCALCIUM:5000,
    Parameters.CompositionalFluid.IONMAGNESIUM:3000,
    Parameters.CompositionalFluid.IONPOTASSIUM:4012,
    Parameters.CompositionalFluid.IONSTRONTIUM:5000,
    Parameters.CompositionalFluid.IONBARIUM:6000,
    Parameters.CompositionalFluid.IONIRON:17000,
    Parameters.CompositionalFluid.IONCHLORIDE:1000,
    Parameters.CompositionalFluid.IONSULPHATE:1235,
    Parameters.CompositionalFluid.IONBICARBONATE:11122,
    Parameters.CompositionalFluid.IONBROMIDE:544,
    Parameters.CompositionalFluid.IONBARIUM:5555,
    Parameters.CompositionalFluid.SALTWATERDENSITYTYPE:Constants.SaltWaterDensity.DENSITY,
    Parameters.CompositionalFluid.SALTWATERDENSITY:72,
}

model.add(ModelComponents.COMPOSITIONALFLUID, "Comp1", parameters=fluid_parameters)

#set fluid parameters
model.set_value(component=ModelComponents.COMPOSITIONALFLUID, Name="Comp1", parameter=Parameters.CompositionalFluid.COMPONENTFRACTIONTYPE, value=Constants.ComponentFractionType.MOLE)

#can set the fluid component fractions using dataframe
comp1_fraction = {}
comp1_fraction[Parameters.FluidComponentFraction.COMPONENT] = [
    Constants.MultiflashComponent.METHANE,
    Constants.MultiflashComponent.ETHANE,
    Constants.MultiflashComponent.HEXANE,
    Constants.MultiflashComponent.PROPANE,
    Constants.MultiflashComponent.ETHANOL,
    Constants.MultiflashComponent.WATER,
    "C7Plus"]
comp1_fraction[Parameters.FluidComponentFraction.SPECIFIEDFRACTION] = [5.45, 12.08, 24.23, 13.0, 7.0, 5.0, 5.0]
comp1_data = pd.DataFrame(comp1_fraction).set_index(Parameters.FluidComponentFraction.COMPONENT)

model.fluids.compositional.set_composition(context="Comp1", value=comp1_data)

#get the fluid composition
comp1_fraction_from_model = model.fluids.compositional.get_composition(context="Comp1")
print ("Compositional fluid \"Comp1\" component fractions:")
print (comp1_fraction_from_model)

print ("Create compositional fluid Comp2 without salt component...")

#create a compositional fluid Comp2, no salt component
model.add(ModelComponents.COMPOSITIONALFLUID, "Comp2")

#set fluid parameters
model.set_value(component=ModelComponents.COMPOSITIONALFLUID, Name="Comp2", parameter=Parameters.CompositionalFluid.COMPONENTFRACTIONTYPE, value=Constants.ComponentFractionType.MOLE)

#can also set the fluid component fractions using dictionary
comp2_fraction = {}
comp2_fraction[Constants.MultiflashComponent.METHANE] = 25.0
comp2_fraction[Constants.MultiflashComponent.ETHANE] = 12.0
comp2_fraction[Constants.MultiflashComponent.HEXANE] = 8.0
comp2_fraction[Constants.MultiflashComponent.PROPANE] = 13.0
comp2_fraction[Constants.MultiflashComponent.ETHANOL] = 7.0
comp2_fraction[Constants.MultiflashComponent.WATER] = 15.0
comp2_fraction["C7Plus"] = 15.0

model.fluids.compositional.set_composition(context="Comp2", value=comp2_fraction)

#get the fluid composition
comp2_fraction_from_model = model.fluids.compositional.get_composition(context="Comp2")
print ("Compositional fluid \"Comp2\" component fractions:")
print (comp2_fraction_from_model)

#save the model
print("Saving model as..." + filename)
model.save(filename)

model.close()
