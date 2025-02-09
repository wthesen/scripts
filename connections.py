'''
    PIPESIM Python Toolkit
    Example: Get connections

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
from sixgill.definitions import Connection
from utilities import open_model_from_case_study
import pandas as pd

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")
all_connections = model.connections()

print("All the conncetions in the model:")
print(pd.DataFrame(all_connections).sort_values("Destination").set_index("Destination"))

print("All the connections connected to Well")
connections_to_well = model.connections(Well ='Well')
print(pd.DataFrame(connections_to_well))

print("All the connections connected to LL-2")
connections_to_flowline = model.connections(Flowline ='LL-2')
print(pd.DataFrame(connections_to_flowline))

print("A selection of the connections to LL-2")
ll2_connections = model.get_connections(Name="LL-2")
print("Inlet from = {}".format(ll2_connections["LL-2"][Connection.SOURCE]))
print("Inlet Source Port = {}".format(ll2_connections["LL-2"][Connection.SOURCEPORT]))
print("Outlet to = {}".format(ll2_connections["LL-2"][Connection.DESTINATION]))

model.close()
