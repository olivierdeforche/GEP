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
EEZ = gpd.read_file("C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/EEZ/Europe/EEZ_Europe_merged.geojson")


### Wind
wm = np.average(wm,axis=0)
wm = wm[:-(lenlat-res),:-(lenlon-res)]
wm = list(np.concatenate(wm).flat)

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(wm, geometry=geo)
geometry = frame.geometry

# create countrie dictionary
dict_country = dict()

## make a dictionary with key = country names and values = list with wind values
for country_name in EEZ["UNION"]:
    dict_country[country_name] = list()
    print(country_name)
    for number in range(len(wm)):
        for polygon in EEZ[EEZ["UNION"] == country_name]['geometry']:
            if polygon.contains(geometry.iloc[number]):
                dict_country[country_name].append(wm[number])
print(dict_country)

assigned = 0
for value in dict_country:
    assigned += len(dict_country[value])
print('Assigned points ', assigned)

## calculate within-cluster sum of squares
wss = 0
for key, value in dict_country.items():
    wss += sum([(x - np.mean(value)) ** 2 for x in value])
print('within-cluster sum of squares', wss)


## Sun
id = np.average(id,axis=0)
id = id[:-(lenlat-res),:-(lenlon-res)]
id = list(np.concatenate(id).flat)

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(id, geometry=geo)
geometry = frame.geometry

# create countrie dictionary
dict_country = dict()

## make a dictionary with key = country names and values = list with wind values
for country_name in EEZ["UNION"]:
    dict_country[country_name] = list()
    print(country_name)
    for number in range(len(id)):
        for polygon in EEZ[EEZ["UNION"] == country_name]['geometry']:
            if polygon.contains(geometry.iloc[number]):
                dict_country[country_name].append(id[number])
print(dict_country)

assigned = 0
for value in dict_country:
    assigned += len(dict_country[value])
print('Assigned points ', assigned)

## calculate within-cluster sum of squares
wss = 0
for key, value in dict_country.items():
    wss += sum([(x - np.mean(value)) ** 2 for x in value])
print('within-cluster sum of squares', wss)