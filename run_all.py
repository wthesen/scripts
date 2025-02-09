'''
    PIPESIM Python Toolkit
    Example: Run all the example scripts

'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

import glob
import os

folder = os.path.dirname(__file__)
if not folder:
    # to support: python run_all.py
    folder = "./"

all_examples = glob.glob(folder + '\*.py')

list_of_failled_examples = []
# Run all examples except itself
for example in all_examples:
    if 'run_all' in example:
        continue
    print(100*'#')
    print('Running example "{}".'.format(example))
    try:
        exec(open(example).read())
    except Exception as e:
        print('Example "{}" failed with error: "{}".'.format(example,e.args))
        list_of_failled_examples.append(example)

if list_of_failled_examples:
    raise ValueError('List of failled examples: {}.'.format(list_of_failled_examples))