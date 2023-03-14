import atlite
import geopandas as gpd
import numpy as np
# from atlite.gis import ExclusionContainer


# # Read countires in
# url = "https://tubcloud.tu-berlin.de/s/7bpHrAkjMT3ADSr/download/country_shapes.geojson"
# countries = gpd.read_file(url).set_index('name')
# print("done")
# excluder = ExclusionContainer(crs=3035)

# shape = countries.to_crs(excluder.crs).loc[["PT"]].geometry
# shape[0]

# cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
cutout = atlite.Cutout("C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc")

# print(type(cutout))
# print(cutout.data)

cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
print(type(cutout))
print(cutout.data)

# A = cutout.availabilitymatrix(shape, excluder)

# cutout.prepare()
# cap_factors_wind = cutout.wind(turbine="Vestas_V112_3MW", capacity_factor=True)

# ax = shape.to_crs(4326).plot()
# cutout.grid.plot(ax=ax, edgecolor='grey', color='None')

# print(cutout.available_features)

# Turbines: Vestas-112-3MW 
cap_factors_wind = cutout.wind(turbine="Vestas_V112_3MW", capacity_factor=True)
print(type(cap_factors_wind))
print(cap_factors_wind)
np.savetxt('cap_factors_wind.csv', cap_factors_wind, delimiter=',')

# Panels: CdTe, CSI, KANENA
cap_factors_sun = cutout.pv(panel='CdTe', orientation='latitude_optimal', capacity_factor=True)
print(cap_factors_sun)
np.savetxt('cap_factors_sun.csv', cap_factors_sun, delimiter=',')
# cap_factors_sun.to_csv("AF_sun.csv")