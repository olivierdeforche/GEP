import pickle
import netCDF4 as nc
import numpy as np
import time
import pandas as pd
import geopandas as gpd

import pandas as pd

dict1 = {"number of storage arrays": 45, "number of ports":2390}

df = pd.DataFrame(data=dict1, index=[0])

print(df)

df = (df.T)
method = 'kmeans'
number_of_clusters = 10
data= 'weather'
print(df)
print(df.sort_index)
string = str('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Timeseries/')+str(method)+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_clustered_on_wind.xlsx')
print(string)
df.to_excel(string)

# fn_era = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
# dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"
# # fn_era = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"

# ds = dict()
# ds["w"] = nc.Dataset(fn_era)
# RANDOM_SEED = 123456

# data = dict()
# data = nc.Dataset(dataset)


# ## Select smaller range of both datapoints
# lon = ds["w"]["lon"][:]
# lat = ds["w"]["lat"][:]
# wm = ds["w"]["wnd100m"][:,:,:] #8760 lists (timesteps 365*24) with 142 lists (lon) with 191 items (lat)
# id = ds["w"]["influx_direct"][:,:,:]

# # print(wm[0,1,0])

# res = 142  
# resize = 1
# res_resized = int(res/resize)

# lenlon = len(lon)
# lenlat = len(lat)


# print(wm.shape)
# wmm = dict()
# wmmm = dict()
# for i in range(wm.shape[0]):
#      print(i)
#      # wmm[i+1] = np.concatenate(wm[i][:, :-(lenlon-res)]).flatten()
#      wmmm[i+1] = wm[i][:, :-(lenlon-res)].flatten()
# print("------------------")
# # print(len(wmm))
# # print(len(wmm[1]))
# print(len(wmmm))
# print(len(wmmm[1]))
# print("----------------")
# # print(wmm[1][0])
# # print(wmmm[1][0])
# print("-------------------")
# print(wmm[1][560])
# print(wmmm[1][560])

# wm_data = data["wind_af"][:,:,:]
# id_data = data["solar_af"][:,:,:]
# lon_data = data["x"][:]
# lat_data = data["y"][:]

# print(wm_data.shape)
# print(wm.shape[1])
# print(wm.shape[-3])
# print(wm.T.shape)
# wm = wm.reshape(-1,wm.shape[-3])
# print(wm.T.shape)
# wm = wm.T
# print(wm[0,1])
# print(wm)

# res = 142  
# resize = 1
# res_resized = int(res/resize)

# lenlon = len(lon)
# lenlat = len(lat)
# adjusted_size = lenlon-res
# lon = lon[:-(adjusted_size)]
# lon = lon[0::resize]
# lat = lat[0::resize]

# # Adjust length lon and lat by cutting of left and bottom
# if len(lon) > res_resized:
#     lon = lon[1:]
#     lat = lat[1:]

# ## Transform the lists
# lon = np.tile(lon, res_resized)
# lat = np.repeat(lat, res_resized)

# df = pd.DataFrame(
#     {'Latitude': lat,
#         'Longitude': lon})

# gdf = gpd.GeoDataFrame(
#     df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
# coordinates = list(gdf["geometry"])

# print(coordinates)

# print('lat', lat)




# ## Only select first res values of each with nr of clusters
# res = 142  
# resize = 1
# res_resized = int(res/resize)

# lenlon = len(lon)
# lenlat = len(lat)
# adjusted_size = lenlon-res
# lon = lon[:-(adjusted_size)]
# lon = lon[0::resize]
# lat = lat[0::resize]

# # Adjust length lon and lat by cutting of left and bottom
# if len(lon) > res_resized:
#     lon = lon[1:]
#     lat = lat[1:]

# ## Transform the lists
# lon = np.tile(lon, res_resized)
# lat = np.repeat(lat, res_resized)




# # wm_time_1 = dict.fromkeys(range(1, len(wm)//2+1))
# # wm_time_2 = dict.fromkeys(range(len(wm)//2+1, len(wm)))
# # id_time_1 = dict.fromkeys(range(1, len(id)//2+1))
# # id_time_2 = dict.fromkeys(range(len(wm)//2+1, len(wm)))

