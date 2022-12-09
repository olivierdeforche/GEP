import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from spopt.region import RegionKMeansHeuristic

import geopandas as gdp
import libpysal as lp
import warnings

# Skip warnings
warnings.filterwarnings("ignore")

fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
fn_sara = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-sarah.nc'

ds = dict()
ds["w"] = nc.Dataset(fn_era)
ds["s"] = nc.Dataset(fn_sara)


### Solar radiation
lon = ds["s"]["lon"][:]
lat = ds["s"]["lat"][:]
id = ds["s"]["influx_direct"][:,:,:]

lon = np.tile(lon, 162)

lat = lat[:-48]
lat = np.repeat(lat, 285)

id = np.average(id,axis=0)
id = id[:-48,:]
id = list(np.concatenate(id).flat)


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.show()


### Windspeed
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
id = ds["w"]["influx_direct"][:,:,:]

lon = np.tile(lon, 142)
lat = np.repeat(lat, 191)
id = np.average(id,axis=0)
id = list(np.concatenate(id).flat)


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.show()


### Windspeed
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]

lon = np.tile(lon, 142)
lat = np.repeat(lat, 191)
wm = np.average(wm,axis=0)
wm = list(np.concatenate(wm).flat)


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.show()


### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]

## Only select first 50 values of each
lon = lon[:-141]
lat = lat[:-92]

## Transform the lists
lon = np.tile(lon, 50)
lat = np.repeat(lat, 50)

## flatten
wm = np.average(wm,axis=0)
wm = wm[:-92,:-141]
wm = list(np.concatenate(wm).flat)

id = np.average(id,axis=0)
id = id[:-92,:-141]
print(id.shape)
id = list(np.concatenate(id).flat)


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.show()

fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.show()