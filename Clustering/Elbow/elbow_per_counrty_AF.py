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
from shapely.geometry import Point, Polygon
import json

### This algorithm deducts the optimal number of clusters k using the heuristic elbow mehtod

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
res = 141
# k_range = range(7, 50)

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

## Read EEZ file
EEZ = gpd.read_file("C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/EEZ/Europe/EEZ_Europe_extended_3.geojson")

### Wind
afw = np.loadtxt(AF_wind, delimiter=',')
afw = afw[:-(lenlat-res),:-(lenlon-res)]
afw = list(np.concatenate(afw).flat)

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(afw, geometry=geo)
geometry = frame.geometry

# create countrie dictionary
dict_country = dict()

## make a dictionary with key = country names and values = list with wind values
for country_name in EEZ["UNION"]:
    dict_country[country_name] = list()
    print(country_name)
    for number in range(len(afw)):
        for polygon in EEZ[EEZ["UNION"] == country_name]['geometry']:
            if polygon.contains(geometry.iloc[number]):
                dict_country[country_name].append(afw[number])

assigned = 0
for value in dict_country:
    assigned += len(dict_country[value])
print('Assigned points ', assigned)

## calculate within-cluster sum of squares
wss = dict()
for key, value in dict_country.items():
    wss[key] = sum([(x - np.mean(value)) ** 2 for x in value])
print('within-cluster sum of squares', wss)

# create a DataFrame from the dictionary
df = pd.DataFrame(list(wss.items()), columns=['Countries', 'WSS'])

# save the DataFrame to an Excel file
df.to_excel('elbow_per_country_AF_wind.xlsx', index=False)

## get max and min countries
key_with_max_value = max(wss, key=wss.get)
print('maximum wind', key_with_max_value, wss[key_with_max_value])

key_with_min_value = min(wss, key=wss.get)
print('minmum wind', key_with_min_value, wss[key_with_min_value])


### Sun
afs = np.loadtxt(AF_sun, delimiter=',')
afs = afs[:-(lenlat-res),:-(lenlon-res)]
afs = list(np.concatenate(afs).flat)

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(afs, geometry=geo)
geometry = frame.geometry

# create countrie dictionary
dict_country = dict()

## make a dictionary with key = country names and values = list with wind values
for country_name in EEZ["UNION"]:
    dict_country[country_name] = list()
    print(country_name)
    for number in range(len(afs)):
        for polygon in EEZ[EEZ["UNION"] == country_name]['geometry']:
            if polygon.contains(geometry.iloc[number]):
                dict_country[country_name].append(afs[number])

assigned = 0
for value in dict_country:
    assigned += len(dict_country[value])
print('Assigned points ', assigned)

## calculate within-cluster sum of squares
wss = dict()
for key, value in dict_country.items():
    wss[key] = sum([(x - np.mean(value)) ** 2 for x in value])
print('within-cluster sum of squares', wss)

# create a DataFrame from the dictionary
df = pd.DataFrame(list(wss.items()), columns=['Country', 'WSS'])

# save the DataFrame to an Excel file
df.to_excel('elbow_per_country_AF_sun.xlsx', index=False)

## get max and min countries
key_with_max_value = max(wss, key=wss.get)
print('maximum sun', key_with_max_value, wss[key_with_max_value])

key_with_min_value = min(wss, key=wss.get)
print('minmum sun', key_with_min_value, wss[key_with_min_value])