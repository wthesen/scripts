'''
    PIPESIM Python Toolkit
    Example: Create and parameterize a well

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")


from sixgill.pipesim import Model
from sixgill.definitions import ModelComponents, Parameters, Constants
from utilities import create_new_model

# Create a new model
model = create_new_model("AddWell.pips", overwrite=True)

print("Adding a black oil fluid named BK111")
model.add(ModelComponents.BLACKOILFLUID, "BK111", parameters = {Parameters.BlackOilFluid.GOR:200, Parameters.BlackOilFluid.WATERCUT:5} )

print("Adding a well named 'Well 2'.")
model.add(ModelComponents.WELL, "Well 2", parameters = {Parameters.Well.AMBIENTTEMPERATURE:60})

model.set_value(Well = "Well 2", parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID, value="BK111")

print("Setting the tubing and casing for Well 2.")
model.add(ModelComponents.CASING, "Csg1", context="Well 2", \
         parameters={Parameters.Casing.TOPMEASUREDDEPTH:0,
                     Parameters.Casing.LENGTH:1000,
                     Parameters.Casing.INNERDIAMETER:12.0,
                     Parameters.Casing.BOREHOLEDIAMETER:30,
                     Parameters.Casing.ROUGHNESS:0.001,
                     Parameters.Casing.THERMALCONDUCTIVITY:34.001,
                     Parameters.Casing.DENSITY:2.001,
                     Parameters.Casing.FLUIDTHERMALCONDUCTIVITY:2.001,
                     Parameters.Casing.CEMENTTHERMALCONDUCTIVITY:2.001,
                     Parameters.Casing.WALLTHICKNESS:0.5})

model.add(ModelComponents.CASING, "Csg2", context="Well 2", \
         parameters={Parameters.Casing.TOPMEASUREDDEPTH:0,
                     Parameters.Casing.LENGTH:3000,
                     Parameters.Casing.INNERDIAMETER:8,
                     Parameters.Casing.BOREHOLEDIAMETER:30,
                     Parameters.Casing.ROUGHNESS:0.001,
                     Parameters.Casing.WALLTHICKNESS:0.5})

model.add(ModelComponents.LINER, "Csg3", context="Well 2", \
         parameters={Parameters.Liner.TOPMEASUREDDEPTH:2950,
                     Parameters.Liner.LENGTH:1050,
                     Parameters.Liner.INNERDIAMETER:6,
                     Parameters.Liner.BOREHOLEDIAMETER:30,
                     Parameters.Liner.ROUGHNESS:0.001,
                     Parameters.Liner.WALLTHICKNESS:0.3})

model.add(ModelComponents.TUBING, "Tub1", context="Well 2", \
         parameters={Parameters.Tubing.TOPMEASUREDDEPTH:0,
                     Parameters.Tubing.LENGTH:3000,
                     Parameters.Tubing.INNERDIAMETER:4,
                     Parameters.Tubing.ROUGHNESS:0.001,
                     Parameters.Tubing.WALLTHICKNESS:0.2})

model.add(ModelComponents.TUBING, "Tub2", context="Well 2", \
         parameters={Parameters.Tubing.TOPMEASUREDDEPTH:3000,
                     Parameters.Tubing.LENGTH:1000,
                     Parameters.Tubing.INNERDIAMETER:3,
                     Parameters.Tubing.ROUGHNESS:0.001,
                     Parameters.Tubing.WALLTHICKNESS:0.2})

model.add(ModelComponents.PACKER, "Packer", context="Well 2", parameters={Parameters.Packer.TOPMEASUREDDEPTH:2000})

############################################################################
#Follow code snippets demonstrates how to add other downhole equipment
############################################################################

print("Adding a choke to Well 2")
model.add(ModelComponents.CHOKE, "CK1", context="Well 2", \
         parameters={Parameters.Packer.TOPMEASUREDDEPTH:2000,
                     Parameters.Choke.BEANSIZE:2,
                     Parameters.Choke.SUBCRITICALCORRELATION:Constants.SubCriticalFlowCorrelation.ASHFORD})

print("Adding an ESP to well 2")
model.add(ModelComponents.ESP, "Esp1", context="Well 2", \
         parameters={Parameters.ESP.TOPMEASUREDDEPTH:1500,
                     Parameters.ESP.OPERATINGFREQUENCY:180,
                     Parameters.ESP.PERMANENTMAGNETMOTOR:True,
                     Parameters.ESP.NUMBEROFPOLES:6,
                     Parameters.ESP.MANUFACTURER:"ALNAS",
                     Parameters.ESP.MODEL:"ANA580",
                     Parameters.ESP.NUMBERSTAGES:100,
                     Parameters.ESP.HEADFACTOR:1,
                     Parameters.ESP.POWERFACTOR:0.95,
                     Parameters.ESP.USEVISCOSITYCORRECTION:True})

#model.add(ModelComponents.PCP, "Pcp1", context="Well 2", \
#         parameters={Parameters.PCP.TOPMEASUREDDEPTH:700,
#                     Parameters.PCP.OPERATINGSPEED:100,
#                     Parameters.PCP.MANUFACTURER:"Weatherford",
#                     Parameters.PCP.MODEL:"BMW 100-4000",
#                     Parameters.PCP.ISTOPDRIVE:False,
#                     Parameters.PCP.HEADFACTOR:1,
#                     Parameters.PCP.POWERFACTOR:0.95,
#                     Parameters.PCP.FLOWRATEFACTOR:0.98,
#                     Parameters.PCP.USEVISCOSITYCORRECTION:True})

#model.add(ModelComponents.RODPUMP, "Rp1", context="Well 2", \
#         parameters={Parameters.RodPump.TOPMEASUREDDEPTH:300,
#                     Parameters.RodPump.NOMINALFLOWRATE:100,
#                     Parameters.RodPump.RODDIAMETER:1.2,
#                     Parameters.RodPump.HASGASSEPARATOR:True})

#from sixgill.definitions import GasLiftType
#model.add(ModelComponents.GASLIFTINJECTION, "Inj1", context="Well 2", \
#         parameters={Parameters.GasLiftInjection.TOPMEASUREDDEPTH:400,
#                     Parameters.GasLiftInjection.GASLIFTTYPE:GasLiftType.GLR,
#                     Parameters.GasLiftInjection.GLR:10})
#model.add(ModelComponents.GASLIFTINJECTION, "Inj2", context="Well 2", \
#         parameters={Parameters.GasLiftInjection.TOPMEASUREDDEPTH:450,
#                     Parameters.GasLiftInjection.MANUFACTURER:"Bompet", \
#                     Parameters.GasLiftInjection.SERIES:"ERO4-JR", \
#                     Parameters.GasLiftInjection.VALVETYPE:"IPO", \
#                     Parameters.GasLiftInjection.PORTSIZE:0.25, \
#                     Parameters.GasLiftInjection.DISCHARGECOEFFICIENT:65, \
#                     Parameters.GasLiftInjection.DISCHARGETOFULLYOPEN:995, \
#                     Parameters.GasLiftInjection.SPRINGPRESSURE:1000, \
#                     Parameters.GasLiftInjection.PTRO:1000, \
#                     })

#model.add(ModelComponents.ENGINEKEYWORDS, "Ek1", context="Well 2", \
#         parameters={Parameters.EngineKeywords.TOPMEASUREDDEPTH:100,
#                     Parameters.EngineKeywords.KEYWORDS:"print all"})

#model.add(ModelComponents.SLIDINGSLEEVE, "Slv1", context="Well 2", \
#         parameters={Parameters.SlidingSleeve.TOPMEASUREDDEPTH:950, Parameters.SlidingSleeve.ISOPEN:False})

#model.add(ModelComponents.SUBSURFACESAFETYVALVE, "SSV1", context="Well 2", \
#         parameters={Parameters.SubsurfaceSafetyValve.TOPMEASUREDDEPTH:250, Parameters.SubsurfaceSafetyValve.BEANID:2})

print("Adding a vertical completion to Well 2")
model.add(ModelComponents.COMPLETION, "VertComp11", context="Well 2", \
         parameters={Parameters.Completion.TOPMEASUREDDEPTH:2800,
                     Parameters.Completion.FLUIDENTRYTYPE:Constants.CompletionFluidEntry.SINGLEPOINT,
                     Parameters.Completion.GEOMETRYPROFILETYPE:Constants.Orientation.VERTICAL,
                     Parameters.Completion.IPRMODEL: Constants.IPRModels.IPRPIMODEL,
                     Parameters.Completion.RESERVOIRPRESSURE:4000,
                     Parameters.IPRPIModel.ISGASMODEL:True,
                     Parameters.IPRPIModel.GASPI:5,
                     Parameters.Completion.RESERVOIRTEMPERATURE:150,
                     Parameters.Well.ASSOCIATEDBLACKOILFLUID: "BK111" })

print("Adding a horizontal completion to Well 2")
model.add(ModelComponents.COMPLETION, "HoriComp", context="Well 2", \
         parameters={Parameters.Completion.TOPMEASUREDDEPTH:3500,
                     Parameters.Completion.BOTTOMMEASUREDDEPTH:4000,
                     Parameters.Completion.FLUIDENTRYTYPE:Constants.CompletionFluidEntry.DISTRIBUTED,
                     Parameters.Completion.GEOMETRYPROFILETYPE:Constants.Orientation.HORIZONTAL,
                     Parameters.Completion.IPRMODEL: Constants.IPRModels.IPRPSSBABUODEH,
                     Parameters.DistributedCompletionModel.ISGASMODEL:True,
                     Parameters.DistributedCompletionModel.GASPI:5,
                     Parameters.DistributedCompletionModel.RESERVOIRXDIM:1000,
                     Parameters.DistributedCompletionModel.RESERVOIRYDIM:1000,
                     Parameters.DistributedCompletionModel.RESERVOIRTHICKNESS:1000,
                     Parameters.DistributedCompletionModel.PERMEABILITYX:5,
                     Parameters.DistributedCompletionModel.PERMEABILITYY:4,
                     Parameters.DistributedCompletionModel.RESERVOIREXTENT:10,
                     Parameters.DistributedCompletionModel.LOCATIONECCEN:10,
                     Parameters.DistributedCompletionModel.COMPLETIONVERTICALPERMRATIO:0.9,  #kv/k
                     Parameters.DistributedCompletionModel.LOCATIONXPOS:4,
                     Parameters.DistributedCompletionModel.LOCATIONYPOS:1,
                     Parameters.DistributedCompletionModel.LOCATIONZPOS:17,
                     Parameters.DistributedCompletionModel.WELLLENGTH:100,
                     Parameters.Completion.RESERVOIRPRESSURE:4000,
                     Parameters.Completion.RESERVOIRTEMPERATURE:150 })

model.set_value(context="Well 2:HoriComp", parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID, value="BK111")

# Save and close the model
print("All finished. Saving model...")
model.save()
model.close()
