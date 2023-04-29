import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def Read_data(data, resize, plot, user, documentation):
    if resize==1:
        if data=="af":
            if user == "Olivier":
                dataset_clusters = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"
                dataset = dataset_clusters
            else: 
                dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_lonlat.nc"
                dataset = dataset_clusters
        elif data=="weather":
            if user == "Olivier":
                dataset_clusters = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
                dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"
            else:
                dataset_clusters = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"
                dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_lonlat.nc"
    
    if resize==2:
        if user == "Olivier":
            dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat_resize2.nc"
        else: 
            dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_lonlat_resize2.nc"
        dataset_clusters = dataset

    if resize==3:
        if user == "Olivier":
            dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat_resize3.nc"
        else: 
            dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_lonlat_resize3.nc"
        dataset_clusters = dataset
        
    if resize==4:
        if user == "Olivier":
            dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat_resize4.nc"
        else: 
            dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_lonlat_resize4.nc"
        dataset_clusters = dataset



    if documentation:
        print("dataread check")


    # Select data that will be used to calculate the data of the clusters
    dss = dict()
    dss["w"] = nc.Dataset(dataset)
    wmm = dss["w"]["wind_af"][:,:,:]
    idd = dss["w"]["solar_af"][:,:,:]

    ds = dict()
    ds["w"] = nc.Dataset(dataset_clusters)
    
    # Select data that will be used to form the clusters
    if data=="af":
        wm = ds["w"]["wind_af"][:,:,:]
        id = ds["w"]["solar_af"][:,:,:]
        if resize==1:
            lon = ds["w"]["x"][:]
            lat = ds["w"]["y"][:]
        else:
            lon = ds["w"]["lon"][:]
            lat = ds["w"]["lat"][:]            
                
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
    # adjusted_size = lenlon-res
    # lon = lon[:-(adjusted_size)]
    # lon = lon[0::resize]
    # lat = lat[0::resize]

    # # Adjust length lon and lat by cutting of left and bottom
    # if len(lon) > res_resized:
    #     lon = lon[1:]
    #     lat = lat[1:]

    ## Transform the lists
    lon = np.tile(lon, lenlat)
    lat = np.repeat(lat, lenlon)

    # Get list of coordinates
    df = pd.DataFrame({'Latitude': lat,'Longitude': lon})

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    coordinates = list(gdf["geometry"])
  
    # Get time series of AF
    wm_time = dict.fromkeys(range(1, len(wmm)))
    id_time = dict.fromkeys(range(1, len(idd)))
    for i in range(len(wmm)):
        wm_time[i] = wmm[i][:, :].flatten()
        id_time[i] = idd[i][:, :].flatten()


    # Transform from houry data
    wm = np.average(wm,axis=0)

    # Make it a square
    wm = wm[:,:]

    wm = list(np.concatenate(wm).flat)
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
    id = id[:,:]
    
    id = list(np.concatenate(id).flat)
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