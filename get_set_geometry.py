'''
    PIPESIM Python Toolkit
    Example: Get and set flowline geometry profile

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from collections import defaultdict
from utilities import open_model_from_case_study
import pandas as pd

# Import the sixgill library
from sixgill.pipesim import Model
from sixgill.definitions import Units, Parameters


def _create_geometry_profile():
    survey = {}
    survey[Parameters.FlowlineGeometry.LATITUDE] = [0.15,0.25,0.21,0.58]
    survey[Parameters.FlowlineGeometry.LONGITUDE] = [0.1,0.12,2.01,1.0]
    return pd.DataFrame(survey)

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips", Units.SI)

flowline = 'FL-3'
print("Get flowline geometry profile: ")
geometry_profile = model.get_geometry(context=flowline)
print("Flowline geometry profile of {0}:\n {1}".format(flowline, geometry_profile))

print("Set flowline geometry profile: ")
data_frame = _create_geometry_profile()
model.set_value(context=flowline, parameter=Parameters.Flowline.USEGISDATA, value=True)
model.set_geometry(context=flowline, value=data_frame)
check_geometry_profile = model.get_geometry(context=flowline)
# the target flowline does not use GIS option. As such, columns of latitude, longitude and isvertex are ignored.
print("The flowline geometry profile is now:\n {}".format(check_geometry_profile))

# Close the model
print("Closing model...")
model.close()
