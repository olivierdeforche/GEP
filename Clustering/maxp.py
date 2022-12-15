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
wm_copy = wm
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

print("starting model")
model = MaxP(frame, w, attrs_name, threshold_name, threshold)
model.solve()

print("Model Solved, starting calculations of cluster values")

fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.show()

nr_of_clusters = np.ceil(res*res/threshold)
nr_of_clusters = int(nr_of_clusters)
clusters = dict.fromkeys(range(1,nr_of_clusters))
clusters_values = dict.fromkeys(range(1,nr_of_clusters))

for i in range(len(clusters)+1):
    clusters[i+1] = list()
    clusters_values[i+1] = list()

for i in range(len(model.labels_)):
    clusters[model.labels_[i]].insert(i,i)
    clusters_values[model.labels_[i]].insert(i,wm_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    print(average)
    for i in range(len(clusters[key])):
        wm_copy[clusters[key][i]] = average


print("values relating to specific clusters calculated and ready")

fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm_copy)
plt.show()

### Sun
id = np.average(id,axis=0)
id = id[:-(lenlat-res),:-(lenlon-res)]
id = list(np.concatenate(id).flat)
id_copy = id
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


print("starting model")

model = MaxP(frame, w, attrs_name, threshold_name, threshold)
model.solve()

print("Model Solved, starting calculations of cluster values")

fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.show()

nr_of_clusters = np.ceil(res*res/threshold)
nr_of_clusters = int(nr_of_clusters)
clusters = dict.fromkeys(range(1,nr_of_clusters))
clusters_values = dict.fromkeys(range(1,nr_of_clusters))

for i in range(len(clusters)+1):
    clusters[i+1] = list()
    clusters_values[i+1] = list()

for i in range(len(model.labels_)):
    clusters[model.labels_[i]].insert(i,i)
    clusters_values[model.labels_[i]].insert(i,id_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    print(average)
    for i in range(len(clusters[key])):
        id_copy[clusters[key][i]] = average


print("values relating to specific clusters calculated and ready")

fig = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id_copy)
plt.show()