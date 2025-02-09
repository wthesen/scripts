'''
    PIPESIM Python Toolkit
    Example: Running a nodal simulation
    
    Attention.
    Matplotlib library must be installed manually to successfully proceed 
    with this example.
'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file and matplotlib are not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

matplotlib_spec=importlib.util.find_spec("matplotlib")
if matplotlib_spec is None:
    sys.exit("The script has been terminated. Matplotlib library must be installed manually to successfully proceed with this example")
    
import pandas as pd
import matplotlib.pyplot as plt

# Import the sixgill library and anything else we need
from sixgill.pipesim import Model
from sixgill.definitions import Parameters, SystemVariables, ProfileVariables, \
            Constants
from utilities import open_model


# Plot: NA analysis plot with operating envelope
def NA_plot(inflowP,inflowQL, outflowP, outflowQL, NA_Point_pressure,NA_Point_LiquidRate,Operating_envelope):

    fig = plt.figure(1, figsize=(12,8)) 
       
    xs, ys = zip(*sorted(zip(inflowQL, inflowP)))
    xs2, ys2 = zip(*sorted(zip(outflowQL, outflowP)))
    xs3, ys3 = zip(*sorted(zip(Operating_envelope.max_drawdown['LiquidFlowrate'], Operating_envelope.max_drawdown['LiquidFlowratePressure'])))
    xs4, ys4 = zip(*sorted(zip(Operating_envelope.reservoir_pressure['LiquidFlowrate'], Operating_envelope.reservoir_pressure['LiquidFlowratePressure'])))
    xs5, ys5 = zip(*sorted(zip(Operating_envelope.erosional_velocity['LiquidFlowrate'], Operating_envelope.erosional_velocity['LiquidFlowratePressure'])))
    xs6, ys6 = zip(*sorted(zip(Operating_envelope.aofp['LiquidFlowrate'], Operating_envelope.aofp['LiquidFlowratePressure'])))
    xs7, ys7 = zip(*sorted(zip(Operating_envelope.inversion_point['LiquidFlowrate'], Operating_envelope.inversion_point['LiquidFlowratePressure'])))
    xs8, ys8 = zip(*sorted(zip(Operating_envelope.liquid_loading['LiquidFlowrate'], Operating_envelope.liquid_loading['LiquidFlowratePressure'])))

    plt.plot(xs, ys, 'b', label='Inflow') 
    plt.plot(xs2, ys2, 'r', label='Outflow')
    plt.plot(xs3, ys3, 'g', label='Max Drawdown')
    plt.plot(xs4, ys4, 'b', label='Reservoir Pressure')
    plt.plot(xs5, ys5, 'c', label='Max Erosional Velocity')
    plt.plot(xs6, ys6, 'k', label='AOFP')
    plt.plot(xs7, ys7, 'y', label='Inversion point for stable tubing production')
    plt.plot(xs8, ys8, 'm', label='Liquid loading')
    plt.scatter(NA_Point_LiquidRate, NA_Point_pressure, s=200, c='r', label='Operation Point')
    plt.legend(loc=1)
    fig.suptitle('NA analysis plot with operating envelope', fontsize=18)
    plt.xlabel('Stock-tank liquid rate at nodal point (STB/d)', fontsize=14)
    plt.ylabel('Pressure at nodal point (psia)', fontsize=14)
    plt.show()

# Open the model
model = open_model("./models/Nodal_example.pips")
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
            SystemVariables.VOLUME_FLOWRATE_GAS_STOCKTANK,
            SystemVariables.WATER_CUT_INSITU,
            SystemVariables.WELLHEAD_VOLUME_FLOWRATE_FLUID_INSITU,
            SystemVariables.OUTLET_VOLUME_FLOWRATE_GAS_STOCKTANK,
            SystemVariables.OUTLET_VOLUME_FLOWRATE_OIL_STOCKTANK,
            SystemVariables.OUTLET_VOLUME_FLOWRATE_WATER_STOCKTANK,
            SystemVariables.SYSTEM_OUTLET_TEMPERATURE,
            SystemVariables.BOTTOM_HOLE_PRESSURE,
            SystemVariables.OUTLET_GLR_STOCKTANK,
            SystemVariables.OUTLET_WATER_CUT_STOCKTANK
]

profile_variables = [
            ProfileVariables.TEMPERATURE,
            ProfileVariables.PRESSURE,
            ProfileVariables.ELEVATION,
            ProfileVariables.TOTAL_DISTANCE,
]

conditions = {Parameters.NodalAnalysisSimulation.LIMITINFLOW: False,
                          Parameters.NodalAnalysisSimulation.LIMITOUTFLOW: True,
                          Parameters.NodalAnalysisSimulation.OUTFLOWPOINTS: 40,
                          Parameters.NodalAnalysisSimulation.INFLOWPOINTS: 50,
                          Parameters.NodalAnalysisSimulation.MAXFLOWRATETYPE: Constants.FlowRateType.LIQUIDFLOWRATE,
                          Parameters.NodalAnalysisSimulation.MAXLIQUIDRATE: 30000,
                          Parameters.NodalAnalysisSimulation.MAXOUTFLOWPRESSURE: 3000,
                          Parameters.NodalAnalysisSimulation.OUTLETPRESSURE: 600,
                          Parameters.NodalAnalysisSimulation.MAXGASRATE: 300,
                          Parameters.NodalAnalysisSimulation.BRANCHTERMINATOR: "J 1",
                          Parameters.NodalAnalysisSimulation.USEPHASERATIO: True

            }

boundaries = {"Well2 - Oil:Completion":{ Parameters.Boundary.PRESSURE:2500,
                                Parameters.Boundary.TEMPERATURE:200,
                                Parameters.Boundary.USEGASRATIO: Constants.GasRatioOption.GLR,
                                Parameters.Boundary.GLR: 600,
                                Parameters.Boundary.USEWATERRATIO: Constants.WaterRatioOption.WATERCUT,
                                Parameters.Boundary.WATERCUT:12 }
                    }

nodal_point_settings = {
                         Parameters.NodalPoint.NODALTYPE: Constants.NodalPointType.DOWNHOLE,
                         Parameters.NodalPoint.DEPTH: 9500,
                         Parameters.NodalPoint.WELLSTRINGTYPE: Constants.TubingSectionType.CASING,
                         Parameters.NodalPoint.NAME: 'NodalPoint'}

# Run the simulation 
print("Running nodal simulation")

results = model.tasks.nodalanalysis.run(producer="Well2 - Oil", parameters=conditions,nodal_point_settings=nodal_point_settings,
                                                inlet_conditions=boundaries, system_variables=system_variables,
                                                profile_variables=profile_variables)


# NA OperationPoint
NA_Point_pressure = results.operating_points[0].point_data[SystemVariables.NODAL_POINT_PRESSURE]
NA_Point_LiquidRate= results.operating_points[0].point_data[SystemVariables.NODAL_POINT_VOLUME_FLOWRATE_LIQUID_STOCKTANK]


# inflow curves:

inflowQL=results.inflow_curves[0].curve_data[SystemVariables.NODAL_POINT_VOLUME_FLOWRATE_LIQUID_STOCKTANK]
inflowP= results.inflow_curves[0].curve_data[SystemVariables.NODAL_POINT_PRESSURE]


# outflow curve
outflowQL= results.outflow_curves[0].curve_data[SystemVariables.NODAL_POINT_VOLUME_FLOWRATE_LIQUID_STOCKTANK]
outflowP= results.outflow_curves[0].curve_data[SystemVariables.NODAL_POINT_PRESSURE]


# Operating envelope - 6 curves

Operating_envelope = results.operating_envelope

envelope_max_drawdownP=results.operating_envelope.max_drawdown[Parameters.NodalOperatingEnvelopePlot.LIQUIDFLOWRATEPRESSURE]

envelope_reservoir_pressureP=results.operating_envelope.reservoir_pressure[Parameters.NodalOperatingEnvelopePlot.LIQUIDFLOWRATEPRESSURE]

envelope_erosional_velocityQL= results.operating_envelope.erosional_velocity[Parameters.NodalOperatingEnvelopePlot.LIQUIDFLOWRATE]

envelope_aofpQL= results.operating_envelope.aofp[Parameters.NodalOperatingEnvelopePlot.LIQUIDFLOWRATE]

envelope_inversion_pointQL= results.operating_envelope.inversion_point[Parameters.NodalOperatingEnvelopePlot.LIQUIDFLOWRATE]

envelope_liquid_loadingQL= results.operating_envelope.liquid_loading[Parameters.NodalOperatingEnvelopePlot.LIQUIDFLOWRATE] # NAN       


if len(sys.argv) == 1:
    NA_plot(inflowP,inflowQL, outflowP, outflowQL, NA_Point_pressure,NA_Point_LiquidRate, Operating_envelope)

# Close the model
model.close()
