"""
Compute Zonal Statistics

For a given polygon and buffer size, compute the mean density of any cells either fully or partially contained within
that polygon.

In this example, we'll be using polygons representing US east coast offshore wind lease areas obtained from BOEM via
their Renewable Energy GIS Data site (https://www.boem.gov/renewable-energy/mapping-and-data/renewable-energy-gis-data).

"""
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# Load the lease area shapefiles
lease_area_shapefile_path = "data/lease_areas/Wind_Lease_Outlines_11_16_2023.shp"

# Import the shapefile to a geodataframe
gdf_lease_areas_all = gpd.read_file(lease_area_shapefile_path)

# Extract a subset that only includes "Commercial" lease types on the east coast
gdf_lease_areas = gdf_lease_areas_all[(gdf_lease_areas_all['LEASE_TYPE'] == 'Commercial') &
                                      (gdf_lease_areas_all['STATE'] != 'CA') &
                                      (gdf_lease_areas_all['STATE'] != 'Louisiana/Texas')]

# This is a lease area selection, hard coded for testing.
lease_area_selection = "OCS-A 0506 - The Narragansett Electric Company"



