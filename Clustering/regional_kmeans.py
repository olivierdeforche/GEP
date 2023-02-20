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

ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456

### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]

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

### Wind
start_wind = time.time()

wm = np.average(wm,axis=0)

wm = wm[:-(lenlat-res),:-(lenlon-res)]
wm = list(np.concatenate(wm).flat)
wm = [[i] for i in wm]

fig1 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.title("Raw wind data")


w = libpysal.weights.lat2W(res, res)

wm = np.array(wm)

model = RegionKMeansHeuristic(wm, clusters, w)
model.solve()


areas = np.arange(res * res)
regions = [areas[model.labels_ == region] for region in range(clusters)]

wm = np.array(wm)
wm = list(np.concatenate(wm).flat)

for i in range(clusters):
    for j in range(len(regions[i])):
        wm[regions[i][j]] = model.centroids_[i]


fig2 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Wind clusters, random colors, kmeans")


fig3 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.title("Wind clusters, ranked with color, kmeans")


end_wind = time.time()
print("Computation time wind (h):")
print((end_wind-start_wind)/3600)

### Sun
start_sun = time.time()

id = np.average(id,axis=0)

id = id[:-(lenlat-res),:-(lenlon-res)]
id = list(np.concatenate(id).flat)
id = [[i] for i in id]


fig4 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.title("Raw sun data")


id = np.array(id)

model = RegionKMeansHeuristic(id, clusters, w)
model.solve()

areas = np.arange(res * res)
regions = [areas[model.labels_ == region] for region in range(clusters)]

id = np.array(id)
id = list(np.concatenate(id).flat)

for i in range(clusters):
    for j in range(len(regions[i])):
        id[regions[i][j]] = model.centroids_[i]

fig5 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Sun clusters, random colors, kmeans")


fig6 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id)
plt.title("Sun clusters, ranked with color, kmeans")

end_sun = time.time()
print("Computation time sun (h)")
print((start_sun-end_sun)/3600)

plt.show()