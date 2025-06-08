"""Example demonstrating how to use the point extraction functionality."""
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
from STanalysis import extract_point_values

# Create a sample NetCDF file with some environmental data
# Here we create a simple grid with temperature data
def create_sample_netcdf(output_path: Path) -> None:
    # Create sample data
    times = pd.date_range("2024-06-01", "2024-06-30")  # 30 days of data
    lats = np.linspace(53.0, 54.0, 11)  # Bremen area
    lons = np.linspace(8.5, 9.5, 11)
    
    # Create some sample temperature data
    temp_data = np.random.normal(20, 5, size=(len(times), len(lats), len(lons)))
    
    # Create the dataset
    ds = xr.Dataset(
        {
            "temperature": (("time", "lat", "lon"), temp_data),
        },
        coords={
            "time": times,
            "lat": lats,
            "lon": lons,
        },
    )
    
    # Save to NetCDF file
    ds.to_netcdf(output_path)

# Create sample points (some locations in Bremen)
def create_sample_points(output_path: Path) -> None:
    points = pd.DataFrame({
        "name": ["Bremen City", "Bremen North", "Bremen University"],
        "lat": [53.0793, 53.1680, 53.1084],
        "lon": [8.8017, 8.6317, 8.8538],
        "date": ["2024-06-08", "2024-06-15", "2024-06-30"]
    })
    points.to_csv(output_path, index=False)

def main():
    # Create the example data directory
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Create sample data files
    netcdf_path = data_dir / "temperature.nc"
    points_path = data_dir / "measurement_points.csv"
    output_path = data_dir / "extracted_values.csv"
    
    # print("Creating sample NetCDF file...")
    # create_sample_netcdf(netcdf_path)
    
    # print("Creating sample points file...")
    # create_sample_points(points_path)
    
    print("Extracting values at points...")
    result_df = extract_point_values(
        netcdf_path=netcdf_path,
        points_path=points_path,
        variable="temperature",
        days_back=2,  # Average over the last 2 days
        date_col="date",
        output_path=output_path
    )
    
    print("\nExtracted values:")
    print(result_df[["name", "lat", "lon", "value"]].to_string())
    print(f"\nResults have been saved to: {output_path}")

if __name__ == "__main__":
    main()
