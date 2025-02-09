'''
    PIPESIM Python Toolkit
    Example: Get and set using Model.find_component_objects

'''
print("Running example file '{}'".format(__file__))



from utilities import open_model_from_case_study

# Import the sixgill library
from sixgill.definitions import Units, Parameters, ALL
from sixgill.core.resources import ModelComponents



# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips", Units.SI)

#get all the flowline components in the model
flowlines = model.find_component_objects(Flowline=ALL)
#find the one with the name "FL-3"
flowline = next((fl for fl in flowlines if fl.name == "FL-3"), None)

#Alternatively, you can get only one flowline:
flowline = model.find_component_objects(Flowline='FL-3', component=ModelComponents.FLOWLINE)[0]


print("Get flowline geometry profile: ")
geometry_profile = model.get_geometry(context=flowline)
print(f"Flowline geometry profile of {flowline}:\n {geometry_profile}")

print("Setting the inner diameter of the 'FL-3' flowline")
print(f"The inner diameter before: {model.get_value(flowline, parameter=Parameters.Flowline.INNERDIAMETER)}")
model.set_value(flowline, parameter=Parameters.Flowline.INNERDIAMETER, value = 3.5)
print(f"The inner diameter is now {model.get_value(flowline, parameter=Parameters.Flowline.INNERDIAMETER)}")


# Close the model
print("Closing model...")
model.close()
