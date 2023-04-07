import pickle
import netCDF4 as nc
import numpy as np

fn_era = "C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc"
# fn_era = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"

ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456

### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:] #8760 lists (timesteps 365*24) with 142 lists (lon) with 191 items (lat)
id = ds["w"]["influx_direct"][:,:,:]


## Only select first res values of each for threshold=number of points you should take together
res = 10 # orig 100
n_clusters = 10 # orig 100

lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lat = lat[:-(lenlat-res)]

## Transform the lists
lon = np.tile(lon, res)
lat = np.repeat(lat, res)

wm_time = dict.fromkeys(range(1, len(wm)))
id_time = dict.fromkeys(range(1, len(id)))
for i in range(len(wm)):
    print(i)
    wm_time[i] = list(np.concatenate(wm[i][:, :-(lenlon-res)]).flat)
    id_time[i] = list(np.concatenate(id[i][:, :-(lenlon-res)]).flat)


with open(,'wb') as fp:
