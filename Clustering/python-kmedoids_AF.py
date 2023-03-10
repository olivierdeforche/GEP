import kmedoids

import netCDF4 as nc
import libpysal
import numpy as np
import matplotlib.pyplot as plt
import warnings
import time
import unittest

from sklearn.metrics.pairwise import euclidean_distances

# Skip warnings
warnings.filterwarnings("ignore")

# fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
fn_era = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"
AF = "C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/cap_factors_wind.csv"

ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456

### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
# wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]

## Only select first res values of each with nr of clusters
res = 100  #orig 100
medoids = 29
n_clusters = medoids
np.random.seed(RANDOM_SEED)

lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lat = lat[:-(lenlat-res)]

## Transform the lists
lon = np.tile(lon, res)
lat = np.repeat(lat, res)

### Wind
start_wind = time.time()

af = np.loadtxt(AF, delimiter=',')
af = af[:-(lenlat-res),:-(lenlon-res)]
af = np. reshape(af,-1)
af_copy = af
af = [[i] for i in af]

fig1 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=af)
plt.title("Availability factors wind")

af = np.array(af)
diss = euclidean_distances(af)

print("starting model")
model = kmedoids.fasterpam(diss, medoids, max_iter=100, init='random', random_state=None, n_cpu=-1)
print("Model Solved, starting calculations of cluster values")

fig22 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels)
plt.title("AF wind clusters, random colors, k-medoids")

clusters = dict.fromkeys(range(1, n_clusters))
clusters_values = dict.fromkeys(range(1, n_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()

for i in range(len(model.labels)):
    clusters[model.labels[i]+1].insert(i, i)
    clusters_values[model.labels[i]+1].insert(i, af_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    for i in range(len(clusters[key])):
        af_copy[clusters[key][i]] = average

fig3 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=af_copy)
plt.title("AF wind clusters, ranked with color, k-medoids")

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

diss = euclidean_distances(id)

print("starting model")
model = kmedoids.fasterpam(diss, medoids, max_iter=100, init='random', random_state=None, n_cpu=-1)
print("Model Solved, starting calculations of cluster values")

fig5 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels)
plt.title("Sun clusters, random colors, k-medoids")

clusters = dict.fromkeys(range(1, n_clusters))
clusters_values = dict.fromkeys(range(1, n_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()

for i in range(len(model.labels)):
    clusters[model.labels[i]+1].insert(i, i)
    clusters_values[model.labels[i]+1].insert(i, id_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    for i in range(len(clusters[key])):
        id_copy[clusters[key][i]] = average

fig6 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id_copy)
plt.title("Sun clusters, ranked with color, k-medoids")

end_sun = time.time()
print("Computation time (h):")
print((end_sun-start_sun)/3600)
plt.show()