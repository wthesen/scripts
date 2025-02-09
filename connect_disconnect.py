'''
    PIPESIM Python Toolkit
    Example: Connect/disconnect equipment and flowline

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
from sixgill.definitions import ModelComponents, Connection
from utilities import open_model, save_model
import tempfile
import os.path

# Open the model
model = open_model("./models/CSN_301_Small Network_Connection.pips")

print('Connect Source to Manifold')
model.connect('Source', 'Manifold')
    
print('Connect Well to Choke')
model.connect({ModelComponents.WELL: 'Well'}, {ModelComponents.CHOKE: 'Choke'})
    
print('Connect Separator top port to Compressor')
model.connect({ModelComponents.TWOPHASESEPARATOR: 'Separator'}, {ModelComponents.COMPRESSOR: 'Compressor'}, source_port=Connection.Separator.TOP)
    
print('Connect Separator bottom port to Pmp')
model.connect('Separator', 'Pmp', source_port=Connection.Separator.BOTTOM)
    
print('Connect Choke to FL-2')
model.connect({ModelComponents.CHOKE: 'Choke'}, {ModelComponents.FLOWLINE: 'FL-2'})
    
print('Connect FL-2 to Manifold')
model.connect({ModelComponents.FLOWLINE: 'FL-2'}, {ModelComponents.JUNCTION: 'Manifold'})
    
print('Cannot Connect Well to Choke')
#The connect should fail because the port of the equipment is occupied
try:
   model.connect({ModelComponents.WELL: 'Well'}, {ModelComponents.CHOKE: 'Choke'})
except ValueError as ex:
    print(ex)
    
print('Disconnect Well from Choke')
model.disconnect(source='Well', destination='Choke')

print('Disconnect Compressor from GL-2')
model.disconnect('GL-2', 'Compressor')

save_model(model, "CSN_301_Small Network_Connection.pips")

# Close the model
print("Closing model...")
model.close()
