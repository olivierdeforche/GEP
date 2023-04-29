import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


# def save_nc_file(resize=2):
#     # Select data that will be used to calculate the data of the clusters
#     ds = dict()
#     dataset_clusters = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
#     dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"
#     ds["w"] = nc.Dataset(dataset)

#     ds["ww"] = nc.Dataset(dataset_clusters)
#     wmw = ds["ww"]["wnd100m"][:,:,:]
#     idw = ds["ww"]["influx_direct"][:,:,:]
#     wm = ds["w"]["wind_af"][:,:,:]
#     id = ds["w"]["solar_af"][:,:,:]

#     lon = ds["w"]["x"][:]
#     lat = ds["w"]["y"][:]
#     wmm = wm
#     ## Only select first res values of each with nr of clusters
#     plt.show()
#     lenlon = len(lon)
#     lenlat = len(lat)


#     res_resized_lon = int(lenlat//resize)
#     res_resized_lat = int(lenlon//resize)

#     if lenlon%resize != 0:
#         lon = lon[:-(lenlon%resize)]
#     if lenlat%resize != 0:
#         lat = lat[:-(lenlat%resize)]
#     lon = lon[0::resize]
#     lat = lat[0::resize]
#     lonl = lon
#     latl = lat

#     lenlonn = len(lon)
#     lenlatt = len(lat) 

#     ## Transform the lists
#     lon = np.tile(lon, lenlat)
#     lat = np.repeat(lat, lenlon)


#     wm_resized = [[0 for _ in range(res_resized_lat)] for _ in range(res_resized_lon)]
#     wmw_resized = [[0 for _ in range(res_resized_lat)] for _ in range(res_resized_lon)]
#     id_resized = [[0 for _ in range(res_resized_lat)] for _ in range(res_resized_lon)]
#     idw_resized = [[0 for _ in range(res_resized_lat)] for _ in range(res_resized_lon)]

#     wm_time = list()
#     wmw_time = list()
#     id_time = list()
#     idw_time = list()    

#     fn = str("C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat_resize")+str(resize)+str(".nc")
#     dss = Dataset(fn, mode='w', format='NETCDF4_CLASSIC')
#     time_dim = dss.createDimension('time', 8760)
#     lat_dim = dss.createDimension('lat', lenlatt)
#     lon_dim = dss.createDimension('lon', lenlonn)
    

#     time_ds = dss.createVariable('time', 'f4', ('time',))
#     lat_ds = dss.createVariable('lat', 'f4', ('lat',))
#     lon_ds = dss.createVariable('lon', 'f4', ('lon',))
#     solar_af = dss.createVariable('solar_af', 'f4', ('time', 'lat', 'lon',))
#     solar_af.units = 'AF'
#     wind_af = dss.createVariable('wind_af', 'f4', ('time', 'lat', 'lon',))
#     wind_af.units = 'AF'
#     wnd100m = dss.createVariable('wnd100m', 'f4', ('time', 'lat', 'lon',))
#     influx_direct = dss.createVariable('influx_direct', 'f4', ('time', 'lat', 'lon',))

#     time_era = ds["w"]["time"][:]

#     lat_ds[:] = latl
#     lon_ds[:] = lonl
#     time_ds[:] = time_era

#     for m in range(len(wmm)):
#         k = 0
#         i = 0
#         while k  < lenlatt:
#             l = 0
#             j = 0
#             while l < lenlonn:
#                 values = wm[m,i:i+resize,j:j+resize].tolist()
#                 value_list = np.concatenate(values).flat
#                 wm_resized[k][l] = np.sum(value_list)/np.size(value_list)

#                 values = wmw[m,i:i+resize,j:j+resize].tolist()
#                 value_list = np.concatenate(values).flat
#                 wmw_resized[k][l] = np.sum(value_list)/np.size(value_list)

#                 values = id[m,i:i+resize,j:j+resize].tolist()
#                 value_list = np.concatenate(values).flat
#                 id_resized[k][l] = np.sum(value_list)/np.size(value_list)

#                 values = idw[m,i:i+resize,j:j+resize].tolist()
#                 value_list = np.concatenate(values).flat
#                 idw_resized[k][l] = np.sum(value_list)/np.size(value_list)

#                 j += resize
#                 l += 1

#             i += resize
#             k += 1
#             solar_af[m,:,:] = id_resized
#             wind_af[m,:,:] = wm_resized
#             wnd100m[m,:,:] = wmw_resized
#             influx_direct[m,:,:] = idw_resized 
#         print(m)

#     print(solar_af[1:24,:,:])

#     print("yes")

#     dss.close()

#     return()

