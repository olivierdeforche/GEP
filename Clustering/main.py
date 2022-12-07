import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


fn_be_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/be-03-2013-era5.nc'
fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
fn_sara = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-sarah.nc'

ds = dict()
ds["be"] = nc.Dataset(fn_be_era)
ds["w"] = nc.Dataset(fn_era)
ds["s"] = nc.Dataset(fn_sara)
print(ds["be"].variables)

# print(ds["w"].variables)
# print(ds["s"].variables)
# print(ds["s"]["influx_direct"][:,72,17])
# print(id)
# print(ds["s"]["influx_direct"][7,-65,:])

# print(ds["w"]["lon"][:])
# print(len(ds["w"]["lon"][:]))
# print("------------------------")
# print(ds["w"]["lat"][:])
# print(len(ds["w"]["lat"][:]))

# print(ds["s"]["lon"])
# print(ds["s"]["lat"])
# lon = ds["be"]["lon"][:]
# lat = ds["be"]["lat"][:]
# id = ds["be"]["influx_direct"][7,:,:]
#
# print(id)
# print(lat)
# print(len(lat))
# print(len(lon))
#
# for i in range(0,23):
#     for j in range(0,13):
#         plt.scatter(lon[i],lat[j],id[j,i])
#
# # plt.xlabel('Longitude')
# # plt.ylabel('Latitude')
# # plt.zlabel('influx direct')
#
# plt.show()

lon = ds["s"]["lon"][:]
lat = ds["s"]["lat"][:]
id = ds["s"]["influx_direct"][7,:,:]

print(id)
print(lat)
print(len(lat))
print(len(lon))

for i in range(0,285):
    for j in range(0,210):
        plt.scatter(lon[i],lat[j],id[j,i])

# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.zlabel('influx direct')

plt.show()