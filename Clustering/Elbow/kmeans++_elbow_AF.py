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
AF_wind = "C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/cap_factors_wind.csv"
AF_sun = "C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/cap_factors_sun.csv"

## Read WSS data
df = pd.read_excel('elbow_per_country_AF_wind.xlsx')
print(df)

percentile_50_wind = df['WSS'].quantile(0.5)*32 #summed percentile
average_wind = np.average(df['WSS'])*32 #summed average
print('average wind', average_wind)

# print the result
print('median value wind:', percentile_50_wind)

dw = pd.read_excel('elbow_per_country_AF_sun.xlsx')
print(dw)

# calculate the 95th percentile value of the data column
percentile_50_sun = dw['WSS'].quantile(0.5)*32 #summed percentile
print('percentile sun', percentile_50_sun)
average_sun = np.average(dw['WSS'])*32 #summed average
print('average sun', average_sun)

# print the result
print('5th percentile value sun:', percentile_50_sun)

ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456

### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]

## Only select first res values of each for threshold=number of points you should take together
k_range = range(2, 30)

lenlon = len(lon)
lenlat = len(lat)

## Transform the lists
lon = np.tile(lon, lenlat)
lat = np.repeat(lat, lenlon)

## Preperation for GeoDataFrame
geo = gpd.GeoSeries.from_xy(lon, lat)
w = libpysal.weights.lat2W(lenlon, lenlat)

### Wind
start_wind = time.time()

afw = np.loadtxt(AF_wind, delimiter=',')
afw = np.reshape(afw,-1)
afw_copy = afw
afw = [[i] for i in afw]

fig1 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
            c=afw)
plt.title("Availability factors wind")

# Initialize an empty list to store the WCSS (within-cluster sum of squares) wind values for each k
wcss_wind = []
wcss_test = []

for n_clusters in k_range:
    print("starting model")
    model = KMeans(n_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(afw)
    # model.solve()
    print("Model Solved, starting calculations of cluster values")
    print(model.inertia_)
    wcss_wind.append(model.inertia_)

    clusters_values_wind = {i: [] for i in range(1, n_clusters + 1)}# dictionary with cluster values per cluster
    for i in range(len(clusters_values_wind) + 1):
        clusters_values_wind[i + 1] = list()
    for i in range(len(model.labels_)):
        clusters_values_wind[model.labels_[i]+1].append(afw_copy[i])
    wss = 0
    for key, value in clusters_values_wind.items():
        wss += (sum([(x - np.mean(value)) ** 2 for x in value]))
    wcss_test.append(wss)

end_wind = time.time()
print("Computation time (h):")
print((end_wind-start_wind)/3600)

# WCSS = dict()
# for key in df:
#     WCSS[key] = list()
#     for i in range(len(k_range)):
#         WCSS[key].append(df[key])

plt.figure()
plt.plot(k_range, wcss_wind)
# for key in WCSS:
#         plt.plot(k_range, WCSS[key])
plt.xlabel('Number of clusters')
plt.ylabel('Within-cluster sum of squares')
plt.title('Elbow method for optimal k wind')
plt.show(block=False)

percentile_50_list = list()
average_wind_list = list()
for i in range(len(k_range)):
    percentile_50_list.append(percentile_50_wind)
    average_wind_list.append(average_wind)

plt.figure()
plt.plot(k_range, wcss_test,color='black')
plt.plot(k_range,percentile_50_list,color='red')
plt.plot(k_range,average_wind_list,color='blue')
plt.xlabel('Number of clusters')
plt.ylabel('Within-cluster sum of squares')
plt.title('Elbow method for optimal k wind, test')
plt.show(block=False)

### Sun
start_sun = time.time()

afs = np.loadtxt(AF_sun, delimiter=',')
afs = list(np.concatenate(afs).flat)
afs_copy = afs
afs = [[i] for i in afs]

fig4 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=afs)
plt.title("Availability factors sun")

wcss_sun = []

for n_clusters in k_range:
    print("starting model")
    model = KMeans(n_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(afs)
    print("Model Solved, starting calculations of cluster values")
    wcss_sun.append(model.inertia_)

k = list()
for i in k_range:
    k.append(i)

percentile_50_list = list()
average_sun_list = list()
for i in range(len(k_range)):
    percentile_50_list.append(percentile_50_sun)
    average_sun_list.append(average_sun)

plt.figure()
plt.plot(k, wcss_sun,color='black')
plt.plot(k_range,percentile_50_list,color='red')
plt.plot(k_range,average_sun_list,color='blue')
plt.xlabel('Number of clusters')
plt.ylabel('Within-cluster sum of squares')
plt.title('Elbow method for optimal k sun')
plt.show()

end_sun = time.time()
print("Computation time (h):")
print((end_sun-start_sun)/3600)
plt.show()