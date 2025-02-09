'''
    PIPESIM Python Toolkit
    Example: Get and set flow correlations

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
from sixgill.definitions import Parameters, Constants

import tempfile
import pandas as pd
from collections import defaultdict
from utilities import open_model_from_case_study

# Open the model
model = open_model_from_case_study("./Network Models/CSN_301_Small Network.pips")

sim_settings = model.sim_settings

#get global flow correlation
global_correlation = sim_settings.global_flow_correlation()
for k, v in global_correlation.items():
    print ("{} = {}".format(k, v))

#set global flow correlation to OLGAS
olgas_corr = {
    Parameters.FlowCorrelation.Multiphase.Vertical.SOURCE: Constants.MultiphaseFlowCorrelationSource.OLGAS,
    Parameters.FlowCorrelation.Multiphase.Vertical.CORRELATION: Constants.MultiphaseFlowCorrelation.OLGAS.OLGASV731_3PHASE,
    Parameters.FlowCorrelation.Multiphase.Horizontal.SOURCE: Constants.MultiphaseFlowCorrelationSource.OLGAS,
    Parameters.FlowCorrelation.Multiphase.Horizontal.CORRELATION: Constants.MultiphaseFlowCorrelation.OLGAS.OLGASV731_3PHASE,
}
sim_settings.global_flow_correlation(olgas_corr)

#check that values are set properly
global_correlation = sim_settings.global_flow_correlation()
for k, v in global_correlation.items():
    print ("{} = {}".format(k, v))

#get and set flow correlation mappings
print ("Use global flow correlation? {}".format(sim_settings.use_global_flow_correlation))

#change this flag to false
sim_settings.use_global_flow_correlation = False

#get the flow correlation mapping for wells and flowlines
flow_correlation_mapping = sim_settings.get_flow_correlations()
fc_data_frame = pd.DataFrame.from_dict(flow_correlation_mapping, orient="index")
fc_data_frame.index.name = "Name"
print (fc_data_frame)

#get the flow correlation mapping that matches context
flow_correlation_mapping = sim_settings.get_flow_correlations(context = "FL-1")
fc_data_frame = pd.DataFrame.from_dict(flow_correlation_mapping, orient="index")
fc_data_frame.index.name = "Name"
print (fc_data_frame)

#change the flow correlation to use BJA for FL-1
new_fc_mapping = defaultdict(dict)
new_fc_mapping["FL-1"][Parameters.FlowCorrelation.Multiphase.Vertical.SOURCE] = Constants.MultiphaseFlowCorrelationSource.BAKER_JARDINE
new_fc_mapping["FL-1"][Parameters.FlowCorrelation.Multiphase.Vertical.CORRELATION] = Constants.MultiphaseFlowCorrelation.BakerJardine.BEGGSBRILLREVISED
new_fc_mapping["FL-1"][Parameters.FlowCorrelation.Multiphase.Vertical.HOLDUPFACTOR] = 0.9
new_fc_mapping["FL-1"][Parameters.FlowCorrelation.Multiphase.Horizontal.SOURCE] = Constants.MultiphaseFlowCorrelationSource.BAKER_JARDINE
new_fc_mapping["FL-1"][Parameters.FlowCorrelation.Multiphase.Horizontal.CORRELATION] = Constants.MultiphaseFlowCorrelation.BakerJardine.BEGGSBRILLREVISED
new_fc_mapping["FL-1"][Parameters.FlowCorrelation.Multiphase.Horizontal.HOLDUPFACTOR] = 0.95
new_fc_mapping["FL-1"][Parameters.FlowCorrelation.OVERRIDEGLOBAL] = True

sim_settings.set_flow_correlations(new_fc_mapping)

filename = tempfile.gettempdir() + "/TestFlowCorrelationSettings.pips"
print("Saving model as..." + filename)
model.save(filename)

#close the model
model.close()
