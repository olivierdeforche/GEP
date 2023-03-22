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
import csv
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
wm = ds["w"]["wnd100m"][:,:,:] #8760 lists (timesteps 365*24) with 142 lists (lon) with 191 items (lat)
id = ds["w"]["influx_direct"][:,:,:]


## Only select first res values of each for threshold=number of points you should take together
res = 10 # orig 100
n_clusters = 10 # orig 100

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

wm_time = dict.fromkeys(range(1, len(wm)))

for i in range(len(wm)):
    wm_time[i] = list(np.concatenate(wm[i][:-(lenlat-res), :-(lenlon-res)]).flat)

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

frame["ward_new"] = model.labels_
frame["number"] = 1
print(frame[["ward_new", "number"]].groupby(by="ward_new").count())


fig2 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Wind clusters, random colors, Ward HAC")

clusters = dict.fromkeys(range(1, n_clusters))
clusters_values = dict.fromkeys(range(1, n_clusters))
clusters_time = dict.fromkeys(range(1, n_clusters))
clusters_one_time = dict.fromkeys(range(1, n_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()
    clusters_time[i+1] = list()
    clusters_one_time[i+1] = list()

for i in range(len(model.labels_)):
    clusters[model.labels_[i]+1].insert(i, i)
    clusters_values[model.labels_[i]+1].insert(i, wm_copy[i])
    for j in range(len(wm_time)):
        clusters_time[model.labels_[i]+1].insert(i, wm_time[j][i])

for key in clusters:
    for j in range(len(wm_time)):
        average = list()
        for i in range(len(clusters[key])):
            average.insert(i, clusters_time[key][j+8760*i])
        average = np.average(average)
        clusters_one_time[key].insert(j, average)

print(clusters_one_time)
# print(len(clusters_one_time))
# print(len(clusters_one_time[1]))
# print(clusters)
# print(wm_time)
# print(len(wm_time))
# print(len(wm_time[0]))

# clusters_one_time = list()
# for key in clusters:
#     print(key)
#     for i in range(len(clusters[key])):
#         # print(i)
#         # print(len(clusters[key]))
#         for value in clusters[key]:
#             # print(value)
#             for j in range(len(wm_time[i])):
#                 average = list()
#                 for k in range(len(wm_time)):
#                     # print(j)
#                     # print(wm_time[value][j])
#                     average.append(wm_time[j][value])
#                 # print(average)
#                 average = np.average(average)
#                 clusters_one_time[key].insert(j, average)

# clusters_one_time = dict.fromkeys(range(1, n_clusters))
#
# for i in range(len(clusters)):
#     clusters_one_time[i + 1] = list()
#
#
# for key in clusters:
#     for value in clusters[key]:
#         for j in range(len(wm_time[1])):
#             average = list()
#             for i in range(len(wm_time)):
#                 average.append(wm_time[i][value])
#             average = np.average(average)
#             clusters_one_time[key].insert(j, average)

# print(clusters) # dictionary with clusternumbers per cluster
# print(clusters_values) # dictionary with cluster values per cluster
# print(clusters_time) # dictionary with time series per cluster
print(clusters_one_time) # dictionary with one time series per cluster
print(len(clusters_one_time))
print(len(clusters_one_time[1]))

fig3 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm_copy)
plt.title("Wind clusters, ranked with color, Ward HAC")

end_wind = time.time()
print("Computation time (h):")
print((end_wind-start_wind)/3600)




# ### Sun
# start_sun = time.time()
#
# id = np.average(id,axis=0)
# id = id[:-(lenlat-res),:-(lenlon-res)]
# id = list(np.concatenate(id).flat)
# id_copy = id
# id = [[i] for i in id]
#
# fig4 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=id)
# plt.title("Raw sun data")
#
# ## transform to GeoDataFrame
# frame = gpd.GeoDataFrame(id, geometry=geo)
# frame.rename(columns={0:'Data'}, inplace=True )
#
# ## Name data used by Ward method
# attrs_name = ["Data"]
# attrs_name = np.array(attrs_name)
#
# print("starting model")
# model = WardSpatial(frame, w, attrs_name, n_clusters)
# model.solve()
# print("Model Solved, starting calculations of cluster values")
#
# fig5 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=model.labels_)
# plt.title("Sun clusters, random colors, Ward HAC")
#
# clusters = dict.fromkeys(range(1, n_clusters))
# clusters_values = dict.fromkeys(range(1, n_clusters))
#
# for i in range(len(clusters) + 1):
#     clusters[i + 1] = list()
#     clusters_values[i + 1] = list()
#
# for i in range(len(model.labels_)):
#     clusters[model.labels_[i]+1].insert(i, i)
#     clusters_values[model.labels_[i]+1].insert(i, id_copy[i])
#
# for key in clusters:
#     average = np.average(clusters_values[key])
#     for i in range(len(clusters[key])):
#         id_copy[clusters[key][i]] = average
#
# fig6 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=id_copy)
# plt.title("Sun clusters, ranked with color, Ward HAC")
#
# end_sun = time.time()
# print("Computation time (h):")
# print((end_sun-start_sun)/3600)
# plt.show()