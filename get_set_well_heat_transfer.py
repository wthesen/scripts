'''
    PIPESIM Python Toolkit
    Example: get set well heat transfer

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
import pandas as pd
from sixgill.pipesim import Model
from sixgill.definitions import Constants, ModelComponents
from utilities import open_model_from_case_study
from sixgill.definitions import Parameters


def set_heat_transfer_calculate(model):
    survey = {}
    survey[Parameters.GeothermalSurvey.HORIZONTALDISTANCE] = [0.0,10.0,15.0]
    survey[Parameters.GeothermalSurvey.MEASUREDDISTANCE] = [0.0,15.0,30.0]
    survey[Parameters.GeothermalSurvey.TEMPERATURE] = [0.0, 20.0, 30.0]
    survey[Parameters.GeothermalSurvey.CURRENTVELOCITY] = [50.0, 60.0, 70.0]
    survey[Parameters.GeothermalSurvey.DENSITY] = [20.0, 30.0, 55.0]
    survey[Parameters.GeothermalSurvey.THERMALCONDUCTIVITY] = [20.0, 30.0, 55.0]
    survey[Parameters.GeothermalSurvey.SPECIFICHEATCAPACITY] = [1.0, 2.0, 3.0]
    df = pd.DataFrame(survey)
    #Set the table
    model.set_geothermal_profile(Well='Well', value=df)
    print_heat_tarnsfer_values(model)
    

def set_heat_transfer_specify(model):
    survey = {}
    survey[Parameters.GeothermalSurvey.HORIZONTALDISTANCE] = [0.0,10.0,15.0]
    survey[Parameters.GeothermalSurvey.MEASUREDDISTANCE] = [0.0,15.0,30.0]
    survey[Parameters.GeothermalSurvey.TEMPERATURE] = [0.0, 20.0, 30.0]
    survey[Parameters.GeothermalSurvey.CURRENTVELOCITY] = [50.0, 60.0, 70.0]
    survey[Parameters.GeothermalSurvey.UCOEFF] = [2.1,2.2,2.3]
    df = pd.DataFrame(survey)
    #Set the table
    model.set_geothermal_profile(Well='Well', value=df)
    print_heat_tarnsfer_values(model)
    
def print_heat_tarnsfer_values(model):
    status = model.get_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.HEATTRANSFERCOEFFICIENTSTATUS)
    print("Heat transfer coefficient: {}".format(status))
    hours = model.get_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.PRODUCTIONINJECTIONTIME)
    print("Production/injection time: {}".format(hours))
    #Get heat transfer table values
    new_survey = model.get_geothermal_profile(Well='Well')
    print(new_survey)

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

#set the heat transfer option to "Calculate"
model.set_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.HEATTRANSFERCOEFFICIENTSTATUS, value = Constants.HeatTransferCoefficient.CALCULATE)
status = model.get_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.HEATTRANSFERCOEFFICIENTSTATUS)
assert status == Constants.HeatTransferCoefficient.CALCULATE
#Set the production/injection time to 4000 hours
model.set_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.PRODUCTIONINJECTIONTIME, value = 4000.0)
hours = model.get_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.PRODUCTIONINJECTIONTIME)
assert hours == 4000.0
#Set the table values
set_heat_transfer_calculate(model) 


#set the heat transfer option to "specify"
model.set_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.HEATTRANSFERCOEFFICIENTSTATUS, value = Constants.HeatTransferCoefficient.SPECIFY)
status = model.get_value( Well = "Well", parameter = Parameters.Well.HeatTransfer.HEATTRANSFERCOEFFICIENTSTATUS)
assert status == Constants.HeatTransferCoefficient.SPECIFY
#Set the table values
set_heat_transfer_specify(model) 


# Close the model
print("Closing model...")
model.close()



