from spopt.region import RegionKMeansHeuristic

import netCDF4 as nc
import libpysal
import numpy as np
import matplotlib.pyplot as plt
import warnings
import time
import cv2


# Skip warnings
warnings.filterwarnings("ignore")

fn_era = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
# fn_era = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"

ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456

### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]

## Only select first res values of each with nr of clusters
res = 142  
resize = 1
clusters = 10 
res_resized = int(res/resize)
np.random.seed(RANDOM_SEED)

lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lon = lon[0::resize]
lat = lat[0::resize]

# Adjust length lon and lat by cutting of left and bottom
if len(lon) > res_resized:
    lon = lon[1:]
    lat = lat[1:]

## Transform the lists
lon = np.tile(lon, res_resized)
lat = np.repeat(lat, res_resized)


### Wind
start_wind = time.time()

# Transform from houry data
wm = np.average(wm,axis=0)

# Make it a square
wm = wm[:lenlat,:lenlon]

i = 0
k = 0
l = 0
wm_resized = [[0 for _ in range(res_resized)] for _ in range(res_resized)]
while i < res and (k < res_resized):
    j = 0
    l = 0
    while (j < res) and (l < res_resized):
        values = wm[i:i+resize,j:j+resize]
        value_list = list(np.concatenate(values).flat)
        wm_resized[k][l] = sum(value_list)/len(value_list)
        j += resize
        l += 1
    k += 1
    i += resize

wm = list(np.concatenate(wm_resized).flat)
wm = [[i] for i in wm]
print("done with resizing wind")


fig1 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.title("Raw wind data")

# # Clustering
# w = libpysal.weights.lat2W(res_resized, res_resized)

# wm = np.array(wm)

# model = RegionKMeansHeuristic(wm, clusters, w)
# model.solve()
# print("Done with clustering wind")

# areas = np.arange(res_resized * res_resized)
# regions = [areas[model.labels_ == region] for region in range(clusters)]

# # Plot clustered zones
# fig2 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=model.labels_)
# plt.title("Wind clusters, random colors, kmeans")

# # Plot clustered zones with respective values
# wm = np.array(wm)
# wm = list(np.concatenate(wm).flat)

# for i in range(clusters):
#     for j in range(len(regions[i])):
#         wm[regions[i][j]] = model.centroids_[i]

# fig3 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=wm)
# plt.title("Wind clusters, ranked with color, kmeans")


# end_wind = time.time()
# print("Computation time wind (h):")
# print((end_wind-start_wind)/3600)

### Sun
start_sun = time.time()

id = np.average(id,axis=0)

# Make it square 
id = id[:lenlat,:lenlon]
i = 0
k = 0
l = 0
id_resized = [[0 for _ in range(res_resized)] for _ in range(res_resized)]
while i < res and (k < res_resized):
    j = 0
    l = 0
    while (j < res) and (l < res_resized):
        values = id[i:i+resize,j:j+resize]
        value_list = list(np.concatenate(values).flat)
        id_resized[k][l] = sum(value_list)/len(value_list)
        j += resize
        l += 1
    k += 1
    i += resize

id = list(np.concatenate(id_resized).flat)
id = [[i] for i in id]
print("done with resizing sun")


fig4 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.title("Raw sun data")

# # Clustering
# id = np.array(id)

# model = RegionKMeansHeuristic(id, clusters, w)
# model.solve()
# print("done with clustering sun")

# areas = np.arange(res_resized * res_resized)
# regions = [areas[model.labels_ == region] for region in range(clusters)]

# id = np.array(id)
# id = list(np.concatenate(id).flat)

# for i in range(clusters):
#     for j in range(len(regions[i])):
#         id[regions[i][j]] = model.centroids_[i]

# fig5 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=model.labels_)
# plt.title("Sun clusters, random colors, kmeans")


# fig6 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=id)
# plt.title("Sun clusters, ranked with color, kmeans")

# end_sun = time.time()
# print("Computation time sun (h)")
# print((start_sun-end_sun)/3600)

plt.show()