'''
    PIPESIM Python Toolkit
    Example: Create network model example

'''
print("Running example file '{}'".format(__file__))

from sixgill.pipesim import Model
from sixgill.definitions import *
import tempfile
import pandas as pd


def _create_fl3_geometry_profile():
    survey = {}
    survey[Parameters.Flowline.MEASUREDDISTANCE] = [0.0,110.0,280.0,400.0]
    survey[Parameters.Flowline.HORIZONTALDISTANCE] = [0.0,100.0,200.0,300.0]
    survey[Parameters.Flowline.ELEVATION] = [100.0,105.0,150.0,200.0]
    return pd.DataFrame(survey)


# Open the model
filename = tempfile.gettempdir() + "/NewNetworkModel.pips"
print("Opening model '{}'".format(filename))
model = Model.new(filename, overwrite=True)

#create a black oil fluid
model.add(ModelComponents.BLACKOILFLUID, "BK111", parameters = {Parameters.BlackOilFluid.GOR:200} )

bo = model.find_components(component=ModelComponents.BLACKOILFLUID, context="BK111")[0]

#create a simple vertical well with one completion
model.add(ModelComponents.WELL, "Well 1",
          parameters = {Parameters.Well.AMBIENTTEMPERATURE:60,
                        Parameters.Well.X_COORD:93,
                        Parameters.Well.Y_COORD:338,})

model.add(ModelComponents.CASING, "Csg1", context="Well 1", \
         parameters={Parameters.Casing.TOPMEASUREDDEPTH:0,
                     Parameters.Casing.LENGTH:3000,
                     Parameters.Casing.INNERDIAMETER:12.0,
                     Parameters.Casing.BOREHOLEDIAMETER:24.0,
                     Parameters.Casing.ROUGHNESS:0.001,
                     Parameters.Casing.WALLTHICKNESS:0.5})

model.add(ModelComponents.TUBING, "Tub1", context="Well 1", \
         parameters={Parameters.Tubing.TOPMEASUREDDEPTH:0,
                     Parameters.Tubing.LENGTH:3000,
                     Parameters.Tubing.INNERDIAMETER:6,
                     Parameters.Tubing.ROUGHNESS:0.001,
                     Parameters.Tubing.WALLTHICKNESS:0.5})

model.add(ModelComponents.PACKER, "Packer", context="Well 1", parameters={Parameters.Packer.TOPMEASUREDDEPTH:2000})

model.add(ModelComponents.CHOKE, "CK-1", context="Well 1", \
         parameters={Parameters.Choke.TOPMEASUREDDEPTH:500, Parameters.Choke.BEANSIZE:2, Parameters.Choke.SUBCRITICALCORRELATION:Constants.SubCriticalFlowCorrelation.ASHFORD})

model.add(ModelComponents.COMPLETION, "VertComp", context="Well 1", \
         parameters={Parameters.Completion.TOPMEASUREDDEPTH:3000,
                     Parameters.Completion.FLUIDENTRYTYPE:Constants.CompletionFluidEntry.SINGLEPOINT,
                     Parameters.Completion.GEOMETRYPROFILETYPE:Constants.Orientation.VERTICAL,
                     Parameters.Completion.IPRMODEL: ModelComponents.IPRBACKPRESSURE,
                     Parameters.IPRBackPressure.CONSTANTC:5,
                     Parameters.IPRBackPressure.SLOPEN:1.1,
                     Parameters.Completion.RESERVOIRPRESSURE:4000,
                     Parameters.Completion.RESERVOIRTEMPERATURE:150 })

model.set_value(component=ModelComponents.WELL, context="Well 1", parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID, value=bo)
model.set_value(Well = "Well 1", Completion = "VertComp", parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID, value=bo)

model.add(ModelComponents.SOURCE, "Src-1", \
             parameters= {Parameters.Source.TEMPERATURE:80,
                          Parameters.Source.PRESSURE:600,
                          Parameters.Source.X_COORD:98,
                          Parameters.Source.Y_COORD:144,
                          })

model.set_value(Source = "Src-1", parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID, value="BK111")

#create Choke 1
model.add(ModelComponents.CHOKE, "Choke-1", \
             parameters= {Parameters.Choke.BEANSIZE:4,
                          Parameters.Choke.X_COORD:172,
                          Parameters.Choke.Y_COORD:317,
                         })

