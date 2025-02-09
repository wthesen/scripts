'''
    PIPESIM Python Toolkit
    Example: Get and set well trajectory

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
from sixgill.definitions import Units, Parameters, NAN
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips", Units.SI)

print("Getting well trajectory for Well_1")
trajectory = model.get_trajectory(context="Well_1")
print("Well trajectory of 'Well_1':\n {}".format(trajectory))

# Create the new trajectory dataframe
new_trajectory = {}
new_trajectory[Parameters.WellTrajectory.INCLINATION] = [0,0.1,0.2,0.3,0.4,0.5]
new_trajectory[Parameters.WellTrajectory.AZIMUTH] = [NAN,NAN,NAN,NAN,NAN,NAN]
new_trajectory[Parameters.WellTrajectory.MAXDOGLEGSEVERITY] = [NAN,NAN,NAN,NAN,NAN,NAN]
new_trajectory[Parameters.WellTrajectory.TRUEVERTICALDEPTH] = [0.0,105.0,205.0,305.0,405.0,505.0]
new_trajectory[Parameters.WellTrajectory.MEASUREDDEPTH] = [0.0,100.0,200.0,300.0,400.0,500.0]
df = pd.DataFrame(new_trajectory)

print("Setting new well trajectory")
model.set_trajectory(context="Well_1", value=df)

check_trajectory = model.get_trajectory(Well="Well_1")
print("The well trajectory is now:\n {}".format(check_trajectory))

# Close the model
print("Closing model...")
model.close()