# wm_time_1 = dict()
# wm_time_2 = dict()
# id_time_1 = dict()
# id_time_2 = dict()
# for i in range(len(wm)//2):
#     print(i)
#     wm_time_1[i+1] = list(np.concatenate(wm[i][:, :-adjusted_size]).flat)
#     wm_time_2[i+1+len(wm)//2] = list(np.concatenate(wm[i+len(wm)//2][:, :-adjusted_size]).flat)
#     id_time_1[i+1] = list(np.concatenate(id[i][:, :-adjusted_size]).flat)
#     id_time_2[i+1+len(wm)//2] = list(np.concatenate(id[i+len(wm)//2][:, :-adjusted_size]).flat)


# # print(len(wm_time_1))
# # print(len(wm_time_2))
# # print(len(wm_time_1[0]))
# # print(len(wm_time_2[0]))
# # print(len(id_time_1))
# # print(len(id_time_2))
# # print(len(id_time_1[0]))
# # print(len(id_time_2[0]))
# # print(type(wm_time))



# # # create a binary pickle file 
# # f1 = open('C:/Users/defor/Desktop/Thesis/Data/wm_time_correct.pkl',"wb")
# # print ("done")
# # # write the python object (dict) to pickle file
# # pickle.dump(wm_time,f1)
# # print ("done")
# # # close file
# # f1.close()

# # print ("done")
# # # f2 = open('C:/Users/defor/Desktop/Thesis/Data/id_time_correct.pkl',"wb")
# # # # write the python object (dict) to pickle file
# # # pickle.dump(id_time,f2)

# # # # close file
# # # f2.close()


# # # create a dictionary using {}
# # person = {"name": "Jessa", "country": "USA", "telephone": 1178}
# # print('Person dictionary')
# # print(person)

# # # save dictionary to person_data.pkl file
# # with open('wm_time_correct.pkl', 'wb') as fp:
# #     pickle.dump(wm_time, fp)
# #     print('dictionary saved successfully to file')

# # # Read dictionary pkl file
# # with open('wm_time_correct.pkl', 'rb') as fp:
# #     person = pickle.load(fp)
# #     print('Person dictionary')
# #     print(person)

# # save dictionary to person_data.pkl file
# with open("C:/Users/defor/Desktop/Thesis/Data/wm_time_correct_1.pkl", 'wb') as fe:
#     pickle.dump(wm_time_1, fe)
#     print('dictionary saved successfully to file')

# start = time.time()
# # Read dictionary pkl file
# with open('C:/Users/defor/Desktop/Thesis/Data/wm_time_correct_1.pkl', 'rb') as fe:
#     wm_1 = pickle.load(fe)
#     print('opened succesfully')
#     print(len(wm_1))

# # # save dictionary to person_data.pkl file
# # with open("C:/Users/defor/Desktop/Thesis/Data/wm_time_correct_2.pkl", 'wb') as fe:
# #     pickle.dump(wm_time_2, fe)
# #     print('dictionary saved successfully to file')

# # Read dictionary pkl file
# with open('C:/Users/defor/Desktop/Thesis/Data/wm_time_correct_2.pkl', 'rb') as fe:
#     wm_2 = pickle.load(fe)
#     print('opened succesfully')
#     print(len(wm_2))

# # # save dictionary to person_data.pkl file
# # with open("C:/Users/defor/Desktop/Thesis/Data/id_time_correct_1.pkl", 'wb') as fe:
# #     pickle.dump(id_time_1, fe)
# #     print('dictionary saved successfully to file')

# # Read dictionary pkl file
# with open('C:/Users/defor/Desktop/Thesis/Data/id_time_correct_1.pkl', 'rb') as fe:
#     id_1 = pickle.load(fe)
#     print('id opened succesfully')
#     print(len(id_1))

# # # save dictionary to person_data.pkl file
# # with open("C:/Users/defor/Desktop/Thesis/Data/id_time_correct_2.pkl", 'wb') as fe:
# #     pickle.dump(id_time_2, fe)
# #     print('dictionary saved successfully to file')

# # Read dictionary pkl file
# with open('C:/Users/defor/Desktop/Thesis/Data/id_time_correct_2.pkl', 'rb') as fe:
#     id_2 = pickle.load(fe)
#     print('id opened succesfully')
#     print(len(id_2))

# stop = time.time()
# print("Data loading and resizing done with a computation time (h):", (stop-start)/3600)