#create junction
model.add(ModelComponents.JUNCTION, "J-1", \
             parameters= {Parameters.Junction.X_COORD:272,
                          Parameters.Junction.Y_COORD:231,
                         })

#create two-phase separator
model.add(ModelComponents.TWOPHASESEPARATOR, "Separator", \
             parameters= {Parameters.TwoPhaseSeparator.PRODUCTIONSTREAM:Constants.SeparatorProductFluid.GAS,
                          Parameters.TwoPhaseSeparator.DISCARDEDSTREAM:Constants.SeparatorProductFluid.LIQUID,
                          Parameters.TwoPhaseSeparator.EFFICIENCY:99,
                          Parameters.TwoPhaseSeparator.X_COORD:411,
                          Parameters.TwoPhaseSeparator.Y_COORD:235,
                          })

#create generic pump
model.add(ModelComponents.PUMP, "Pump", \
             parameters= {Parameters.Pump.POWER:600,
                          Parameters.Pump.EFFICIENCY:99,
                          Parameters.Pump.PRESSUREDIFFERENTIAL:600,
                          Parameters.Pump.ROUTE:Constants.PumpThermodynamics.ADIABATIC,
                          Parameters.Pump.X_COORD:579,
                          Parameters.Pump.Y_COORD:322,
                          })

#create compressor
model.add(ModelComponents.COMPRESSOR, "Compressor", \
             parameters= {Parameters.Compressor.POWER:1400,
                          Parameters.Compressor.EFFICIENCY:70,
                          Parameters.Compressor.ROUTE:Constants.CompressorThermodynamics.ADIABATIC,
                          Parameters.Compressor.X_COORD:571,
                          Parameters.Compressor.Y_COORD:163,
                          })

#create heatexchanger
model.add(ModelComponents.HEATEXCHANGER, "HX", \
             parameters= {Parameters.HeatExchanger.TEMPERATUREDIFFERENTIAL:60,
                          Parameters.HeatExchanger.PRESSUREDROP:200,
                          Parameters.Compressor.X_COORD:650,
                          Parameters.Compressor.Y_COORD:163,
                          })

#create oil sink
model.add(ModelComponents.SINK, "Oil-facility", \
             parameters= {Parameters.Sink.PRESSURE:400,
                          Parameters.Sink.X_COORD:748,
                          Parameters.Sink.Y_COORD:312,
                          })

#create gas sink
model.add(ModelComponents.SINK, "Gas-tank", \
             parameters= {Parameters.Sink.GASFLOWRATE:50,
                          Parameters.Sink.FLOWRATETYPE:Constants.FlowRateType.GASFLOWRATE,
                          Parameters.Sink.X_COORD:748,
                          Parameters.Sink.Y_COORD:166,
                          })

