#!/usr/bin/env python3
"""
Test script for NO2 data extraction using the point extraction functionality.

Since your NetCDF file is on a Windows path that's not accessible in this Linux environment,
this script shows you how to use the functionality once you have the file accessible.
"""

import pandas as pd
import numpy as np
import xarray as xr
from pathlib import Path
from STanalysis import extract_point_values

def create_mock_no2_data(output_path: Path) -> None:
    """Create a mock NO2 dataset similar to your real data for testing."""
    # Create time dimension (daily data for ~9 years like your file)
    times = pd.date_range("2006-01-01", periods=100, freq="D")  # Smaller for testing
    
    # Create x,y coordinates similar to your LAEA projection (EPSG:3035)
    # Your file has x=3890, y=4037, but we'll use smaller dimensions for testing
    x_coords = np.linspace(2426378.0, 6593261.9, 50)  # Based on your geospatial bounds
    y_coords = np.linspace(1285303.3, 5446513.7, 50)
    
    # Create some realistic NO2 data (μg/m³)
    np.random.seed(42)  # For reproducible results
    data = np.random.gamma(2, 15, size=(len(times), len(y_coords), len(x_coords)))
    data = np.where(data > 100, np.nan, data)  # Cap at 100 μg/m³, set higher values to NaN
    
    # Create the dataset
    ds = xr.Dataset(
        {
            "no2_downscaled": (
                ("time", "y", "x"), 
                data.astype(np.float32),
                {
                    "_FillValue": np.nan,
                    "missing_value": np.nan,
                    "standard_name": "mass_concentration_of_nitrogen_dioxide_in_air",
                    "long_name": "Downscaled NO2 concentration in air",
                    "units": "μg/m³",
                    "grid_mapping": "crs",
                }
            )
        },
        coords={
            "time": (
                "time",
                times,
                {
                    "standard_name": "time",
                    "long_name": "time",
                    "units": "days since 2006-01-01 00:00:00",
                    "calendar": "proleptic_gregorian",
                    "axis": "T",
                }
            ),
            "x": (
                "x",
                x_coords,
                {
                    "standard_name": "projection_x_coordinate",
                    "long_name": "x coordinate of projection",
                    "units": "m",
                    "axis": "X",
                }
            ),
            "y": (
                "y", 
                y_coords,
                {
                    "standard_name": "projection_y_coordinate",
                    "long_name": "y coordinate of projection",
                    "units": "m",
                    "axis": "Y",
                }
            ),
        }
    )
    
    # Add CRS information (EPSG:3035 - LAEA Europe)
    ds["crs"] = xr.DataArray(
        0,
        attrs={
            "grid_mapping_name": "lambert_azimuthal_equal_area",
            "longitude_of_projection_origin": 10.0,
            "latitude_of_projection_origin": 52.0,
            "false_easting": 4321000.0,
            "false_northing": 3210000.0,
            "semi_major_axis": 6378137.0,
            "semi_minor_axis": 6356752.314140356,
            "inverse_flattening": 298.257222101,
            "crs_wkt": '''PROJCS["ETRS89-extended / LAEA Europe",
                GEOGCS["ETRS89",
                    DATUM["European_Terrestrial_Reference_System_1989",
                        SPHEROID["GRS 1980",6378137,298.257222101,
                            AUTHORITY["EPSG","7019"]],
                        AUTHORITY["EPSG","6258"]],
                    PRIMEM["Greenwich",0,
                        AUTHORITY["EPSG","8901"]],
                    UNIT["degree",0.0174532925199433,
                        AUTHORITY["EPSG","9122"]],
                    AUTHORITY["EPSG","4258"]],
                PROJECTION["Lambert_Azimuthal_Equal_Area"],
                PARAMETER["latitude_of_center",52],
                PARAMETER["longitude_of_center",10],
                PARAMETER["false_easting",4321000],
                PARAMETER["false_northing",3210000],
                UNIT["metre",1,
                    AUTHORITY["EPSG","9001"]],
                AUTHORITY["EPSG","3035"]]'''
        }
    )
    
    # Add global attributes
    ds.attrs.update({
        "Conventions": "CF-1.8",
        "source": "Mock NO2 data for testing",
        "institution": "Test Environment",
        "title": "Mock High-resolution NO2 concentration data",
        "geospatial_bounds_crs": "EPSG:3035",
        "geospatial_lat_min": 34.0,
        "geospatial_lat_max": 72.0,
        "geospatial_lon_min": -11.0,
        "geospatial_lon_max": 45.0,
    })
    
    # Save to file
    ds.to_netcdf(output_path)
    print(f"Created mock NO2 dataset: {output_path}")

def test_extraction():
    """Test the point extraction with mock data."""
    
    # Create mock data
    mock_nc_path = Path("mock_no2_data.nc")
    create_mock_no2_data(mock_nc_path)
    
    # Use your actual points file
    points_path = "converted_with_random_dates.csv"
    
    try:
        print("Testing point extraction...")
        result = extract_point_values(
            netcdf_path=mock_nc_path,
            points_path=points_path,
            variable="no2_downscaled",
            date_col="date",
            days_back=7,
            output_path="test_results.csv"
        )
        
        print(f"Successfully extracted values for {len(result)} points!")
        print("\nFirst 5 results:")
        print(result[["Name", "lon", "lat", "date", "value"]].head())
        
        print(f"\nValue statistics:")
        print(f"Mean: {result['value'].mean():.2f} μg/m³")
        print(f"Min: {result['value'].min():.2f} μg/m³")
        print(f"Max: {result['value'].max():.2f} μg/m³")
        print(f"NaN values: {result['value'].isna().sum()}")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if mock_nc_path.exists():
            mock_nc_path.unlink()

def show_usage_instructions():
    """Show instructions for using with real data."""
    print("\n" + "="*60)
    print("USAGE INSTRUCTIONS FOR YOUR REAL NO2 DATA")
    print("="*60)
    print()
    print("1. Make sure your NO2 NetCDF file is accessible in this Linux environment.")
    print("   You can:")
    print("   - Copy the file to this workspace")
    print("   - Mount the Windows drive")
    print("   - Use a network path")
    print()
    print("2. Use the extract_point_values function like this:")
    print()
    print("```python")
    print("from STanalysis import extract_point_values")
    print()
    print("result = extract_point_values(")
    print("    netcdf_path='path/to/no2_daily_1km_eu.nc',  # Your actual file path")
    print("    points_path='converted_with_random_dates.csv',")
    print("    variable='no2_downscaled',")
    print("    date_col='date',")
    print("    days_back=7,  # Average over 7 days")
    print("    output_path='no2_extracted_values.csv'")
    print(")")
    print("```")
    print()
    print("3. The function will:")
    print("   - Automatically detect the EPSG:3035 projection from your NetCDF file")
    print("   - Transform your WGS84 lat/lon coordinates to the projected coordinates")
    print("   - Extract NO2 values at each point location")
    print("   - Average values over the specified time period")
    print("   - Return a DataFrame with the results")

if __name__ == "__main__":
    print("Testing NO2 point extraction functionality...")
    test_extraction()
    show_usage_instructions()
