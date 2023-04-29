import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.ops as so
import cartopy.crs as ccrs
import pandas as pd

def PoliticalRegions(lon, lat, coordinates, resize, user):

    # Load data of Exclusive Economic Zones 
    if user =="Olivier":
        EEZ = gpd.read_file('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/EEZ_Europe_land.geojson')
    else:
        EEZ = gpd.read_file('"C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/EEZ_Europe_land.geojson')

    labels_wind = list()

    j = 0
    for coordinate in coordinates:
        in_europe = False
        previous_length = len(labels_wind)
        for i in range(len(EEZ["geometry"])):
            if EEZ["geometry"][i].contains(coordinate):
                labels_wind.append(i)
                in_europe = True
                break
        if in_europe==False:
            labels_wind.append(36)
        j += 1

    labels_solar = labels_wind.copy()

    areas = np.arange((142//resize) * (191//resize))
    regions_wind = [areas[labels_wind == region] for region in range(len(EEZ["geometry"])+1)]
    regions_solar = [areas[labels_solar == region] for region in range(len(EEZ["geometry"])+1)]
    
    number_of_clusters_wind = len(EEZ["geometry"])+1
    number_of_clusters_solar = len(EEZ["geometry"])+1

    EEZ.plot(edgecolor='k', facecolor='lightgrey')

    fig2 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=labels_wind)
    plt.title("Wind clusters, random colors, Political regions")

    fig5 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=labels_solar)
    plt.title("Sun clusters, random colors, Political regions")


    return(labels_wind, regions_wind, number_of_clusters_wind, labels_solar, regions_solar, number_of_clusters_solar)