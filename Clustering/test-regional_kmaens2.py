from spopt.region.spenclib.utils import lattice
from spopt.region import RegionKMeansHeuristic
import numpy
import libpysal
import matplotlib.pyplot as plt

hori, vert = 50, 50
n_polys = hori * vert
gdf = lattice(hori, vert)
print(gdf.head())

RANDOM_SEED = 12345
numpy.random.seed(RANDOM_SEED)
gdf["data_values_1"] = numpy.random.random(n_polys)
gdf["data_values_2"] = numpy.random.random(n_polys)
vals = ["data_values_1", "data_values_2"]
print(gdf.head())

gdf = gdf[:1300].append(gdf[1500:])
w = libpysal.weights.Rook.from_dataframe(gdf)

gdf.plot()
plt.show()


numpy.random.seed(RANDOM_SEED)
model = RegionKMeansHeuristic(gdf[vals].values, 8, w)
model.solve()

gdf["reg_k_mean"] = model.labels_
gdf.plot(
    column="reg_k_mean",
    categorical=True,
    cmap="tab20",
    figsize=(12,12),
    edgecolor="w"
)
plt.show()