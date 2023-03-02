from sklearn.cluster import AgglomerativeClustering

#from ..BaseClass import BaseSpOptHeuristicSolver
import netCDF4 as nc
from spopt.region import WardSpatial
import matplotlib.pyplot as plt

import libpysal
import matplotlib
import numpy as np
import spopt
import warnings
import geopandas as gpd
import time

import pytest

# Skip warnings
warnings.filterwarnings("ignore")

# fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
fn_era = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"


ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456


### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]


## Only select first res values of each for threshold=number of points you should take together
res = 100
n_clusters = 30

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
start_wind = time.time()

wm = np.average(wm,axis=0)
wm = wm[:-(lenlat-res),:-(lenlon-res)]
wm = list(np.concatenate(wm).flat)
wm_copy = wm
wm = [[i] for i in wm]

fig1 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
            c=wm)
plt.title("Raw wind data")

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(wm, geometry=geo)

#frame["count"] = 1
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by Ward method
attrs_name = ["Data"]
attrs_name = np.array(attrs_name)

#spatial weights
w = libpysal.weights.lat2W(res, res)

print("starting model")
model = WardSpatial(frame, w, attrs_name, n_clusters)
model.solve()
print("Model Solved, starting calculations of cluster values")

fig2 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Wind clusters, random colors, Ward HAC")

clusters = dict.fromkeys(range(1, n_clusters))
clusters_values = dict.fromkeys(range(1, n_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()


for i in range(len(model.labels_)):
    clusters[model.labels_[i]+1].insert(i, i)
    clusters_values[model.labels_[i]+1].insert(i, wm_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    for i in range(len(clusters[key])):
        wm_copy[clusters[key][i]] = average

fig3 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm_copy)
plt.title("Wind clusters, ranked with color, Ward HAC")

end_wind = time.time()
print("Computation time (h):")
print((end_wind-start_wind)/3600)


### Sun
start_sun = time.time()

id = np.average(id,axis=0)
id = id[:-(lenlat-res),:-(lenlon-res)]
id = list(np.concatenate(id).flat)
id_copy = id
id = [[i] for i in id]

fig4 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.title("Raw sun data")

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(id, geometry=geo)
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by Ward method
attrs_name = ["Data"]
attrs_name = np.array(attrs_name)

print("starting model")
model = WardSpatial(frame, w, attrs_name, n_clusters)
model.solve()
print("Model Solved, starting calculations of cluster values")

fig5 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Sun clusters, random colors, Ward HAC")

clusters = dict.fromkeys(range(1, n_clusters))
clusters_values = dict.fromkeys(range(1, n_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()

for i in range(len(model.labels_)):
    clusters[model.labels_[i]+1].insert(i, i)
    clusters_values[model.labels_[i]+1].insert(i, id_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    for i in range(len(clusters[key])):
        id_copy[clusters[key][i]] = average

fig6 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id_copy)
plt.title("Sun clusters, ranked with color, Ward HAC")
plt.show()

end_wind = time.time()
print("Computation time (h):")
print((end_wind-start_wind)/3600)