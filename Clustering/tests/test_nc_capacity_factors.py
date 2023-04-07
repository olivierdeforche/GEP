import atlite
import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np

data = "no"
if data=="yes":
    dataset = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"
else:
    dataset = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
ds = dict()
ds["w"] = nc.Dataset(dataset)

if data=="yes":
    wm = ds["w"]["wind_af"][:,:,:]
    id = ds["w"]["solar_af"][:,:,:]
    lon = ds["w"]["x"][:]
    lat = ds["w"]["y"][:]
            
else:
    wm = ds["w"]["wnd100m"][:,:,:]
    id = ds["w"]["influx_direct"][:,:,:]
    lon = ds["w"]["lon"][:]
    lat = ds["w"]["lat"][:]

print("wind", wm, "solar", id, "lon",lon,"lat",lat)












# cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
# # print(cutout)

# era = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
# k = dict()
# k["w"] = nc.Dataset(era)

# capacity_factors_file =  "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"
# capacity_factors = dict()
# capacity_factors = nc.Dataset(capacity_factors_file)
# print(k["w"]["wnd100m"][:,:,:])
# print(capacity_factors["solar_af"][:,:,:])
# print(capacity_factors["wind_af"][:,:,:])
# print(k["w"]["x"][:])
# print(k["w"]["lon"][:])
# print(capacity_factors)

# print(ds["w"]["wnd100m"][:,:,:])
# wm = ds["w"]["wnd100m"][:,:,:]
# wm = np.average(wm,axis=0)
# print(wm)

# time_era = k["w"]["time"][:]
# lon_era = k["w"]["lon"][:]
# lat_era = k["w"]["lat"][:]
# print(k["w"]["wnd100m"].shape)
# lenlon = len(lon_era)
# lenlat = len(lat_era)
# wm = wm[:lenlat,:lenlon]
# print(wm)

# print(ds["w"]["time"][:])
# print(ds["w"]["lon"][:])
# print(ds["w"]["lat"][:])

# solar = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_solar.nc"
# wind = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_wind.nc"
# fn = "C:/Users/defor/Desktop/Thesis/Data/Capacity_factor_lonlat.nc"

# solar = Dataset(solar)
# solar = solar["specific generation"]
# wind = Dataset(wind)
# wind = wind["specific generation"]
# ds = Dataset(fn, mode='w', format='NETCDF4_CLASSIC')
# time = ds.createDimension('time', 8760)
# lat = ds.createDimension('y', 142)
# lon = ds.createDimension('x', 191)



# times = ds.createVariable('time', 'f4', ('time',))
# lats = ds.createVariable('y', 'f4', ('y',))
# lons = ds.createVariable('x', 'f4', ('x',))
# solar_af = ds.createVariable('solar_af', 'f4', ('time', 'y', 'x',))
# solar_af.units = 'AF'
# wind_af = ds.createVariable('wind_af', 'f4', ('time', 'y', 'x',))
# wind_af.units = 'AF'

# lats[:] = lat_era
# lons[:] = lon_era
# times[:] = time_era

# for t in time_era:
#     xy = 0
#     for la in range(142):
#         print("time", t, "latitude", la)
#         solar_af[t,la,:] = solar[t,xy:xy+191]
#         wind_af[t,la,:] = wind[t,xy:xy+191]
#         xy += 191
# print("yes")
# ds.close()


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
    
