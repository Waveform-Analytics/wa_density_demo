"""
In this script, we're preparing the density data for loading into an Observable
notebook. To simplify things, we're just going to find the density *.img files and
export them to geotiff

"""

import rasterio
import os
import glob
from collections import Counter
import numpy as np

# First, we'll find all of the data files
density_folder = "data/density"
species_folders = [path for path in glob.glob(os.path.join(density_folder, '*')) if os.path.isdir(path)]

# Use glob to find all .img files in all subdirectories
all_img_files = glob.glob(f'{density_folder}/**/*.img', recursive=True)

# Filter for files that contain the word "density"
density_img_files = [file for file in all_img_files if 'density' in os.path.basename(file)]

# Get species name from the path
species_name = [filepath.split('/')[2].split('_v')[0] for filepath in density_img_files]

# Most species have a density file for each month, but not all. In cases where it's not
# exactly 12 density files, we'll need to do something different.
count_of_species = Counter(species_name)


# Define a function to read in the img file and save it to geotiff
def img_to_geotiff(input_file_path, output_file_path):
    """
    Convert ERDAS Imagine files to geotiff

    Args:
        input_file_path (str): Path to *.img file
        output_file_path (str): Path to *.tif file

    Returns: None

    """
    with rasterio.open(input_file_path) as src:
        # Read the data
        data = src.read()
        # Copy the metadata
        meta = src.meta.copy()
        # Update the metadata for GeoTIFF
        meta.update(driver='GTiff')
        # Write to a new GeoTIFF file
        with rasterio.open(output_file_path, 'w', **meta) as dst:
            dst.write(data)

# If you look at "count_of_species", you can see that several species have only 1 file, and are
# simple annual averages. In that case we will make a separate file for each month that's
# a copy of the annual file (this is for plotting purposes). Two species have 36 files:
# humpback whale and North Atlantic right whale. These are special cases that have explanations
# in the readme file. For Humpback whales, the authors recommend using the 2009-2019 files.
# For NARW, they recommend using 2010-2019.

species = 'test spp'
month_number = '04'
test = f"{species}.month{month_number}.tif"

for density_file, spp_name in zip(density_img_files, species_name):

    # There are 12 months of density data available
    if count_of_species.get(spp_name)==12:
        month_number = density_file.split('month')[1].split('.img')[0]
        out_file = f"data/density_geotiffs/{spp_name}.month{month_number}.tif"
        img_to_geotiff(density_file, out_file)

    # There's only an annual average
    elif count_of_species.get(spp_name)==1:
        for month_num_val in np.arange(1,13):
            out_file = f"data/density_geotiffs/{spp_name}.month{month_num_val:02}.tif"
            img_to_geotiff(density_file, out_file)

    # Humpback whale - special case
    elif spp_name == 'Humpback_whale':
        if "2009_2019" in density_file:
            month_number = density_file.split('month')[1].split('.img')[0]
            out_file = f"data/density_geotiffs/{spp_name}.month{month_number}.tif"
            img_to_geotiff(density_file, out_file)

    # NARW - special case
    elif spp_name == 'North_Atlantic_right_whale':
        if "2010-2019" in density_file:
            month_number = density_file.split('month')[1].split('.img')[0]
            out_file = f"data/density_geotiffs/{spp_name}.month{month_number}.tif"
            img_to_geotiff(density_file, out_file)

    else:
        print('Error! This file was not handled: ' + density_file)
