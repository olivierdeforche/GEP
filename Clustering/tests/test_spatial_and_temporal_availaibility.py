import atlite
import geopandas as gpd
import numpy as np
from atlite.gis import ExclusionContainer
import matplotlib.pyplot as plt

cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
# cutout = atlite.Cutout("C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc")

# print(type(cutout))
# print(cutout.data)

# cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
print(type(cutout))
print(cutout.data)

# A = cutout.availabilitymatrix(shape, excluder)

cutout.prepare()
cap_factors_wind = cutout.wind(turbine="Vestas_V112_3MW", capacity_factor=True)

# ax = shape.to_crs(4326).plot()
# cutout.grid.plot(ax=ax, edgecolor='grey', color='None')

# print(cutout.available_features)

# Turbines: Vestas-112-3MW 
# cap_factors_wind = cutout.wind(turbine="Vestas_V112_3MW", per_unit=True)
# cap_factors_wind = cutout.wind(turbine="Vestas_V112_3MW", capacity_factor=True)
print(type(cap_factors_wind))
# max
# cap_factors_wind = cap_factors_wind / max(cap_factors_wind)
print(cap_factors_wind)
# np.savetxt('cap_factors_wind.csv', cap_factors_wind, delimiter=',')

# Panels: CdTe, CSI, KANENA
# cap_factors_sun = cutout.pv(panel='CdTe', orientation='latitude_optimal', capacity_factor=True)
# print(cap_factors_sun)
# np.savetxt('cap_factors_sun.csv', cap_factors_sun, delimiter=',')
# cap_factors_sun.to_csv("AF_sun.csv")

# cap_factors_wind.to_pandas().div(1e3).plot(ylabel="Solar Power [GW]", ls="--", figsize=(10, 4))

fig1 = plt.figure(figsize=(6, 6))
plt.plot(cap_factors_wind)
# fig2 = plt.figure(figsize=(6, 6))
# plt.plot(cap_factors_sun)
plt.show()