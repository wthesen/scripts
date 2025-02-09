
'''
    PIPESIM Python Toolkit
    Example: Running simulation sequentially using Process
'''
print("Running example file '{}'".format(__file__))

# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

from datetime import datetime
from multiprocessing import Process, Value
from sixgill.pipesim import Model
from sixgill.definitions import OutputVariables
from utilities import open_model_from_case_study

def run_sim(n):
    model = open_model_from_case_study("./Well Models/CSW_101_Basic Oil Well.pips")
    for _ in range(2):
        n.value += 1
        print ("Iteration {} ...".format(n.value))
        nodal_analysis_results = model.tasks.ptprofilesimulation.run('Well_1', system_variables=OutputVariables.System.WELL_PERFORMANCE, profile_variables=OutputVariables.Profile.WELL_PERFORMANCE)
        del nodal_analysis_results
    model.close()

def run_sim_using_process():
    num = Value('i', 0)
    for _ in range(2):
        p = Process(target=run_sim, args=(num,))
        p.start()
        p.join()        

if __name__ == '__main__':
    print("now =", datetime.now())
    run_sim_using_process()
    print("now =", datetime.now())
