'''
    PIPESIM Python Toolkit
    Example: Get and set blackoil user viscosity table

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


def _create_viscosity_table():
    viscosity_survey = {}
    viscosity_survey[Parameters.BlackOilUserViscosityTable.TEMPERATURE] = [66,86,106]
    viscosity_survey[Parameters.BlackOilUserViscosityTable.VISCOSITY] = [99.3,101.23,94.56]
    return pd.DataFrame(viscosity_survey)

# Open the model
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")

blackoil = 'Heavy_Oil'
print("Get blackoil user viscosity table: ")
viscosity_table = model.get_deadoil_viscosity_table(BlackOilFluid=blackoil)
print("Blackoil user viscosity table of {0}:\n {1}".format(blackoil, viscosity_table))

#Delete the viscosity points
model.delete_deadoil_viscosity_table(BlackOilFluid=blackoil)
#Try to get the viscosity table after delete(should come back with zero points)
viscosity_table = model.get_deadoil_viscosity_table(BlackOilFluid=blackoil)
print("Blackoil user viscosity table of {0}:\n has now {1} points".format(blackoil, viscosity_table.size))

print("Set blackoil user viscosity table: ")
data_frame = _create_viscosity_table()

model.set_deadoil_viscosity_table(BlackOilFluid=blackoil, value=data_frame)
check_viscosity_table = model.get_deadoil_viscosity_table(context=blackoil)

print("The black oil viscosity table is now:\n {}".format(check_viscosity_table))

# Close the model
print("Closing model...")
model.close()
