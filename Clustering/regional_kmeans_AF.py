from spopt.region import RegionKMeansHeuristic

import netCDF4 as nc
import libpysal
import numpy as np
import matplotlib.pyplot as plt
import warnings
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

## Only select first res values of each with nr of clusters
res = 100  #orig 100
clusters = 30 #orig 30
np.random.seed(RANDOM_SEED)

lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lat = lat[:-(lenlat-res)]

## Transform the lists
lon = np.tile(lon, res)
lat = np.repeat(lat, res)

# ### Wind
# start_wind = time.time()
#
# afw = np.loadtxt(AF_wind, delimiter=',')
# afw = afw[:-(lenlat-res),:-(lenlon-res)]
# afw = np. reshape(afw,-1)
# afw_copy = afw
# afw = [[i] for i in afw]
#
# fig1 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#             c=afw)
# plt.title("Availability factors wind")
#
# w = libpysal.weights.lat2W(res, res)
#
# afw = np.array(afw)
#
# print("starting model")
# model = RegionKMeansHeuristic(afw, clusters, w)
# model.solve()
# print("Model Solved, starting calculations of cluster values")
#
# areas = np.arange(res * res)
# regions = [areas[model.labels_ == region] for region in range(clusters)]
#
# afw = np.array(afw)
# afw = list(np.concatenate(afw).flat)
#
# for i in range(clusters):
#     for j in range(len(regions[i])):
#         afw[regions[i][j]] = model.centroids_[i]
#
# fig2 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=model.labels_)
# plt.title("AF wind clusters, random colors, regional kmeans")
#
# fig3 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=afw)
# plt.title("AF wind clusters, ranked with color, regional kmeans")
#
# end_wind = time.time()
# print("Computation time wind (h):")
# print((end_wind-start_wind)/3600)
# # plt.show()

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

afs = np.array(afs)

model = RegionKMeansHeuristic(afs, clusters, w)
model.solve()

areas = np.arange(res * res)
regions = [areas[model.labels_ == region] for region in range(clusters)]

afs = np.array(afs)
afs = list(np.concatenate(afs).flat)

for i in range(clusters):
    for j in range(len(regions[i])):
        afs[regions[i][j]] = model.centroids_[i]

fig5 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("AF Sun clusters, random colors, regional kmeans")

fig6 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=afs)
plt.title("AF Sun clusters, ranked with color, regional kmeans")

end_sun = time.time()
print("Computation time sun (h)")
print((end_sun-start_sun)/3600)
plt.show()