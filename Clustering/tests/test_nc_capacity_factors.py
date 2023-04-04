import atlite
import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np

# cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
# # print(cutout)

era = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
k = dict()
k["w"] = nc.Dataset(era)
# print(ds["w"]["wnd100m"][:,:,:])
# wm = ds["w"]["wnd100m"][:,:,:]
# wm = np.average(wm,axis=0)
# print(wm)

time_era = k["w"]["time"][:]
lon_era = k["w"]["lon"][:]
lat_era = k["w"]["lat"][:]
print(k["w"]["wnd100m"].shape)
lenlon = len(lon_era)
lenlat = len(lat_era)
# wm = wm[:lenlat,:lenlon]
# print(wm)

# print(ds["w"]["time"][:])
# print(ds["w"]["lon"][:])
# print(ds["w"]["lat"][:])

solar = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_solar.nc"
wind = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_wind.nc"
fn = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"

solar = Dataset(solar)
solar = solar["specific generation"]
wind = Dataset(wind)
wind = wind["specific generation"]
ds = Dataset(fn, mode='w', format='NETCDF4_CLASSIC')
time = ds.createDimension('time', 8760)
lat = ds.createDimension('lat', 142)
lon = ds.createDimension('lon', 191)



times = ds.createVariable('time', 'f4', ('time',))
lats = ds.createVariable('lat', 'f4', ('lat',))
lons = ds.createVariable('lon', 'f4', ('lon',))
solar_af = ds.createVariable('solar_af', 'f4', ('time', 'lat', 'lon',))
solar_af.units = 'AF'
wind_af = ds.createVariable('wind_af', 'f4', ('time', 'lat', 'lon',))
wind_af.units = 'AF'

lats[:] = lat_era
lons[:] = lon_era
times[:] = time_era

for t in time_era:
    xy = 0
    for la in range(142):
        print("time", t, "latitude", la)
        solar_af[t,la,:] = solar[t,xy:xy+191]
        solar_af[t,la,:] = wind[t,xy:xy+191]
        xy += 191
print("yes")
ds.close()


# for t in time_era:
#     xy = 0
#     print("time", t)
#     for la in range(142):
#         for lo in range(191):
#             solar_af[t, la, lo] = solar[t, xy]
#             wind_af[t, la, lo] = wind[t, xy]
#             xy += 1
# print("yes")
# ds.close()

# print(solar["specific generation"][:,:])
# solar = solar["specific generation"][:,:]
# solar = np.average(solar,axis=0)
# print(solar)

# latitudes = ds["w"].createVariable("lat","f4",("lat",))
# longitudes = ds["w"].createVariable("lon","f4",("lon",))
# latitudes.units = "K"
# longitudes.units = ""

# print(ds["w"]["specific generation"][:,:])
# print(ds["w"]["time"][:])
# print(ds["w"]["dim_0"][:])

# print(cutout)
# print(cutout.coords['x'].values)
# print(cutout.coords['y'].values)
    
