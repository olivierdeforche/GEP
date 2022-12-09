from spopt.region import RegionKMeansHeuristic

import netCDF4 as nc
import geopandas
import libpysal
import numpy as np
import matplotlib.pyplot as plt

fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'

ds = dict()
ds["w"] = nc.Dataset(fn_era)


### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]

## Only select first 50 values of each
res = 10
lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lat = lat[:-(lenlat-res)]

## Transform the lists
lon = np.tile(lon, res)
lat = np.repeat(lat, res)

## flatten
wm = np.average(wm,axis=0)
wm = wm[:-(lenlat-res),:-(lenlon-res)]
print(wm)
wm = list(np.concatenate(wm).flat)
print(wm)

# id = np.average(id,axis=0)
# id = id[:-(lenlat-res),:-(lenlon-res)]
# print(id.shape)
# id = list(np.concatenate(id).flat)


fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.show()

# fig = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=id)
# plt.show()


w = libpysal.weights.lat2W(res, res)



# model = RegionKMeansHeuristic(wm, 20, w)
# model.solve()
# model.labels_
#
# gdf["region"] = model.labels_
# gdf.plot(column="region")
# plt.show()
# print("done")