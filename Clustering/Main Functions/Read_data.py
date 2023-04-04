import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

def Read_data(data, resize, plot, user):
    if data=="af":
        if user == "Olivier":
            solar_data = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_solar.nc"
            wind_data = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_wind.nc"
            dataset = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
        else: 
            solar_data = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_solar.nc"
            wind_data = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Capacity_factor_wind.nc"
            dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"
    else:
        if user == "Olivier":
            dataset = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
        else:
            dataset = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"

    ds = dict()
    ds["w"] = nc.Dataset(dataset)
    solar = nc.Dataset(solar_data)
    wind = nc.Dataset(wind_data)

    ### Select smaller range of both datapoints
    lon = ds["w"]["lon"][:]
    lat = ds["w"]["lat"][:]

    if data=="af":
        wm = solar[:,:]
        id = wind[:,:]
                
    else:
        wm = ds["w"]["wnd100m"][:,:,:]
        id = ds["w"]["influx_direct"][:,:,:]

    ## Only select first res values of each with nr of clusters
    res = 142  
    resize = 1
    clusters = 10 
    res_resized = int(res/resize)

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
        print("done with resizing wind")

        if plot:
            fig1 = plt.figure(figsize=(6, 6))
            plt.scatter(lon, lat,
                    c=wm)
            plt.title("Raw wind data")

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
    print("done with resizing sun")

    if plot:
        fig4 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=id)
        plt.title("Raw sun data")

    return(wm, wm_copy, id, id_copy, lon, lat, res_resized)