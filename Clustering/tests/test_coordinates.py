import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd

dataset = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"

ds = dict()
ds["w"] = nc.Dataset(dataset)
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
lenlat = len(lat)
lenlon = len(lon)
print(type(lat))
lat = np.tile(lat, lenlon)
lon = np.repeat(lon,lenlat)

print(lat)
print(lon)
print(len(lat))
print(len(lon))


df = pd.DataFrame(
    {     'Latitude': lat,
        'Longitude': lon})

gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
print(gdf)

coordinates = list(gdf["geometry"])
print(coordinates)