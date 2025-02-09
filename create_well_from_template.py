'''
    PIPESIM Python Toolkit
    Example: Copy a template to a new well

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
from utilities import create_new_model

model = create_new_model("copy_well.pips", overwrite=True)

model.copy('Simple vertical', 'Sixgill', True)

print(model.find(Well='Sixgill'))

model.save(model.filename)

model.close()
