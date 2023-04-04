import atlite
from atlite.gis import ExclusionContainer
from atlite.gis import shape_availability
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import rasterio
from rasterio.plot import show
import numpy as np
import pandas as pd
import xarray as xr

## Extract data
cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
countries = gpd.read_file("C:/Users/defor/Desktop/Thesis/country_shapes.geojson")
countries.plot(edgecolor='k', facecolor='lightgrey')
crs = ccrs.EqualEarth()
fig = plt.figure(figsize=(10,5))
ax = plt.axes(projection=crs)

# Chang index of GeoDataFrame from number to 'name' 
countries = countries.set_index('name')

countries.to_crs(crs.proj4_init).plot(
    ax=ax,
    edgecolor='k',
    facecolor='lightgrey'
)

## Exclude in-eligable land
excluder = ExclusionContainer(crs=3035)
print("yes containter")
excluder.add_geometry("C:/Users/defor/Desktop/Thesis/Natura2000_end2021.gpkg")
print("yes excluder")

## Convert geometry of countries to excluder.crs 
shape = countries.to_crs(excluder.crs).loc[['PT', 'ES']].geometry
print("yes Countries")

band, transform = shape_availability(shape, excluder)

print("yes band and transform")

fig, ax = plt.subplots(figsize=(4,8))
shape.plot(ax=ax, color='none')
show(band, transform=transform, cmap='Greens', ax=ax)

print("exclude done")

# Start working with weather data
A = cutout.availabilitymatrix(shape, excluder)
fig, ax = plt.subplots()
A.sel(name='PT').plot(cmap='Greens')
shape.to_crs(3035).plot(ax=ax, edgecolor='k', color='none')
cutout.grid.plot(ax=ax, color='none', edgecolor='grey', ls=':')


## Preperation for conversion to capacity factors
cap_per_sqkm = 2
area = cutout.grid.set_index(['y', 'x']).to_crs(3035).area / 1e6
area = xr.DataArray(area, dims=('spatial'))
capacity_matrix = A.stack(spatial=['y', 'x']) * area * cap_per_sqkm

print("preparation for conversion done")

## Conversion to capacity factors
print(capacity_matrix)
print(shape.index)
print(shape)
cutout.prepare()
wind = cutout.wind(matrix=capacity_matrix, turbine="Vestas_V90_3MW", index=shape.index,  per_unit=True)
pv = cutout.pv(matrix=capacity_matrix, panel="CdTe", 
               orientation="latitude_optimal", index=shape.index,  per_unit=True
)

fig1 = plt.figure(figsize=(6, 6))
plt.plot(wind)
fig2 = plt.figure(figsize=(6, 6))
plt.plot(pv)

print(wind)
print(pv)
print("conversion done")

## Conversion to availability factors
fig2 = plt.figure(figsize=(6, 6))
plt.plot(wind)

fig3 = plt.figure(figsize=(6, 6))
plt.plot(pv)

plt.show()