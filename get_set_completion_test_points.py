'''
    PIPESIM Python Toolkit
    Example: Get and set completion test points

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


def _new_completion_test_points():
    points = {}
    points[Parameters.CompletionTestPoint.LIQUIDFLOWRATE] = [1.0, 2.0, 3.0, 4.0]
    points[Parameters.CompletionTestPoint.GASFLOWRATE] = [5.0, 6.0, 7.0, 9.0]
    points[Parameters.CompletionTestPoint.STATICRESERVOIRPRESSURE] = [10.0, 11.0, 12.0, 12.0]
    points[Parameters.CompletionTestPoint.BOTTOMHOLEFLOWINGPRESSURE] = [13.0, 14.0, 15.0, 16.0]
    return pd.DataFrame(points)


# Open the model
model = open_model_from_case_study("./Well Models/CSW_141_Vert Multilayer Producer.pips", Units.SI)

# Uppler_Layer Completion
print("Getting upper layer completion test points for Well_1")
test_points = model.get_completion_test_points(context='Well_1:Upper_Layer')
print("Well completion test points of Upper_Layer completion in Well_1 :\n {}".format(test_points))

# Create the new completion test points dataframe
new_test_points = _new_completion_test_points()

print("Setting new well completion test points to Upper_Layer completion in Well_1")
model.set_completion_test_points(context='Well_1:Upper_Layer', value = new_test_points)

check_test_points = model.get_completion_test_points(context='Well_1:Upper_Layer')
print("The well completion test points of Upper_Layer completion in Well_1 is now:\n {}".format(check_test_points))


# Middle_Layer Completion
print("Getting middle layer completion test points for Well_1")
test_points = model.get_completion_test_points(Well = "Well_1", Completion = 'Middle_Layer')
print("Well completion test points of Middle_Layer completion in Well_1 :\n {}".format(test_points))

# Create the new completion test points dataframe
new_test_points = _new_completion_test_points()

print("Setting new well completion test points to Middle_Layer completion in Well_1")
model.set_completion_test_points(value = new_test_points, Well = "Well_1", Completion = 'Middle_Layer')

check_test_points = model.get_completion_test_points(Well = "Well_1", Completion = 'Middle_Layer')
print("The well completion test points of Middle_Layer completion in Well_1 is now:\n {}".format(check_test_points))


# Bottom_Layer Completion
print("Getting bottom layer completion test points for Well_1")
test_points = model.get_completion_test_points(Well = "Well_1", Name = 'Bottom_Layer')
print("Well completion test points of Bottom_Layer completion in Well_1 :\n {}".format(test_points))

# Create the new completion test points dataframe
new_test_points = _new_completion_test_points()

print("Setting new well completion test points to Bottom_Layer completion in Well_1")
model.set_completion_test_points(value = new_test_points, Well = "Well_1", Name = 'Bottom_Layer')

check_test_points = model.get_completion_test_points(Well = "Well_1", Name = 'Bottom_Layer')
print("The well completion test points of Bottom_Layer completion in Well_1 is now:\n {}".format(check_test_points))

# Close the model
print("Closing model...")
model.close()
