import geopandas
import libpysal
import numpy
import pandas
import spopt
from spopt.region import RegionKMeansHeuristic
import warnings
import matplotlib.pyplot as plt
import geopandas as gpd


dim1 = 4
dim2 = 4
w = libpysal.weights.lat2W(dim1, dim2)
w.n
noclusters = 5
RANDOM_SEED = 12345
numpy.random.seed(RANDOM_SEED)
data = numpy.random.normal(size=(w.n, 3))
data.shape

# print(w.neighbors)

libpysal.weights.build_lattice_shapefile(dim1, dim2, "lattice.shp")
gdf = geopandas.read_file("lattice.shp")
gdf.plot(column="ID")

model = RegionKMeansHeuristic(data, noclusters, w)
model.solve()

print(model.labels_)

areas = numpy.arange(dim1 * dim2)
regions = [areas[model.labels_ == region] for region in range(5)]

# gdf["region"] = model.labels_
# gdf.plot(column="region")
labels = model.labels_
print(type(labels))
# print(regions)
# print(model.labels_)
# print(type(regions))
# print(model.centroids_)

# europe_land = gpd.read_file("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/europe.geojson")
# print(europe_land.geometry[0])
# print(type(europe_land))

current_amount_of_clusters = noclusters
off_shore = list()
for i in range(len(regions)):
    off_shore.append(list())
    for number in regions[i]:
        if number == 0 or number ==12 or number ==10:
            regions[i] = regions[i][regions[i] != number]
            off_shore[-1].append(number)
            labels[number] = current_amount_of_clusters

    if len(off_shore[-1])==0:
        off_shore = off_shore[:-1]
    else:
        current_amount_of_clusters += 1
print(labels)
# print(regions)
# print(off_shore)
# print(model.labels_)
# print(labels)
# plt.show()

# EEZ = geopandas.read_file('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/EEZ_Europe_land.geojson')
    

# dict_wind = dict()

# for country_name in EEZ["UNION"]:
#     dict_wind[country_name] = 0

# # print(dict_wind)

# i = 0
# for countryname in EEZ["UNION"]:
#     if countryname=="Estonia" or countryname=="Portugal":
#         dict_wind[EEZ["UNION"][i]] += 1/(i+1)
#     i += 1

# print(dict_wind)

# for cluster in regions_wind:
#     size_cluster = len(cluster)
#     for number in cluster:
#         i = 0
#         for polygon in EEZ["geometry"]:
#             if polygon.contains(coordinates[number]):
#                 dict_wind[EEZ["UNION"][i]] += 1/size_cluster
#             else:
#                 i += 1