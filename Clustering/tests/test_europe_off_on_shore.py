import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely.geometry import Point, Polygon
import pandas as pd



# EZZ = gpd.read_file("C:/Users/defor/Desktop/Thesis/Data/EEZ-Europe.shp")
# print(EZZ)
# EZZ.to_file('C:/Users/defor/Desktop/Thesis/Data/EEZ_Land_v3_202030.geojson', driver='GeoJSON')
# EZZ = gpd.read_file("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/EEZ_Europe_land.geojson")
# EZZ.plot(edgecolor='k', facecolor='lightgrey')
# print(EZZ)
# plt.show()

# europe_land = gpd.read_file("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/europe.geojson")
# europe = europe_land.geometry[0]
# coordinates = [Point(40.5, 55.8), Point(36.9,45.5), Point(27.6,42.6),Point(-14,60)]

# df = pd.DataFrame(
#     {     'Latitude': [55.8, 45.5, 42.6, 60],
#         'Longitude': [40.5, 36.9, 27.6, -14]})

# gdf = gpd.GeoDataFrame(
#     df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
# ax = europe_land.plot(edgecolor='k', facecolor='lightgrey')
# gdf.plot(ax=ax, color='red')

# for point in coordinates:
#     if not europe.contains(point):
#         print(point,"is inside the sea")

# plt.show()


# countries = gpd.read_file("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/europe.geojson")
# countries.plot(edgecolor='k', facecolor='lightgrey')
# plt.show()


# polys = []
# for polygon in countries.geometry:
#     polys.append(polygon)
# # print(polys)


# mergedPolys = unary_union(polys)
# gpd.GeoSeries(polys).boundary.plot()
# gpd.GeoSeries([mergedPolys]).boundary.plot()
# crs = ccrs.EqualEarth()
# fig = plt.figure(figsize=(10,5))
# ax = plt.axes(projection=crs)
# print(mergedPolys)

# gdf = gpd.GeoDataFrame(index=[0], crs=3035, geometry=[mergedPolys])
# print(gdf)

# europe = gpd.GeoSeries([mergedPolys]).__geo_interface__
# gdf.to_file("C:/Users/defor/Desktop/Thesis/GEP/Clustering/tests/europe.geojson", driver='GeoJSON')
# print(gdf)
# plt.show()

