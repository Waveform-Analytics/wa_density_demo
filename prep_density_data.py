"""
In this script, we're preparing the density data for loading into an Observable
notebook. To simplify things, we're just going to find the density *.img files and
export them to simple csv files.
"""

import rasterio
from rasterio.enums import Resampling
import os
import glob

# First, we'll find all of the data files
density_folder = "data/density"
glob.glob(density_folder)

# Open the .img file
with rasterio.open('path_to_your_file.img') as src:
    # Read the data
    data = src.read()

    # Copy the metadata
    meta = src.meta.copy()

    # Update the metadata for GeoTIFF
    meta.update(driver='GTiff')

    # Write to a new GeoTIFF file
    with rasterio.open('output_filename.tif', 'w', **meta) as dst:
        dst.write(data)

