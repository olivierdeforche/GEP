from spopt.region.spenclib.utils import lattice
from spopt.region import RegionKMeansHeuristic
import numpy
import libpysal
import matplotlib.pyplot as plt
import geopandas


libpysal.examples.explain('mexico')
# rsbr = libpysal.examples.get_path("map_RS_BR.shp")
# rsbr_gdf = geopandas.read_file(rsbr)
# print(rsbr_gdf.head())
