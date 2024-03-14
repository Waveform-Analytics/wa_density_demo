""" prep_stats_summary.py

Combine MGEL monthly animal density raster files with BOEM Offshore wind lease area shapefiles to get average monthly
densities in buffered areas around the different lease areas.

"""

import rasterio
from rasterio.mask import mask
from rasterio.plot import show
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