# save_nc_file(2)
# save_nc_file(3)
# save_nc_file(4)

    # for t in range(len(time_era)):
    #     for la in range(lenlatt):
    #         solar_af[t,la,:] = id_time[t][la]
    #         wind_af[t,la,:] = wm_time[t][la]
    #         wnd100m[t,la,:] = idw_time[t][la]
    #         influx_direct[t,la,:] = wmw_time[t][la]

    # wm = wind_af[:,:,:]
    # id = solar_af[1:24,:,:]
    # print(wm)
    # print(id)





    # fn = str("C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat_resize")+str("_weather_")+str(resize)+str(".nc")
    # dss = Dataset(fn, mode='w', format='NETCDF4_CLASSIC')
    # time_dim = dss.createDimension('time', 8760)
    # lat_dim = dss.createDimension('lat', lenlatt)
    # lon_dim = dss.createDimension('lon', lenlonn)


    # time_ds = dss.createVariable('time', 'f4', ('time',))
    # lat_ds = dss.createVariable('lat', 'f4', ('lat',))
    # lon_ds = dss.createVariable('lon', 'f4', ('lon',))

    # # wm = ds["ww"]["wnd100m"][:,:,:]
    # # id = ds["ww"]["influx_direct"][:,:,:]
    
    # wnd100m = dss.createVariable('wnd100m', 'f4', ('time', 'lat', 'lon',))
    # influx_direct = dss.createVariable('influx_direct', 'f4', ('time', 'lat', 'lon',))

    # time_era = ds["w"]["time"][:]

    # lat_ds[:] = latl
    # lon_ds[:] = lonl
    # time_ds[:] = time_era

    # for t in range(len(time_era)):
    #     for la in range(lenlatt):
    #         wnd100m[t,la,:] = wmw_time[t][la]
    #         influx_direct[t,la,:] = idw_time[t][la]
    # # wm  = wnd100m[:,:,:]
    # # id = influx_direct[1:24,:,:]
    # # print(wm)
    # # print(id)
    
    # print("yes")
    # dss.close()

# save_nc_file(4)
# save_nc_file(3)
# save_nc_file(2)




dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat_resize4.nc"
# dataset_clusters = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat_resize_weather_4.nc"
dss = dict()
dss["w"] = nc.Dataset(dataset)
wmm = dss["w"]["wind_af"][:,:,:]
idd = dss["w"]["solar_af"][:,:,:]

print(idd[1:24,1,1])
wmm = dss["w"]["wnd100m"][:,:,:]
idd = dss["w"]["influx_direct"][:,:,:]

print(idd[1:24,1,1])

# print(wmm)
# print(idd[12,20,:])
# dsd = dict()
# dss["w"] = nc.Dataset(dataset_clusters)
# wmm = dss["w"]["wnd100m"][:,:,:]
# idd = dss["w"]["influx_direct"][:,:,:]
# print(wmm)



# # # Get time series of AF
# # wm_time = dict.fromkeys(range(1, len(wmm)))
# # id_time = dict.fromkeys(range(1, len(idd)))
# # for i in range(len(wmm)):
# #     wm_time[i] = wmm[i][:, :].flatten()
# #     id_time[i] = idd[i][:, :].flatten()

# # print(wm_resized)
# # print(len(wm_resized))
# # print(len(wm_resized[0]))

# # while i < res and (k < res_resized):
# #     j = 0
# #     l = 0
# #     while (j < res) and (l < res_resized):
# #         values = wm[i:i+resize,j:j+resize]
# #         value_list = list(np.concatenate(values).flat)
# #         wm_resized[k][l] = sum(value_list)/len(value_list)
# #         j += resize
# #         l += 1
# #     k += 1
# #     i += resize


# # # Get list of coordinates
# # df = pd.DataFrame(
# #     {     'Latitude': lat,
# #         'Longitude': lon})

# # gdf = gpd.GeoDataFrame(
# #     df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
# # coordinates = list(gdf["geometry"])


# # # Get time series of AF
# # wm_time = dict.fromkeys(range(1, len(wmm)))
# # id_time = dict.fromkeys(range(1, len(idd)))
# # for i in range(len(wmm)):
# #     wm_time[i] = wmm[i][:, :-(lenlon-res)].flatten()
# #     id_time[i] = idd[i][:, :-(lenlon-res)].flatten()


# # # Transform from houry data
# # wm = np.average(wm,axis=0)

# # # Make it a square
# # wm = wm[:lenlat,:lenlon]

# # i = 0
# # k = 0
# # l = 0
# # wm_resized = [[0 for _ in range(res_resized)] for _ in range(res_resized)]
# # while i < res and (k < res_resized):
# #     j = 0
# #     l = 0
# #     while (j < res) and (l < res_resized):
# #         values = wm[i:i+resize,j:j+resize]
# #         value_list = list(np.concatenate(values).flat)
# #         wm_resized[k][l] = sum(value_list)/len(value_list)
# #         j += resize
# #         l += 1
# #     k += 1
# #     i += resize

# # wm = list(np.concatenate(wm_resized).flat)
# # wm_copy = wm
# # wm = [[i] for i in wm]

# # if plot:
# #     fig1 = plt.figure(figsize=(6, 6))
# #     plt.scatter(lon, lat,
# #             c=wm)
# #     plt.title("Raw wind data")

# # if documentation:
# #     print("wind resize done")

# # ## Solar        
# # id = np.average(id,axis=0)

# # # Make it square 
# # id = id[:lenlat,:lenlon]
# # i = 0
# # k = 0
# # l = 0
# # id_resized = [[0 for _ in range(res_resized)] for _ in range(res_resized)]
# # while i < res and (k < res_resized):
# #     j = 0
# #     l = 0
# #     while (j < res) and (l < res_resized):
# #         values = id[i:i+resize,j:j+resize]
# #         value_list = list(np.concatenate(values).flat)
# #         id_resized[k][l] = sum(value_list)/len(value_list)
# #         j += resize
# #         l += 1
# #     k += 1
# #     i += resize

# # id = list(np.concatenate(id_resized).flat)
# # id_copy = id
# # id = [[i] for i in id]

# # if plot:
# #     fig4 = plt.figure(figsize=(6, 6))
# #     plt.scatter(lon, lat,
# #             c=id)
# #     plt.title("Raw sun data")

# # if documentation:
# #     print("Solar resize done")

# # return(wm, wm_copy, wm_time, id, id_copy, id_time, lon, lat, coordinates, res_resized)