from typing import Optional
from sixgill.definitions import Units
from sixgill.pipesim import Model
import os.path
import tempfile

def get_case_study_path(case_study_file):
    relativePath = os.path.join(os.path.dirname(__file__), './../../../Case Studies')
    if os.path.exists(relativePath):
        return os.path.join(relativePath, case_study_file)
    
    return os.path.join('C:/Program Files/Schlumberger/PIPESIM2023.1/Case Studies', case_study_file)

def open_model_from_full_path(full_path, units: Optional[str]=Units.FIELD):
    print("Opening model '{}'".format(os.path.abspath(full_path)))
    return Model.open(full_path, units)

def open_model_from_case_study(case_study_file, units: Optional[str]=Units.FIELD)->Model:
    return open_model_from_full_path(get_case_study_path(case_study_file), units)

def open_model(filename, units: Optional[str]=Units.FIELD):
    if os.path.isabs(filename):
        full_path = filename
    else:
        full_path = os.path.join(os.path.dirname(__file__), filename)
    return open_model_from_full_path(full_path, units)

def create_new_model(filename, units: Optional[str]=Units.FIELD, overwrite: Optional[bool]=False):
    full_path = os.path.join(tempfile.gettempdir(), filename)
    print("Creating model '{}'".format(full_path))
    return Model.new(full_path, units, overwrite)

def save_model(model, filename):
    if os.path.isabs(filename):
        full_path = filename
    else:
        full_path = os.path.join(tempfile.gettempdir(), filename)
    model.save(full_path)
    print("Model saved to {}".format(full_path))


def make_sure_model_has_no_issues(model):
    if len(model.validate()) > 0:
        raise RuntimeError("Model has validation issues") 

