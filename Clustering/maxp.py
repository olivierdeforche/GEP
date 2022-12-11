import netCDF4 as nc
from spopt.region import MaxPHeuristic as MaxP
import matplotlib.pyplot as plt

import libpysal
import matplotlib
import numpy as np
import spopt
import warnings
import geopandas as gpd

# Skip warnings
warnings.filterwarnings("ignore")

fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'

ds = dict()
ds["w"] = nc.Dataset(fn_era)


### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]

## Only select first res values of each for threshold=number of points you should take together
res = 100
threshold = 200
lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lat = lat[:-(lenlat-res)]

## Transform the lists
lon = np.tile(lon, res)
lat = np.repeat(lat, res)

## Preperation for GeoDataFrame
geo = gpd.GeoSeries.from_xy(lon, lat)
w = libpysal.weights.lat2W(res, res)

### Wind
wm = np.average(wm,axis=0)
wm = wm[:-(lenlat-res),:-(lenlon-res)]
wm = list(np.concatenate(wm).flat)
wm = [[i] for i in wm]


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.show()

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(wm, geometry=geo)
frame["count"] = 1
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by MaxP method
attrs_name = "Data"
threshold_name = "count"

model = MaxP(frame, w, attrs_name, threshold_name, threshold)
model.solve()

fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.show()





### Sun
id = np.average(id,axis=0)
id = id[:-(lenlat-res),:-(lenlon-res)]
id = list(np.concatenate(id).flat)
id = [[i] for i in id]


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.show()

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(id, geometry=geo)
frame["count"] = 1
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by MaxP method
attrs_name = "Data"
threshold_name = "count"

model = MaxP(frame, w, attrs_name, threshold_name, threshold)
model.solve()

fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.show()