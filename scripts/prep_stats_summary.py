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
import pandas as pd

# --------------------- Define the buffer sizes --------------------- #
buffers = [0, 10000, 50000, 100000] # Buffer sizes in km

# --------------------- Prep animal density files --------------------- #
# We'll work with a subset of species to keep the file size reasonable - and also
# because some species are less likely to occur off the US northeast coast where
# most of the lease areas are.
species_list = ['Atlantic_spotted_dolphin',
                'Atlantic_white_sided_dolphin',
                'Common_bottlenose_dolphin',
                'Common_minke_whale',
                'Fin_whale',
                'Harbor_porpoise',
                'Humpback_whale',
                'North_Atlantic_right_whale',
                'Pilot_whales',
                'Rissos_dolphin',
                'Seals',
                'Sei_whale',
                'Short_beaked_common_dolphin',
                'Sperm_whale']
density_file_path = 'datasets/density_geotiffs/'

# --------------------- Prep the lease area shapefiles --------------------- #
# Load the lease area shapefiles
lease_area_shapefile_path = "datasets/lease_areas/Wind_Lease_Outlines_11_16_2023.shp"

# Import the shapefile to a geodataframe
gdf_lease_areas_all = gpd.read_file(lease_area_shapefile_path)

# Extract a subset that only includes "Commercial" lease types on the east coast
gdf_lease_areas = gdf_lease_areas_all[(gdf_lease_areas_all['LEASE_TYPE'] == 'Commercial') &
                                      (gdf_lease_areas_all['Shape_Area'] > 0.001) &
                                      (gdf_lease_areas_all['STATE'] != 'CA') &
                                      (gdf_lease_areas_all['STATE'] != 'Louisiana/Texas')]

# --------------------- Prep the output lists --------------------- #
species = []
lease_area = []
month = []
buffer_size = []
density = []

# --------------------- Reproject the geodatabase --------------------- #
# Load just the first raster file and get its CRS info
raster_src = rasterio.open('datasets/density_geotiffs/Rissos_dolphin.month06.tif')
# Get the CRS info from the density file
raster_crs = raster_src.crs
# Reproject the lease areas geodatabase
gdf_lease_areas_reprojected = gdf_lease_areas.to_crs(raster_crs)

# --------------------- Loop through shapefiles --------------------- #
for file_idx, species_name in enumerate(species_list):
    for month_num in np.arange(1,13):
        density_file = f"{density_file_path}{species_name}.month{month_num:02d}.tif"
        # Load the raster file
        raster_src = rasterio.open(density_file)
        for area_idx, lease_area_selection in enumerate(gdf_lease_areas_reprojected['LEASE_NU_1']):
            # Select only the polygon corresponding to the current selection
            # lease_areas_selection = area_row['LEASE_NU_1']
            gdf_selected = gdf_lease_areas_reprojected[gdf_lease_areas_reprojected['LEASE_NU_1'] ==
                                                       lease_area_selection]
            for buff in buffers:
                print('species: ' + species_name +
                      ', month: ' + str(month_num) +
                      ', area_idx: ' + lease_area_selection +
                      ', buff: ' + str(buff) + 'm' )

                species.append(species_name)
                lease_area.append(lease_area_selection)
                month.append(month_num)
                buffer_size.append(buff)

                # Create a buffered polygon
                buffered_lease_area = gdf_selected.geometry.buffer(buff)

                # mask the raster using the selected lease area polygon
                try:
                    out_image, _ = mask(raster_src, buffered_lease_area, crop=True)
                    overlap_area = out_image[0]

                    # Compute the mean, excluding no datasets values (assuming they are np.nan or a defined no datasets value for
                    # your raster)
                    no_data_value = raster_src.nodata  # Get no datasets value from raster metadata if available
                    if no_data_value is not None:
                        # Mean value within the buffer area
                        mean_value = np.mean(overlap_area[overlap_area != no_data_value])
                    else:
                        # Mean value within the buffer area
                        mean_value = np.mean(overlap_area[np.isfinite(overlap_area)])
                except:
                    mean_value = np.nan

                density.append(mean_value)

    raster_src.close()

df_out = pd.DataFrame(columns=['species', 'lease_area', 'month', 'buffer_size', 'density'],
                      data=np.array([species, lease_area, month, buffer_size, density]).transpose())

df_out.to_csv('datasets/stats_summary.csv', index=False)


