'''
    PIPESIM Python Toolkit
    Example: Get and set blackoil user mix viscosity table

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from utilities import open_model_from_case_study
import pandas as pd

# Import the sixgill library
from sixgill.definitions import Parameters


def _create_mix_viscosity_table():
    mix_viscosity_survey = {}
    mix_viscosity_survey[Parameters.BlackOilUserEmulsionTable.WATERCUT] = [
        0, 33, 45
    ]
    mix_viscosity_survey[
        Parameters.BlackOilUserEmulsionTable.VISCOSITYRATIO] = [
            0.22, 0.5, 0.1
        ]
    return pd.DataFrame(mix_viscosity_survey)


# Open the model
model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")

blackoil = 'Heavy_Oil'
print("Get blackoil user mix viscosity table: ")
viscosity_table = model.get_mix_viscosity_table(BlackOilFluid=blackoil)
print("Blackoil user mix viscosity table of {0}:\n {1}".format(
    blackoil, viscosity_table))


print("Set blackoil user mix viscosity table: ")
data_frame = _create_mix_viscosity_table()

model.set_mix_viscosity_table(BlackOilFluid=blackoil, value=data_frame)
check_mix_viscosity_table = model.get_mix_viscosity_table(context=blackoil)

print("The black oil mix viscosity table is now:\n {}".format(
    check_mix_viscosity_table))

#Delete the mix viscosity points
print('')
print('Delete blackoil user mix viscosity table:')
model.delete_mix_viscosity_table(BlackOilFluid=blackoil)
#Try to get the mix viscosity table after delete(should come back with zero points)
viscosity_table = model.get_mix_viscosity_table(BlackOilFluid=blackoil)
print("Blackoil user mix viscosity table of {0}:\n has now {1} points".format(
    blackoil, viscosity_table.size))
print('')


# Close the model
print("Closing model...")
model.close()
