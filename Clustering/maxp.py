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

ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456


### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]


## Only select first res values of each for threshold=number of points you should take together
res = 10 #orig 100
threshold = 23 #orig 333
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

start_wind = time.time()

### Wind
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
frame["count"] = 1
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by MaxP method
attrs_name = "Data"
threshold_name = "count"

print("starting model")
model = MaxP(frame, w, attrs_name, threshold_name, threshold, verbose=True)
model.solve()

print("Model Solved, starting calculations of cluster values")

fig22 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Wind clusters, random colors, max-p")

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
    for i in range(len(clusters[key])):
        wm_copy[clusters[key][i]] = average


print("values relating to specific clusters calculated and ready")

fig3 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm_copy)
plt.title("Wind clusters, ranked with color")

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
frame["count"] = 1
frame.rename(columns={0:'Data'}, inplace=True )

## Name data used by MaxP method
attrs_name = "Data"
threshold_name = "count"


print("starting model")

model = MaxP(frame, w, attrs_name, threshold_name, threshold, verbose=True)
model.solve()

print("Model Solved, starting calculations of cluster values")

fig5 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Sun clusters, random colors, max-p")

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
    for i in range(len(clusters[key])):
        id_copy[clusters[key][i]] = average


print("values relating to specific clusters calculated and ready")

fig6 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=id_copy)
plt.title("Sun clusters, ranked with color, max-p")

end_sun = time.time()
print("Computation time sun (h)")
print((start_sun-end_sun)/3600)

plt.show()