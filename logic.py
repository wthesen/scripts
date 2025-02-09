# -*- coding: utf-8 -*-
"""
Example script to demonstrate importing sources into a PIPESIM model using the sixgill library.
"""
import sys
import os
import subprocess
import datetime
import pytz
import pandas as pd
import sixgill.pipesim as ps
from sixgill.definitions import Units, ModelComponents, Parameters, SystemVariables, ProfileVariables

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
        return username if not username.isspace() else "unknown_user"
        
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
    existing_sources = model.find(Name=source_name)

    if existing_sources:
        # Get the actual component object instead of the name
        source_obj = existing_sources[0]
        print(f"Updating existing source: {source_name}")
    else:
        try:
            source_obj = model.add(ModelComponents.SOURCE, source_name)
            if not source_obj:
                print(f"Error: Failed to create source: {source_name}")
                return
            print(f"Creating new source: {source_name}")
        except Exception as e:
            print(f"Exception occurred while creating source {source_name}: {e}")
            return
        
    # Set parameters for the source
    try:
        source_obj.set_value(Parameters.Source.PRESSURE, source_data['Pressure (psia)'])
        source_obj.set_value(Parameters.Source.TEMPERATURE, source_data['Temperature (°F)'])
        source_obj.set_value(Parameters.Source.GASFLOWRATE, source_data['Gas Flowrate (MSCFD)'])
        source_obj.set_value(Parameters.Source.LIQUIDFLOWRATE, source_data['Liquid Flow Rate (BBL/D)'])
        source_obj.set_value(Parameters.Source.LATITUDE, source_data['Latitude'])
        source_obj.set_value(Parameters.Source.LONGITUDE, source_data['Longitude'])
        source_obj.set_value(Parameters.Source.STATUS, source_data['Status'])
        source_obj.set_value(Parameters.Source.FORMATION, source_data['Formation'])
        source_obj.set_value(Parameters.Source.H2S, source_data['H2S'])
        source_obj.set_value(Parameters.Source.CO2, source_data['CO2'])
        source_obj.set_value(Parameters.Source.N2, source_data['N2'])
        source_obj.set_value(Parameters.Source.H2, source_data['H2'])
        source_obj.set_value(Parameters.Source.HE, source_data['HE'])
        source_obj.set_value(Parameters.Source.C1, source_data['C1'])
        source_obj.set_value(Parameters.Source.C2, source_data['C2'])
        source_obj.set_value(Parameters.Source.C3, source_data['C3'])
        source_obj.set_value(Parameters.Source.IC4, source_data['IC4'])
        source_obj.set_value(Parameters.Source.NC4, source_data['NC4'])
        source_obj.set_value(Parameters.Source.IC5, source_data['IC5'])
        source_obj.set_value(Parameters.Source.NC5, source_data['NC5'])
        source_obj.set_value(Parameters.Source.C6, source_data['C6'])
        source_obj.set_value(Parameters.Source.C7PLUS, source_data['C7Plus'])
    except Exception as e:
        print(f"Error setting parameters for source {source_name}: {e}")

    model.save()


def create_sources_in_pipesim(model, sources_data):
    """Create or update sources in the Pipesim model"""
    for index, source in sources_data.iterrows():
        print(f"\nProcessing source: {source['UWI']}")
        create_or_update_source(model, source)


def run_network_simulation(model, study_name):
    """
    Run a network simulation and retrieve results.
    """
    system_variables = [
        SystemVariables.PRESSURE,
        SystemVariables.TEMPERATURE,
        SystemVariables.VOLUME_FLOWRATE_LIQUID_STOCKTANK,
        SystemVariables.VOLUME_FLOWRATE_OIL_STOCKTANK,
        SystemVariables.VOLUME_FLOWRATE_WATER_STOCKTANK,
        SystemVariables.VOLUME_FLOWRATE_GAS_STOCKTANK,
        SystemVariables.BOTTOM_HOLE_PRESSURE,
        SystemVariables.OUTLET_GLR_STOCKTANK,
        SystemVariables.OUTLET_WATER_CUT_STOCKTANK,
    ]
    profile_variables = [
        ProfileVariables.TEMPERATURE,
        ProfileVariables.ELEVATION,
        ProfileVariables.TOTAL_DISTANCE,
    ]

    results = model.tasks.networksimulation.run(
        study=study_name,
        system_variables=system_variables,
        profile_variables=profile_variables)

    # Convert results to DataFrames for easier handling
    node_results_df = pd.DataFrame(results.node)
    system_results_df = pd.DataFrame(results.system)
    profile_results_df = {key: pd.DataFrame(value) for key, value in results.profile.items()}

    # Print summaries of the results
    if not node_results_df.empty:
        print("\nNode Results Summary:")
        print(node_results_df.describe())
    else:
        print("\nNode Results Summary: No data available.")

    if not system_results_df.empty:
        print("\nSystem Results Summary:")
        print(system_results_df.describe())
    else:
        print("\nSystem Results Summary: No data available.")

    print("\nProfile Results Summary:")
    for key, df in profile_results_df.items():
        if not df.empty:
            print(f"\nProfile Results for {key}:")
            print(df.describe())
        else:
            print(f"\nProfile Results for {key}: No data available.")

    return results


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
    model = ps.Model.open(model_path, units=Units.FIELD)
    create_sources_in_pipesim(model, sources_data)
    run_network_simulation(model, study_name="Study 1")
    model.save()
    model.close()

    print(f"\nProcessed source data from: {excel_file_path}")


if __name__ == "__main__":
    main()