#create flowline between choke-1 and J-1
model.add(ModelComponents.FLOWLINE, "RS-1", \
             parameters= {Parameters.Flowline.SHOWASRISER:True,
                          Parameters.Flowline.DETAILEDMODEL:True,
                          Parameters.Flowline.USEGLOBALSETTINGS: False,           
                          Parameters.Flowline.PLATFORMHEIGHT: 50,
                          Parameters.Flowline.HeatTransfer.ISUCALCULATED:True,
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:100,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

model.set_value('RS-1', Parameters.Flowline.AMBIENTAIRTEMPERATURE, 50)
model.set_value('RS-1', Parameters.Flowline.HeatTransfer.SURROUNDINGFLUIDVELOCITY, 2) 



#create flowline between J-1 and separator
model.add(ModelComponents.FLOWLINE, "FL-2", \
             parameters= {Parameters.Flowline.DETAILEDMODEL:False,
                          Parameters.Flowline.AMBIENTFLUIDTYPE:"Air",
                          Parameters.Flowline.USEGLOBALSETTINGS: False,
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:150,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

#create flowline between Src-1 and J-1
model.add(ModelComponents.FLOWLINE, "FL-3", \
             parameters= {Parameters.Flowline.DETAILEDMODEL:True,
                          Parameters.Flowline.AMBIENTFLUIDTYPE:"Water",
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:100,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

model.set_geometry( Flowline = "FL-3", value = _create_fl3_geometry_profile())

#create flowline between separator and Pump
model.add(ModelComponents.FLOWLINE, "FL-4", \
             parameters= {Parameters.Flowline.DETAILEDMODEL:False,
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:150,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

#create flowline between separator and Compressor
model.add(ModelComponents.FLOWLINE, "FL-5", \
             parameters= {Parameters.Flowline.DETAILEDMODEL:False,
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:150,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

#create flowline between Compressor and heat exchanger
model.add(ModelComponents.FLOWLINE, "GL-1", \
             parameters= {Parameters.Flowline.DETAILEDMODEL:False,
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:150,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

#create flowline between heat exchanger and gas-tank
model.add(ModelComponents.FLOWLINE, "GL-2", \
             parameters= {Parameters.Flowline.DETAILEDMODEL:False,
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:150,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

#create flowline between Pump and oil-facility
model.add(ModelComponents.FLOWLINE, "PL-1", \
             parameters= {Parameters.Flowline.DETAILEDMODEL:False,
                          Parameters.Flowline.INNERDIAMETER:4,
                          Parameters.Flowline.LENGTH:150,
                          Parameters.Flowline.ROUGHNESS:0.001,
                          Parameters.Flowline.WALLTHICKNESS:0.5,
                          Parameters.Flowline.UNDULATIONRATE:0.1,
                          Parameters.Flowline.HORIZONTALDISTANCE:200,
                          Parameters.Flowline.ELEVATIONDIFFERENCE:10,
                          })

#connect the surface facility into a network
model.connect({ModelComponents.SOURCE: 'Src-1'}, {ModelComponents.FLOWLINE: 'FL-3'})
model.connect({ModelComponents.FLOWLINE: 'FL-3'}, {ModelComponents.JUNCTION: 'J-1'})
model.connect({ModelComponents.WELL: 'Well 1'}, {ModelComponents.CHOKE: 'Choke-1'})
model.connect({ModelComponents.CHOKE: 'Choke-1'}, {ModelComponents.FLOWLINE: 'RS-1'})
model.connect({ModelComponents.FLOWLINE: 'RS-1'}, {ModelComponents.JUNCTION: 'J-1'})
model.connect({ModelComponents.JUNCTION: 'J-1'}, {ModelComponents.FLOWLINE: 'FL-2'})
model.connect({ModelComponents.FLOWLINE: 'FL-2'}, {ModelComponents.TWOPHASESEPARATOR: 'Separator'})
model.connect({ModelComponents.TWOPHASESEPARATOR: 'Separator'}, {ModelComponents.FLOWLINE: 'FL-4'}, \
               source_port=Connection.Separator.BOTTOM)
model.connect({ModelComponents.TWOPHASESEPARATOR: 'Separator'}, {ModelComponents.FLOWLINE: 'FL-5'},
               source_port=Connection.Separator.TOP)
model.connect({ModelComponents.FLOWLINE: 'FL-4'}, {ModelComponents.PUMP: 'Pump'})
model.connect({ModelComponents.PUMP: 'Pump'}, {ModelComponents.FLOWLINE: 'PL-1'})
model.connect({ModelComponents.FLOWLINE: 'PL-1'}, {ModelComponents.SINK: 'Oil-facility'})
model.connect({ModelComponents.FLOWLINE: 'FL-5'}, {ModelComponents.COMPRESSOR: 'Compressor'})
model.connect({ModelComponents.COMPRESSOR: 'Compressor'}, {ModelComponents.FLOWLINE: 'GL-1'})
model.connect({ModelComponents.FLOWLINE: 'GL-1'}, {ModelComponents.HEATEXCHANGER: 'HX'})
model.connect({ModelComponents.HEATEXCHANGER: 'HX'}, {ModelComponents.FLOWLINE: 'GL-2'})
model.connect({ModelComponents.FLOWLINE: 'GL-2'}, {ModelComponents.SINK: 'Gas-tank'})

#set wellstream outlet to choke
model.set_value(Well = "Well 1", parameter=Parameters.Well.WELLOUTLETEQUIPMENT, value="Choke-1")

print("Saving model as..." + filename)
model.save(filename)

model.close()
