'''
    PIPESIM Python Toolkit
    Example: Get and set source PQ curve

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
from sixgill.definitions import Units, Parameters
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips", Units.SI)

# Create the new PQ curve dataframe
new_pq_curve = {}
new_pq_curve[Parameters.PQCurve.PRESSURE] = [2.0, 3.0, 4.0, 5.0]
new_pq_curve[Parameters.PQCurve.LIQUIDFLOWRATE] = [7.0, 8.0, 9.0, 10.0]
df = pd.DataFrame(new_pq_curve)

# Switch to using the PQ Curve
print("Setting new PQ curve")
model.set_value(context="Source", parameter=Parameters.Source.USEPQCURVE, value=True)
model.set_pq_curve(context="Source", value=df)

# Check the PQ Curve that is now being used
check_pq_curve = model.get_pq_curve(Source="Source")
print("The PQ curve of Source is now:\n {}".format(check_pq_curve))

# Close the model
print("Closing model...")
model.close()
