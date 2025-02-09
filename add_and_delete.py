'''
    PIPESIM Python Toolkit
    Example: Add and delete components

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from sixgill.pipesim import Model
from sixgill.definitions import ModelComponents
import tempfile

# Open the model
filename = tempfile.gettempdir() + "/ExercisingAddAndDelete.pips"
print("Opening model '{}'".format(filename))
model = Model.new(filename, overwrite=True)

node = model.add(component=ModelComponents.SOURCE, name='Sixgill')

print(model.find(Name='Sixgill'))

model.delete(component=ModelComponents.SOURCE, Name='Sixgill')

print(model.find(Name='Sixgill'))

# And if the same item exists twice, then its not going to let you continue
newnode1 = model.add(component=ModelComponents.SOURCE, name='SixgillXP')

print("This will raise an error because the item already exists")
try:
    newnode2 = model.add(component=ModelComponents.SOURCE, name='SixgillXP')
except ValueError as ex:
    print('Error message: "{}"'.format(ex.args[0]))

model.close()
