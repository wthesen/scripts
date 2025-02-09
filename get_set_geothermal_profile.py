'''
    PIPESIM Python Toolkit
    Example: Get and set flowline geothermal profile

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

# Import the sixgill library and pandas
from sixgill.pipesim import Model
from sixgill.definitions import Units, Parameters
from utilities import open_model_from_case_study
import pandas as pd

# Simple routine to create the new survey
def new_geothermal_survey():
    survey = {}
    survey[Parameters.GeothermalSurvey.HORIZONTALDISTANCE] = [0.0,10.0,15.0]
    survey[Parameters.GeothermalSurvey.MEASUREDDISTANCE] = [0.0,15.0,30.0]
    survey[Parameters.GeothermalSurvey.TEMPERATURE] = [0.0, 20.0, 30.0]
    survey[Parameters.GeothermalSurvey.CURRENTVELOCITY] = [50.0, 60.0, 70.0]
    survey[Parameters.GeothermalSurvey.UCOEFF] = [20.0, 30.0, 55.0]
    return pd.DataFrame(survey)

# Open the flowline model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips", Units.SI)

# We're going to update flowline FL-3
flowline = 'Fl-3'

# Display the current flowline geothermal survey for information
print("Get flowline geothermal profile:")
geothermal_profile = model.get_geothermal_profile(Flowline = flowline)
print("Flowline geothermal profile of {0}:\n {1}".format(flowline, geothermal_profile))

# Set the new flowline geothermal survey
print("Set flowline geothermal profile: ")
data_frame = new_geothermal_survey()
model.set_geothermal_profile(Flowline = flowline, value=data_frame)

# And print out the new geothermal survey
check_geothermal_profile = model.get_geothermal_profile(context=flowline)
# the target flowline does not use GIS option. As such, columns of latitude, longitude and isvertex are ignored.
print("The flowline geothermal profile is now:\n {}".format(check_geothermal_profile))

# Close the model
print("Closing model...")
model.close()

# Open the well model
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")

well = "Well_1"

# Display the current well geothermal survey for information
print("Get well geothermal profile:")
geothermal_profile = model.get_geothermal_profile(Well = well)
print("Well borehole geothermal profile of {0}:\n {1}".format(well, geothermal_profile))

# Set the new well geothermal survey
print("Set well geothermal profile: ")
data_frame = new_geothermal_survey()
model.set_geothermal_profile(context=well, value=data_frame)

# And print out the new geothermal survey
check_geothermal_profile = model.get_geothermal_profile(context=well)
# the target flowline does not use GIS option. As such, columns of latitude, longitude and isvertex are ignored.
print("The well geothermal profile is now:\n {}".format(check_geothermal_profile))

# Close the model
print("Closing model...")
model.close()
