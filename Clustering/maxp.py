import netCDF4 as nc
from spopt.region import MaxPHeuristic as MaxP
import matplotlib.pyplot as plt

import geopandas
import libpysal
import matplotlib
import numpy as np
import spopt
import warnings

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

## Only select first 50 values of each
res = 100
clusters = 50
lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lat = lat[:-(lenlat-res)]

## Transform the lists
lon = np.tile(lon, res)
lat = np.repeat(lat, res)

### Wind
wm = np.average(wm,axis=0)
wm = wm[:-(lenlat-res),:-(lenlon-res)]
wm = list(np.concatenate(wm).flat)
wm = [[i] for i in wm]


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
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