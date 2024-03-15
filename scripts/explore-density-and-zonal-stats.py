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

    # Created a buffered polygon
    buffered_lease_area = gdf_selected_lease_area_reprojected.geometry.buffer(buffer_size)

    # mask the raster using the selected lease area polygon
    out_image, _ = mask(raster_src, buffered_lease_area, crop=True)
    raster_data = out_image[0]

    # max the buffer area (for plotting color limit extents)
    buffered_plot_area = buffered_lease_area.buffer(buffer_size)
    out_image_for_plotting, _ = mask(raster_src, buffered_plot_area, crop=True)
    raster_plot_area = out_image_for_plotting[0]

    # Compute the mean, excluding no data values (assuming they are np.nan or a defined no data value for your raster)
    no_data_value = raster_src.nodata  # Get no data value from raster metadata if available
    if no_data_value is not None:
        # Mean value within the buffer area
        mean_value = np.mean(raster_data[raster_data != no_data_value])
        # For plot color extents
        min_value = np.min(raster_plot_area[raster_plot_area != no_data_value])
        max_value = np.max(raster_plot_area[raster_plot_area != no_data_value])
    else:
        # Mean value within the buffer area
        mean_value = np.mean(raster_data[np.isfinite(raster_data)])
        # For plot color extents
        min_value = np.min(raster_plot_area[np.isfinite(raster_plot_area)])
        max_value = np.max(raster_plot_area[np.isfinite(raster_plot_area)])

    # ############################################################################################### #
    # ---------- Quickly plot the raster with the polygon, just to check that it looks reasonable --- #
    fig, ax = plt.subplots(figsize=(7, 7), constrained_layout=True)

    # Get the bounds of the buffered polygon for zooming in the plot
    minx, miny, maxx, maxy = buffered_lease_area.iloc[0].bounds
    # Add a buffer around the polygon for spacing in the plot
    plot_buffer_size = maxx - minx

    im = ax.imshow(raster_data, cmap='viridis', vmin=min_value, vmax=max_value,
                   extent=[minx - plot_buffer_size, maxx + plot_buffer_size,
                           miny - plot_buffer_size, maxy + plot_buffer_size], origin='upper')

    ax.set_aspect('equal')
    ax.set_xlabel('Eastings (m)')
    ax.set_ylabel('Northings (m)')
    ax.set_title(lease_area_selection + " - " +
                 f"{buffer_size/1000:.0f}-km buffer\n"
                 f"Mean density inside buffer: " + f"{mean_value:.0e} "
                 f"animals per 100 km$^2$")

    # Overlay the polygon(s) from the GeoDataFrame
    gdf_selected_lease_area_reprojected.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)

    # Overlay the buffered polygon
    buffered_lease_area.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2, linestyle='--')

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.036, pad=0.04)

    # Label the colorbar
    cbar.set_label('Density (animals/100 km$^2$)', rotation=270, labelpad=15)

    buffer_plot_folder = "images/density_buffer_plots"

    plt.savefig(buffer_plot_folder + "/example_buffer_plot.png", bbox_inches='tight')
