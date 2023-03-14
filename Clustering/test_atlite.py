import atlite
# from atlite.gis import ExclusionContainer
# from atlite.gis import shape_availability
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import cartopy
# import cartopy.crs as ccrs

# ## Extract data
# cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")

# countries = gpd.read_file("C:/Users/defor/Desktop/Thesis/country_shapes.geojson")
# countries.plot(edgecolor='k', facecolor='lightgrey')
# plt.show()

# # crs = ccrs.EqualEarth()

# # fig = plt.figure(figsize=(10,5))

# # ax = plt.axes(projection=crs)

# # countries.to_crs(crs.proj4_init).plot(
# #     ax=ax,
# #     edgecolor='k',
# #     facecolor='lightgrey'
# # )
# # plt.show()

# ## Exclude in-eligable land
# excluder = ExclusionContainer(crs=3035)
# excluder.add_geometry("C:/Users/defor/Desktop/Thesis/Natura2000_end2021.gpkg")

# # ## Convert geometry of countries to excluder.crs
# # shape = countries.to_crs(excluder.crs).loc[["PT"]].geometry
# # print(shape[0])
