import netCDF4 as nc
from spopt.region import MaxPHeuristic as MaxP
import matplotlib.pyplot as plt

import libpysal
import matplotlib
import numpy as np
import spopt
import warnings
import geopandas as gpd
import time

# Skip warnings
warnings.filterwarnings("ignore")

# fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
fn_era = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"
AF_wind = "C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/cap_factors_wind.csv"
AF_sun = "C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/cap_factors_sun.csv"

ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456

### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]

## Only select first res values of each for threshold=number of points you should take together
res = 100 #orig 100
threshold = 320 #orig 333
np.random.seed(RANDOM_SEED)

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

afw = np.loadtxt(AF_wind, delimiter=',')
afw = afw[:-(lenlat-res),:-(lenlon-res)]
afw = np. reshape(afw,-1)
afw_copy = afw
afw = [[i] for i in afw]

fig1 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
            c=afw)
plt.title("Availability factors wind")

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(afw, geometry=geo)
frame["count"] = afw_copy
threshold_wind = threshold*np.average(afw_copy)
threshold_wind = int(threshold_wind)
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by MaxP method
attrs_name = "Data"
threshold_name = "count"

print("starting model")
model = MaxP(frame, w, attrs_name, threshold_name, threshold_wind, verbose=True)
model.solve()
print("Model Solved, starting calculations of cluster values")

fig22 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("AF wind clusters, random colors, max-p")
plt.plot()

nr_of_clusters = np.ceil(res*res/threshold)
nr_of_clusters = int(nr_of_clusters)
clusters = dict.fromkeys(range(1,nr_of_clusters))
clusters_values = dict.fromkeys(range(1,nr_of_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()

for i in range(len(model.labels_)):
    clusters[model.labels_[i]].insert(i, i)
    clusters_values[model.labels_[i]].insert(i, afw_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    for i in range(len(clusters[key])):
        afw_copy[clusters[key][i]] = average

print("values relating to specific clusters calculated and ready")

fig3 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=afw_copy)
plt.title("AF wind clusters, ranked with color, max-p")

end_wind = time.time()
print("Computation time (h):")
print((end_wind-start_wind)/3600)

### Sun
start_sun = time.time()

afs = np.loadtxt(AF_sun, delimiter=',')
afs = afs[:-(lenlat-res),:-(lenlon-res)]
afs = np. reshape(afs,-1)
afs_copy = afs
afs = [[i] for i in afs]

fig4 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=afs)
plt.title("Availability factors sun")

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(afs, geometry=geo)
frame["count"] = afs_copy
threshold_sun = threshold*np.average(afs_copy)
threshold_sun = int(threshold_sun)
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by MaxP method
attrs_name = "Data"
threshold_name = "count"

print("starting model")
model = MaxP(frame, w, attrs_name, threshold_name, threshold_sun, verbose=True)
model.solve()
print("Model Solved, starting calculations of cluster values")

fig5 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("AF sun clusters, random colors, max-p")

nr_of_clusters = np.ceil(res*res/threshold)
nr_of_clusters = int(nr_of_clusters)
clusters = dict.fromkeys(range(1,nr_of_clusters))
clusters_values = dict.fromkeys(range(1,nr_of_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()

for i in range(len(model.labels_)):
    clusters[model.labels_[i]].insert(i, i)
    clusters_values[model.labels_[i]].insert(i, afs_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    for i in range(len(clusters[key])):
        afs_copy[clusters[key][i]] = average

print("values relating to specific clusters calculated and ready")

fig6 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=afs_copy)
plt.title("AF sun clusters, ranked with color, max-p")

end_sun = time.time()
print("Computation time sun (h)")
print((end_sun-start_sun)/3600)

plt.show()