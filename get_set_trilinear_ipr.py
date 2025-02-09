'''
    Pipesim Python Toolkit
    Example: Get and set completion IPR model

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

import pandas as pd

# Import the sixgill library
from sixgill.pipesim import Model
from sixgill.definitions import ModelComponents, Parameters, Constants, SystemVariables, ProfileVariables
from utilities import open_model_from_case_study

completion_name = 'Test_tri_linear'
well_name = 'Hor_Well'


def add_trilinear_transient_ipr(model):
    """
       Creates a new horizontal completion and sets it to Trilinear IPR model
    """
    

    parameters={
                Parameters.Completion.TOPMEASUREDDEPTH:10000,
                Parameters.Completion.BOTTOMMEASUREDDEPTH:11000,
                Parameters.Completion.ASSOCIATEDCOMPOSITIONALFLUID:'CFluid',
                Parameters.Completion.FLUIDENTRYTYPE:Constants.CompletionFluidEntry.DISTRIBUTED,
                Parameters.Completion.GEOMETRYPROFILETYPE:Constants.Orientation.HORIZONTAL,
                Parameters.Completion.IPRMODEL: Constants.IPRModels.IPRTRILINEAR,
                Parameters.Completion.SHOTDENSITY:3,
                Parameters.Completion.DIAMETER : 10,
                Parameters.Completion.PENETRATIONDEPTH:5,       
                Parameters.Completion.RESERVOIRPRESSURE:1500,
                Parameters.Completion.RESERVOIRTEMPERATURE:150,
                #The trilinear IPR parameters
                Parameters.IPRTriLinear.DISTANCETOBOUNDARY:1000,
                Parameters.IPRTriLinear.RESERVOIRTHICKNESS:30,
                Parameters.IPRTriLinear.OUTERRESPERM:0.05,
                Parameters.IPRTriLinear.INNERRESPERM:0.05,
                Parameters.IPRTriLinear.OUTERRESPOROSITY:5,
                Parameters.IPRTriLinear.INNERRESPOROSITY:3,
                Parameters.IPRTriLinear.OUTERRESCOMPRESSIBILITY:0.05,
                Parameters.IPRTriLinear.INNERRESCOMPRESSIBILITY:0.05,
                Parameters.IPRTriLinear.NUMHYDRAULICFRAC:10,
                Parameters.IPRTriLinear.HYDRAULICFRACHALF:15,
                Parameters.IPRTriLinear.HYDRAULICFRACWIDTH:0.5,
                Parameters.IPRTriLinear.HYDRAULICFRACPERM:180,
                Parameters.IPRTriLinear.HYDRAULICFRACPOROSITY:20,
                Parameters.IPRTriLinear.HYDRAULICFRACCOMPRESSIBILITY:0.05,
                Parameters.IPRTriLinear.CALCSKIN: False,
                Parameters.IPRTriLinear.CALCULATIONTYPE: Constants.TrilinearCalculationType.CONSTANTPRESSURE,
                Parameters.IPRTriLinear.TIME: 3,
                Parameters.IPRTriLinear.ISGASMODEL: False,
                Parameters.IPRTriLinear.USEVOGELBELOWBUBBLEPOINT: True,
                Parameters.IPRTriLinear.USEVOGELWATERCUTCORRECTION: False }

    model.add(ModelComponents.COMPLETION, completion_name, context=well_name, parameters=parameters)

def run_pt_profile_simulation(model):
    """
    Runs a pt profile simulation with time sensitivitiy
    Arguments:
        model {[Model]}
    """  
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
            ProfileVariables.TOTAL_DISTANCE
    ]
    parameters = {
    Parameters.PTProfileSimulation.INLETPRESSURE:3300,  #psia
    Parameters.PTProfileSimulation.OUTLETPRESSURE:250,  #psia
    Parameters.PTProfileSimulation.FLOWRATETYPE:Constants.FlowRateType.LIQUIDFLOWRATE,
    Parameters.PTProfileSimulation.LIQUIDFLOWRATE:300,
    #Set the custom variable
    Parameters.PTProfileSimulation.CALCULATEDVARIABLE:Constants.CalculatedVariable.CUSTOM,
    Parameters.PTProfileSimulation.CUSTOMVARIABLE:{
                          Parameters.PTProfileSimulation.CustomVariable.COMPONENT:completion_name,
                          Parameters.PTProfileSimulation.CustomVariable.VARIABLE:Parameters.IPRTriLinear.DISTANCETOBOUNDARY,
                          Parameters.PTProfileSimulation.CustomVariable.MINVALUE:200,
                          Parameters.PTProfileSimulation.CustomVariable.MAXVALUE:2000,
                      },
    #Set the sensitivity
    Parameters.PTProfileSimulation.SENSITIVITYVARIABLE:{
        Parameters.PTProfileSimulation.SensitivityVariable.COMPONENT:completion_name,
        Parameters.PTProfileSimulation.SensitivityVariable.VARIABLE:Parameters.IPRTriLinear.TIME,
        Parameters.PTProfileSimulation.SensitivityVariable.VALUES:[3.0,4.0,5.0] #psia
        }
    }

    # Find out what sensitivity variables are available for "Test_tri_linear' completion"
    sens_vars = model.tasks.ptprofilesimulation.get_sensitivity_variables(well_name)
    tri_linear_sens = sens_vars[completion_name]
    print('The available sensivity variables for completion "tri_linear_sens" are:')
    print(tri_linear_sens)
    

    # Run the simulation and print out the results
    print("Running PT profile simulation")
    results = model.tasks.ptprofilesimulation.run(producer=well_name,
                                   parameters=parameters,
                                   system_variables=system_variables,
                                   profile_variables=profile_variables)
    
    #generate result table like the one on PIPESIM UI:
    #system results
    system_df = pd.DataFrame.from_dict(results.system, orient="index")
    system_df.index.name = "Variable"
    print ("System result = {}".format(system_df))
    
    print ("Cases = {}".format(results.cases))
    
    #node results
    for case, node_res in results.node.items():
        print ("\nNode result for {}".format(case))
        node_df = pd.DataFrame.from_dict(node_res, orient="index")
        node_df.index.name = "Variable"
        print (node_df)
    
    #profile results
    for case, profile in results.profile.items():
        print ("\nProfile result for {}".format(case))
        profile_df = pd.DataFrame.from_dict(profile)
        print (profile_df)

# Open the model
model = open_model_from_case_study("./Well Models/CSW_105_Horizontal Oil Well.pips")

add_trilinear_transient_ipr(model)
#run a pt/profile simulation with sensitivities set to trilinear "time" parameter
run_pt_profile_simulation(model)

model.close()
