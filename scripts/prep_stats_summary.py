""" prep_stats_summary.py

Combine MGEL monthly animal density raster files with BOEM Offshore wind lease area shapefiles to get average monthly
densities in buffered areas around the different lease areas.

The purpose of this script is to end up with a summary table, which is exported to csv. The headers for this table
are: species, lease area, month, buffer_size, and density. These summary stats can then be used as the starting
point for a visualization using any other tool (such as ObservableHQ, Holoviz, Plotly Dash, etc).

"""

import rasterio
from rasterio.mask import mask
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import glob


# --------------------- Define the buffer sizes --------------------- #
buffers = [0, 10000, 50000, 100000] # Buffer sizes in km

# --------------------- Prep animal density files --------------------- #
density_raster_files = glob.glob('data/density_geotiffs/*')

# --------------------- Prep the lease area shapefiles --------------------- #
# Load the lease area shapefiles
lease_area_shapefile_path = "data/lease_areas/Wind_Lease_Outlines_11_16_2023.shp"

# Import the shapefile to a geodataframe
gdf_lease_areas_all = gpd.read_file(lease_area_shapefile_path)

# Extract a subset that only includes "Commercial" lease types on the east coast
gdf_lease_areas = gdf_lease_areas_all[(gdf_lease_areas_all['LEASE_TYPE'] == 'Commercial') &
                                      (gdf_lease_areas_all['Shape_Area'] > 0.001) &
                                      (gdf_lease_areas_all['STATE'] != 'CA') &
                                      (gdf_lease_areas_all['STATE'] != 'Louisiana/Texas')]
