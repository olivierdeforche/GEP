import geopandas as gpd
import netCDF4 as nc
import xarray as xr
from atlite.gis import ExclusionContainer
from atlite.gis import shape_availability
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs


# Read countires in
url = "https://tubcloud.tu-berlin.de/s/7bpHrAkjMT3ADSr/download/country_shapes.geojson"
countries = gpd.read_file(url).set_index('name')


# Exclusion from natura data base
fn_era = 'C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc'
excluder = ExclusionContainer(crs=3035)

#This is currently only for Portugal, need the natura for the whole of EU
excluder.add_geometry('Natura2000_end2021-PT.gpkg') 
shape = countries.to_crs(excluder.crs).loc[["PT"]].geometry
shape[0]

# Returns a 2D numpy.ndarray and a transformation similar to rasterio data
# Eligile raster cells have a True and excluded cells a False.
band, transform = shape_availability(shape, excluder)

fig, ax = plt.subplots(figsize=(4,8))
shape.plot(ax=ax, color='none')
show(band, transform=transform, cmap='Greens', ax=ax)

