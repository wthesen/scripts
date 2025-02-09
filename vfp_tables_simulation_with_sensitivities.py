'''
    PIPESIM Python Toolkit
    Example: Running a vfp tables simulation with sensitivities
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
import tempfile
from sixgill.definitions import Parameters, SystemVariables, Constants  
   
from utilities import open_model_from_case_study


# Open the model
model = open_model_from_case_study("./Well Models/CSW_131_IPO_SC_GL_Design.pips")
print(model.about())

well_name = "Well"

conditions = {Parameters.VfpTablesSimulation.RESERVOIRSIMULATOR: Constants.VFPTablesOperationTable.ECLIPSE,
                          Parameters.VfpTablesSimulation.TABLENUMBER: 2,
                          Parameters.VfpTablesSimulation.INCLUDETEMPERATURE: True,
                          Parameters.VfpTablesSimulation.BOTTOMHOLEDATUMDEPTH: 30,
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
print("Running VFP tables simulation")

results = model.tasks.vfptablessimulation.run(producer=well_name, parameters=conditions)

vfp_table_content = results.system[SystemVariables.VFP_TABLES][well_name]
vfp_table_with_temperature_content = results.system[SystemVariables.VFP_TABLES_WITH_TEMPERATURE][well_name]


print("VFP table content")
print(vfp_table_content)
print("================================================================")
print("VFP table with temperature content")
print(vfp_table_with_temperature_content)

#Export both results to files
folder_path = tempfile.gettempdir()
file_name = folder_path + r"\vfp_table_content.txt"
text_file = open(file_name, "w")
text_file.write(vfp_table_content)
text_file.close()
print('{} generated'.format(file_name))

file_name = folder_path + r"\vfp_table_with_temperature_content.txt"
text_file = open(file_name, "w")
text_file.write(vfp_table_with_temperature_content)
text_file.close()
print('{} generated'.format(file_name))


#Get the results in files:   
files = model.tasks.vfptablessimulation.generate_engine_files(producer=well_name, study="Study 1", folder_path=folder_path)
print("The exported VFP tables simulation files are:")
print(files)




# Close the model
model.close()
