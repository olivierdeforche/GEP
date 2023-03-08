import geopandas as gpd
import netCDF4 as nc
import xarray as xr

fn_era = 'C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc'
ds = xr.open_dataset(fn_era)
edgar = ds.to_dataframe()
print(edgar)
print("done")


# geometry = gpd.points_from_xy(ds["w"]["lon"][:],ds["w"]["lat"][:])
# gdf = gpd.GeoDataFrame(ds, geometry=geometry, crs=4326)
# print(gdf.head(4))    

