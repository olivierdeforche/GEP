from sklearn.cluster import KMeans

#from ..BaseClass import BaseSpOptHeuristicSolver
import netCDF4 as nc
from spopt.region import WardSpatial
import matplotlib.pyplot as plt

import libpysal
import matplotlib
import numpy as np
import spopt
import warnings
import csv
import geopandas as gpd
import time
import pandas as pd
import pytest

### This algorithm deducts the optimal number of clusters k using the heuristic elbow mehtod

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
k_range = range(7, 50)

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

# Initialize an empty list to store the WCSS (within-cluster sum of squares) wind values for each k
wcss_wind = []
wcss_test = []

for n_clusters in k_range:
    print("starting model")
    model = KMeans(n_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(wm)
    # model.solve()
    print("Model Solved, starting calculations of cluster values")
    print(model.inertia_)
    wcss_wind.append(model.inertia_)

    clusters_values_wind = {i: [] for i in range(1, n_clusters + 1)}# dictionary with cluster values per cluster
    for i in range(len(clusters_values_wind) + 1):
        clusters_values_wind[i + 1] = list()
    for i in range(len(model.labels_)):
        clusters_values_wind[model.labels_[i]+1].append(wm_copy[i])
    wss = 0
    for key, value in clusters_values_wind.items():
        wss += (sum([(x - np.mean(value)) ** 2 for x in value]))
    wcss_test.append(wss)

end_wind = time.time()
print("Computation time (h):")
print((end_wind-start_wind)/3600)

plt.figure()
plt.plot(k_range, wcss_wind)
plt.xlabel('Number of clusters')
plt.ylabel('Within-cluster sum of squares')
plt.title('Elbow method for optimal k wind')
plt.show(block=False)

plt.figure()
plt.plot(k_range, wcss_test)
plt.xlabel('Number of clusters')
plt.ylabel('Within-cluster sum of squares')
plt.title('Elbow method for optimal k wind, test')
plt.show(block=False)

### Sun
start_sun = time.time()

id = np.average(id,axis=0)
id = id[:-(lenlat-res),:-(lenlon-res)]
id = list(np.concatenate(id).flat)
id_copy = id
id = [[i] for i in id]

wcss_sun = []

for n_clusters in k_range:
    print("starting model")
    model = KMeans(n_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(id)
    print("Model Solved, starting calculations of cluster values")
    wcss_sun.append(model.inertia_)

k = list()
for i in k_range:
    k.append(i)

plt.figure()
plt.plot(k, wcss_sun)
plt.xlabel('Number of clusters')
plt.ylabel('Within-cluster sum of squares')
plt.title('Elbow method for optimal k sun')
plt.show()

end_sun = time.time()
print("Computation time (h):")
print((end_sun-start_sun)/3600)