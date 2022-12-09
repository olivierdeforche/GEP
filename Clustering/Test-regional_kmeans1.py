from spopt.region import RegionKMeansHeuristic

import geopandas
import libpysal
import numpy
import  matplotlib.pyplot as plt

dim = 10
w = libpysal.weights.lat2W(dim, dim)
# print(w.n)

RANDOM_SEED = 12345
numpy.random.seed(RANDOM_SEED)
data = numpy.random.normal(size=(w.n, 1))
# print(data)

print(w.neighbors)

libpysal.weights.build_lattice_shapefile(dim, dim, "lattice.shp")

gdf = geopandas.read_file("lattice.shp")
gdf.plot(column="ID")
plt.show()


print(data)
print(type(data))
print(type(data[0]))
print([data[0]])


model = RegionKMeansHeuristic(data, 20, w)
model.solve()


model.labels_
gdf["region"] = model.labels_
gdf.plot(column="region")
plt.show()
