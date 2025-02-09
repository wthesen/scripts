from sixgill.pipesim import Model, Units, ModelComponents, Parameters
import os

TIMESTAMP = "2025-02-09 00:58:57"
USERNAME = "wthesen"
PIPESIM_PROJECT = r"C:\Program Files\Schlumberger\Pipesim2023.1\Projects\Hoole_2025_02_07.pips"
SAVE_PATH = os.path.join(os.path.dirname(PIPESIM_PROJECT), f"Hoole_2025_02_07_corrected_{TIMESTAMP.replace(':', '-')}.pips")

try:
    print(f"[{TIMESTAMP}] Opening model: {PIPESIM_PROJECT}")
    model = Model.open(PIPESIM_PROJECT)

    # First, let's check what's in the model
    print(f"[{TIMESTAMP}] Checking existing model components:")
    for component in model.get_components():
        try:
            print(f"[{TIMESTAMP}] Component: {component}")
            if model.get_component_type(component) == ModelComponents.SOURCE:
                lat = model.get_value(Source=component, parameter=Parameters.Source.LATITUDE)
                lon = model.get_value(Source=component, parameter=Parameters.Source.LONGITUDE)
                fluid = model.get_value(Source=component, parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID)
                print(f"[{TIMESTAMP}] - Latitude: {lat}")
                print(f"[{TIMESTAMP}] - Longitude: {lon}")
                print(f"[{TIMESTAMP}] - Fluid: {fluid}")
                print("---")
        except Exception as e:
            print(f"[{TIMESTAMP}] Error getting properties for {component}: {str(e)}")

    # Now let's add new sources
    print(f"[{TIMESTAMP}] Adding new sources...")
    
    # Let's try just 5 wells first
    well_data = [
        ("Src-11", 55.87867848, -113.92900217),
        ("Src-12", 55.84338894, -113.8661201),
        ("Src-13", 55.83330032, -113.84815379),
        ("Src-14", 55.87363908, -113.92001902),
        ("Src-15", 55.86859902, -113.91103586)
    ]

    for source_name, lat, lon in well_data:
        try:
            print(f"[{TIMESTAMP}] Adding source: {source_name}")
            model.add(ModelComponents.SOURCE, source_name)
            model.set_value(Source=source_name, parameter=Parameters.Source.LATITUDE, value=lat)
            model.set_value(Source=source_name, parameter=Parameters.Source.LONGITUDE, value=lon)
            model.set_value(Source=source_name, parameter=Parameters.Source.TEMPERATURE, value=80)
            model.set_value(Source=source_name, parameter=Parameters.Source.PRESSURE, value=600)
            model.set_value(Source=source_name, parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID, value="Dry Gas")
            print(f"[{TIMESTAMP}] Successfully added {source_name}")
        except Exception as e:
            print(f"[{TIMESTAMP}] Error adding {source_name}: {str(e)}")

    print(f"[{TIMESTAMP}] Saving model to: {SAVE_PATH}")
    model.save(SAVE_PATH)
    print(f"[{TIMESTAMP}] Model saved successfully")

    # Verify the changes
    print(f"[{TIMESTAMP}] Verifying changes:")
    for component in model.get_components():
        try:
            if model.get_component_type(component) == ModelComponents.SOURCE:
                lat = model.get_value(Source=component, parameter=Parameters.Source.LATITUDE)
                lon = model.get_value(Source=component, parameter=Parameters.Source.LONGITUDE)
                fluid = model.get_value(Source=component, parameter=Parameters.Well.ASSOCIATEDBLACKOILFLUID)
                print(f"[{TIMESTAMP}] Source: {component}")
                print(f"[{TIMESTAMP}] - Latitude: {lat}")
                print(f"[{TIMESTAMP}] - Longitude: {lon}")
                print(f"[{TIMESTAMP}] - Fluid: {fluid}")
                print("---")
        except Exception as e:
            print(f"[{TIMESTAMP}] Error getting properties for {component}: {str(e)}")

except Exception as e:
    print(f"[{TIMESTAMP}] Error: {str(e)}")