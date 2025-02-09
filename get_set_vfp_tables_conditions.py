'''
    PIPESIM Python Toolkit
    Example: setting a vfp tables simulation with sensitivities
'''
print("Running example file '{}'".format(__file__))


# Make sure utilities file is not missed
import sys
import importlib
utilities_spec=importlib.util.find_spec("utilities")
if utilities_spec is None:
    print("")
    sys.exit("The script has been terminated. Missed 'utilities.py' file from Examples folder. Copy file and run the script again.")

# Import the sixgill library and anything else we need
from sixgill.definitions import Parameters, Constants
from utilities import open_model_from_case_study


# Open the model
model = open_model_from_case_study("./Well Models/CSW_131_IPO_SC_GL_Design.pips")
print(model.about())

well_name = "Well"

#Get a list of possible artificial lift sensitivities for VFP tables task
print("Possible artificial lift sensitivities:")
vars = model.tasks.vfptablessimulation.get_artificial_lift_variables(producer=well_name)
print(vars)

conditions = {
    Parameters.VfpTablesSimulation.RESERVOIRSIMULATOR: Constants.VFPTablesOperationTable.ECLIPSE,
    Parameters.VfpTablesSimulation.TABLENUMBER: 2,
    Parameters.VfpTablesSimulation.INCLUDETEMPERATURE: True,
    Parameters.VfpTablesSimulation.BOTTOMHOLEDATUMDEPTH: 30,
    Parameters.VfpTablesSimulation.RATETYPE : Parameters.VfpTablesSimulation.LIQUIDFLOWRATE,
    Parameters.VfpTablesSimulation.GLRATIOTYPE : Parameters.VfpTablesSimulation.GOR,
    Parameters.VfpTablesSimulation.GWRATIOTYPE : Parameters.VfpTablesSimulation.WATERCUT,
    
    Parameters.VfpTablesSimulation.SENSITIVITYVARIABLES:
        { 
            Parameters.VfpTablesSimulation.LIQUIDRATESENSITIVITY:[200.0, 300.0],
            Parameters.VfpTablesSimulation.OUTLETPRESSURESENSITIVITY:[250.0, 350.0],
            Parameters.VfpTablesSimulation.ARTIFICIALLIFTSENSITIVITY:
                {
                  Parameters.VfpTablesSimulation.SensitivityVariable.COMPONENT:Parameters.GasliftSensitivity.COMPONENTNAME,
                  Parameters.VfpTablesSimulation.SensitivityVariable.VARIABLE:Parameters.GasliftSensitivity.MINVALVEINJECTIONDP,
                  Parameters.VfpTablesSimulation.SensitivityVariable.VALUES:[40,50], #psia
                }
        }

            }


# Run the simulation 
print("Setting VFP tables conditions")

results = model.tasks.vfptablessimulation.set_conditions(producer=well_name, parameters=conditions)
conditions_to_check = model.tasks.vfptablessimulation.get_conditions(producer=well_name)


print("VFP table conditions:")
print(conditions_to_check)

# Close the model
model.close()
