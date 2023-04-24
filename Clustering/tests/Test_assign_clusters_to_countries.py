import geopandas as gpd
import atlite
import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import numpy as np


EEZ = gpd.read_file('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/EEZ_Europe_land.geojson')
EEZ.plot(edgecolor='k', facecolor='lightgrey')
print(EEZ)
plt.show()
# print(EZZ["geometry"][0])
# print(EEZ["MRGID_EEZ"][0])
for polygon in EEZ["UN_TER1"]:
    print(polygon)

# dict_wind = dict()

# for country_name in EEZ["UNION"]:
#     dict_wind[country_name] = None


# for cluster in regions_wind:
#     size_cluster = len(cluster)
#     for number in cluster:
#         i = 0
#         for polygon in EEZ["geometry"]:
#             if polygon.contains(coordinates[number]):
#                 dict_wind[EEZ["UNION"][i]] += 1/size_cluster
#             else:
#                 i += 1


# coordinates = [[40.5, 55.8], [36.9,45.5], [27.6,42.6],[-14,60],[21,52]]
# hull = ConvexHull(coordinates)
# print(hull.vertices)

# index = len(hull.vertices)-1
# list_of_points = list()
# for point in hull.vertices:
#     list_of_points.append(Point(coordinates[point]))
# print(list_of_points)
# poly = Polygon(list_of_points)
# print(poly)
# df = gpd.GeoSeries(
#     poly)

# gdf = gpd.GeoSeries(
#     list_of_points)
# ax = gdf.plot(color='red')
# df.plot(ax=ax, color='green', alpha=0.5)
# plt.show()

# plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
# # plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
# print(hull.vertices)
# plt.show()


# df = pd.DataFrame(
#     {     'Latitude': [55.8, 45.5, 42.6, 60, 53.4],
#         'Longitude': [40.5, 36.9, 27.6, -14, 16.4]})

# gdf = gpd.GeoDataFrame(
#     df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# print(gdf)

# gdf_hull = gdf.unary_union.convex_hull
# convex_hull = gpd.GeoDataFrame({'geometry': gdf_hull, 'convex_hull':[1]})

# ax = gdf.plot(color='red')
# convex_hull.plot(ax=ax, color='green', alpha=0.5)

# print(gdf_hull)


