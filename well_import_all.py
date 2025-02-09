# -*- coding: utf-8 -*-
"""
Example script to demonstrate using the sixgill library with PIPESIM.
"""
import sys
import os
import importlib
import subprocess
import datetime
import pytz
import pandas as pd
import sixgill.pipesim as ps
from sixgill.definitions import Units, Tasks, SimulationState, ModelComponents, Parameters
import shutil

def get_current_user():
    """
    Get current user login
    """
    code = """
import ctypes
from ctypes.wintypes import DWORD
GetUserName = ctypes.windll.advapi32.GetUserNameW
size = DWORD(0)
GetUserName(None, ctypes.byref(size))
buffer = ctypes.create_unicode_buffer(size.value)
GetUserName(buffer, ctypes.byref(size))
print(buffer.value)
""".strip()
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_file = os.path.join(
            script_dir,
            f"_get_user_{os.getpid()}_{datetime.datetime.now().strftime('%H%M%S%f')}.py"
        )
        
        with open(temp_file, "w") as f:
            f.write(code)
        
        result = subprocess.run(
            [sys.executable, "-B", temp_file],
            capture_output=True,
            text=True,
            check=True
        )
        
        username = result.stdout.strip()
        return username if username else "unknown_user"
        
    except Exception as e:
        print(f"Note: Using default username due to: {e}", file=sys.stderr)
        return "unknown_user"
        
    finally:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass


def get_current_datetime_utc():
    """Get current UTC datetime in consistent format"""
    return datetime.datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")


def read_excel_data(file_path):
    """Read source data from Excel file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    df = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
    df.columns = df.columns.str.strip()
    print("Columns in the DataFrame:", df.columns.tolist())
    return df


def create_or_update_source(model, source_data):
    """Create or update a source in the Pipesim model"""
    source_name = source_data['UWI']
    existing_sources = [comp for comp in model.get_components(ModelComponents.SOURCE) if comp.name == source_name]

    if existing_sources:
        source_obj = existing_sources[0]
        print(f"Updating existing source: {source_name}")
    else:
        source_obj = model.new_component(ModelComponents.SOURCE)
        source_obj.name = source_name
        print(f"Creating new source: {source_name}")
        
    # Set parameters for the source
    source_obj.set_value(Parameters.PRESSURE, source_data['Pressure (psia)'])
    source_obj.set_value(Parameters.TEMPERATURE, source_data['Temperature (°F)'])
    source_obj.set_value(Parameters.GASFLOWRATE, source_data['Gas Flowrate (MSCFD)'])
    source_obj.set_value(Parameters.LIQUIDFLOWRATE, source_data['Liquid Flow Rate (BBL/D)'])
    source_obj.set_value(Parameters.LATITUDE, source_data['Latitude'])
    source_obj.set_value(Parameters.LONGITUDE, source_data['Longitude'])
    source_obj.set_value(Parameters.STATUS, source_data['Status'])
    source_obj.set_value(Parameters.FORMATION, source_data['Formation'])
    source_obj.set_value(Parameters.H2S, source_data['H2S'])
    source_obj.set_value(Parameters.CO2, source_data['CO2'])
    source_obj.set_value(Parameters.N2, source_data['N2'])
    source_obj.set_value(Parameters.H2, source_data['H2'])
    source_obj.set_value(Parameters.HE, source_data['HE'])
    source_obj.set_value(Parameters.C1, source_data['C1'])
    source_obj.set_value(Parameters.C2, source_data['C2'])
    source_obj.set_value(Parameters.C3, source_data['C3'])
    source_obj.set_value(Parameters.IC4, source_data['IC4'])
    source_obj.set_value(Parameters.NC4, source_data['NC4'])
    source_obj.set_value(Parameters.IC5, source_data['IC5'])
    source_obj.set_value(Parameters.NC5, source_data['NC5'])
    source_obj.set_value(Parameters.C6, source_data['C6'])
    source_obj.set_value(Parameters.C7PLUS, source_data['C7Plus'])

    model.save()


def create_sources_in_pipesim(model_path, sources_data):
    """Create or update sources in the Pipesim model"""
    print(f"Creating sources in Pipesim model: {model_path}")
    session = ps.create_pipesim_session(file_path=model_path)
    model = ps.Model(model_file=model_path, pipesim_session=session, unit_system=Units.FIELD)

    for index, source in sources_data.iterrows():
        print(f"\nProcessing source: {source['UWI']}")
        create_or_update_source(model, source)

    model.save()


def run_network_simulation(model, study_name):
    """
    Run a network simulation and retrieve results.
    """
    simulation = model.tasks.networksimulation
    simulation_id = simulation.start_simulation(study=study_name)

    sim_state = simulation.get_state(simulation_id)
    while sim_state.sim_status == SimulationState.RUNNING:
        print("Simulation is running...")
        sim_state = simulation.get_state(simulation_id)

    if sim_state.sim_status == SimulationState.COMPLETED:
        print("Simulation completed successfully.")
        results = simulation.get_results(simulation_id)
        print("Simulation results:", results)
    else:
        print("Simulation failed.")
        messages = simulation.get_messages(simulation_id)
        print("Simulation messages:", messages)


def main():
    """
    Main function that displays system information and processes the source data
    """
    time = get_current_datetime_utc()
    user = get_current_user()
    
    print(f"\nCurrent Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {time}")
    print(f"Current User's Login: {user}")

    excel_file_path = r"C:\Program Files\Schlumberger\Pipesim2023.1\Projects\pipesimpython.xlsx"
    sources_data = read_excel_data(excel_file_path)
    
    model_path = r"C:\Program Files\Schlumberger\Pipesim2023.1\Projects\Hoole_2025_02_07.pips"
    create_sources_in_pipesim(model_path, sources_data)
    
    session = ps.create_pipesim_session(file_path=model_path)
    model = ps.Model(model_file=model_path, pipesim_session=session, unit_system=Units.FIELD)
    run_network_simulation(model, study_name="Study 1")

    print(f"\nProcessed source data from: {excel_file_path}")


if __name__ == "__main__":
    main()