import atlite

cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
# print(cutout.pv)
# print(cutout.available_features)
# cap_factors_wind = cutout.wind(turbine="Vestas_V112_3MW", capacity_factor=True)
# print(type(cap_factors_wind))
# print(cap_factors_wind)

# # Panels: CdTe, CSI, KANENA
# cap_factors_sun = cutout.pv(panel='CdTe', orientation='latitude_optimal', capacity_factor=True) 
# print(cap_factors_sun)