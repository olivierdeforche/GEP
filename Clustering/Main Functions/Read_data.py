import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def Read_data(data, resize, plot, user, documentation):
    if data=="af":
        if user == "Olivier":
            dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"
        else: 
            dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_lonlat.nc"
    elif data=="weather":
        if user == "Olivier":
            dataset = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
        else:
            dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"

    if documentation:
        print("dataread check")

    ds = dict()
    ds["w"] = nc.Dataset(dataset)

    ### Select smaller range of both datapoints
    if data=="af":
        wm = ds["w"]["wind_af"][:,:,:]
        id = ds["w"]["solar_af"][:,:,:]
        lon = ds["w"]["x"][:]
        lat = ds["w"]["y"][:]
                
    else:
        wm = ds["w"]["wnd100m"][:,:,:]
        id = ds["w"]["influx_direct"][:,:,:]
        lon = ds["w"]["lon"][:]
        lat = ds["w"]["lat"][:]

    ## Only select first res values of each with nr of clusters
    res = 142  
    resize = 1
    res_resized = int(res/resize)

    lenlon = len(lon)
    lenlat = len(lat)
    adjusted_size = lenlon-res
    lon = lon[:-(adjusted_size)]
    lon = lon[0::resize]
    lat = lat[0::resize]

    # Adjust length lon and lat by cutting of left and bottom
    if len(lon) > res_resized:
        lon = lon[1:]
        lat = lat[1:]

    ## Transform the lists
    lon = np.tile(lon, res_resized)
    lat = np.repeat(lat, res_resized)

    # Get list of coordinates
    df = pd.DataFrame(
        {     'Latitude': lat,
            'Longitude': lon})

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    coordinates = list(gdf["geometry"])

  
    # Get time series
    wm_time = dict.fromkeys(range(1, len(wm)))
    id_time = dict.fromkeys(range(1, len(id)))
    for i in range(len(wm)):
        wm_time[i] = wm[i][:, :-(lenlon-res)].flatten()
        id_time[i] = id[i][:, :-(lenlon-res)].flatten()


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
    wm_copy = wm
    wm = [[i] for i in wm]

    if plot:
        fig1 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=wm)
        plt.title("Raw wind data")

    if documentation:
        print("wind resize done")

    ## Solar        
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
    id_copy = id
    id = [[i] for i in id]

    if plot:
        fig4 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=id)
        plt.title("Raw sun data")

    if documentation:
        print("Solar resize done")

    return(wm, wm_copy, wm_time, id, id_copy, id_time, lon, lat, coordinates, res_resized)