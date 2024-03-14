""" explore-density-and-zonal-stats.py
Raster data statistics

For a given polygon and buffer size, compute the mean density of any cells either fully or partially contained within
that polygon.

In this example, we'll be looking at polygons representing US east coast offshore wind lease areas obtained from BOEM
via their Renewable Energy GIS Data site
(https://www.boem.gov/renewable-energy/mapping-and-data/renewable-energy-gis-data).

"""
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np


# --------------------- Lease Area Shapefiles --------------------- #

# Load the lease area shapefiles
lease_area_shapefile_path = "data/lease_areas/Wind_Lease_Outlines_11_16_2023.shp"

# Import the shapefile to a geodataframe
gdf_lease_areas_all = gpd.read_file(lease_area_shapefile_path)

# Extract a subset that only includes "Commercial" lease types on the east coast
gdf_lease_areas = gdf_lease_areas_all[(gdf_lease_areas_all['LEASE_TYPE'] == 'Commercial') &
                                      (gdf_lease_areas_all['Shape_Area'] > 0.001) &
                                      (gdf_lease_areas_all['STATE'] != 'CA') &
                                      (gdf_lease_areas_all['STATE'] != 'Louisiana/Texas')]

# Lease area selection, hard-coded for testing.
lease_area_selection = "OCS-A 0486 - Revolution Wind, LLC"

# Buffer size in meters
buffer_size = 10000


# --------------------- Density (raster) files --------------------- #

# Raster file selection, hard-coded for testing
raster_file_path = "data/density_geotiffs/Atlantic_spotted_dolphin.month01.tif"


# --------------------- Zonal Statistics --------------------- #

# The density data and the BOEM polygons are not in the same projection. The density file uses an Albers Equal Area
# projection while the lease area shapefiles are in geographic coordinates (latitude and longitude). We will stick
# with Albers and convert the shapefiles.

# Open the raster data file
with rasterio.open(raster_file_path) as raster_src:
    # Get the CRS (Coordinate Reference System) of the raster data file
    raster_crs = raster_src.crs

    # Extract the selected lease area
    gdf_selected_lease_area = gdf_lease_areas[gdf_lease_areas['LEASE_NU_1'] == lease_area_selection]

    # Reproject the lease area geodatabase
    gdf_selected_lease_area_reprojected = gdf_selected_lease_area.to_crs(raster_crs)

    # mask the raster using the selected lease area polygon
    out_image, out_transform = mask(raster_src, gdf_selected_lease_area_reprojected.geometry, crop=True)
    raster_data = out_image[0]

    # Compute the mean, excluding no data values (assuming they are np.nan or a defined no data value for your raster)
    no_data_value = raster_src.nodata  # Get no data value from raster metadata if available
    if no_data_value is not None:
        mean_value = np.mean(raster_data[raster_data != no_data_value])
    else:
        mean_value = np.mean(raster_data[np.isfinite(raster_data)])

    # ############################################################################################### #
    # ---------- Quickly plot the raster with the polygon, just to check that it looks reasonable --- #
    fig, ax = plt.subplots(figsize=(7, 7))

    # Plot the raster
    show(raster_src, ax=ax)

    # Overlay the polygon(s) from the GeoDataFrame
    gdf_selected_lease_area_reprojected.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)

    plt.show()
