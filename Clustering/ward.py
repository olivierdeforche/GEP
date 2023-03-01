from sklearn.cluster import AgglomerativeClustering

#from ..BaseClass import BaseSpOptHeuristicSolver
import netCDF4 as nc
from spopt.region import WardSpatial
import matplotlib.pyplot as plt

import libpysal
import matplotlib
import numpy as np
import spopt
import warnings
import geopandas as gpd
import time

import pytest

# Skip warnings
warnings.filterwarnings("ignore")

# fn_era = 'C:/Users/defor/OneDrive/Bureaublad/unif/Master/Thesis/GEP/Data/data_clustering/europe-2013-era5.nc'
fn_era = "C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc"


ds = dict()
ds["w"] = nc.Dataset(fn_era)
RANDOM_SEED = 123456


### Select smaller range of both datapoints
lon = ds["w"]["lon"][:]
lat = ds["w"]["lat"][:]
wm = ds["w"]["wnd100m"][:,:,:]
id = ds["w"]["influx_direct"][:,:,:]


## Only select first res values of each for threshold=number of points you should take together
res = 50 #orig 100
#threshold = 100 #orig 333
#np.random.seed(RANDOM_SEED)

lenlon = len(lon)
lenlat = len(lat)
lon = lon[:-(lenlon-res)]
lat = lat[:-(lenlat-res)]

## Transform the lists
lon = np.tile(lon, res)
lat = np.repeat(lat, res)

## Preperation for GeoDataFrame
geo = gpd.GeoSeries.from_xy(lon, lat)
w = libpysal.weights.lat2W(res, res)
print(w)

### Wind
start_wind = time.time()

wm = np.average(wm,axis=0)
wm = wm[:-(lenlat-res),:-(lenlon-res)]
wm = list(np.concatenate(wm).flat)
wm_copy = wm
wm = [[i] for i in wm]

fig1 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm)
plt.title("Raw wind data")

## transform to GeoDataFrame
frame = gpd.GeoDataFrame(wm, geometry=geo)

#frame["count"] = 1
frame.rename(columns={0:'Data'}, inplace=True )
print(frame)

## Name data used by Ward method
attrs_name = ["Data"]
attrs_name = np.array(attrs_name)
print(attrs_name)

#spatial weights
w = libpysal.weights.lat2W(res, res)
clusters = 30



print("starting model")
model = WardSpatial(frame, w, attrs_name, clusters)
model.solve()
print("Model Solved, starting calculations of cluster values")

fig2 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=model.labels_)
plt.title("Wind clusters, random colors, ward")


nr_of_clusters = clusters
clusters = dict.fromkeys(range(1, nr_of_clusters))
clusters_values = dict.fromkeys(range(1, nr_of_clusters))

for i in range(len(clusters) + 1):
    clusters[i + 1] = list()
    clusters_values[i + 1] = list()

for i in range(len(model.labels_)):
    clusters[model.labels_[i]].insert(i, i)
    clusters_values[model.labels_[i]].insert(i, wm_copy[i])

for key in clusters:
    average = np.average(clusters_values[key])
    for i in range(len(clusters[key])):
        wm_copy[clusters[key][i]] = average

fig3 = plt.figure(figsize=(6, 6))
plt.scatter(lon, lat,
           c=wm_copy)
plt.title("Wind clusters, ranked with color, max-p")
plt.show()

end_wind = time.time()
print("Computation time (h):")
print((end_wind-start_wind)/3600)





# areas = np.arange(res * res)
# regions = [areas[model.labels_ == region] for region in range(clusters)]
#
# wm = np.array(wm)
# wm = list(np.concatenate(wm).flat)
#
# for i in range(clusters):
#     for j in range(len(regions[i])):
#         wm[regions[i][j]] = model.centroids_[i]
#
#
# fig2 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=model.labels_)
# plt.title("Wind clusters, random colors, kmeans")
# plt.show()
#
# nr_of_clusters = clusters
# clusters = dict.fromkeys(range(1,nr_of_clusters))
# clusters_values = dict.fromkeys(range(1,nr_of_clusters))
#
# for i in range(len(clusters)+1):
#     clusters[i+1] = list()
#     clusters_values[i+1] = list()
#
# for i in range(len(model.labels_)):
#     clusters[model.labels_[i]].insert(i,i)
#     clusters_values[model.labels_[i]].insert(i,wm_copy[i])
#
# for key in clusters:
#     average = np.average(clusters_values[key])
#     for i in range(len(clusters[key])):
#         wm_copy[clusters[key][i]] = average
#
#
# fig3 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=wm_copy)
# plt.title("Wind clusters, ranked with color, kmeans")
#
#
# end_wind = time.time()
# print("Computation time wind (h):")
# print((end_wind-start_wind)/3600)
#
# plt.show()





# nr_of_clusters = clusters
# clusters = dict.fromkeys(range(1,nr_of_clusters))
# clusters_values = dict.fromkeys(range(1,nr_of_clusters))
#
# for i in range(len(clusters)+1):
#     clusters[i+1] = list()
#     clusters_values[i+1] = list()
#
# for i in range(len(model.labels_)):
#     clusters[model.labels_[i]].insert(i,i)
#     clusters_values[model.labels_[i]].insert(i,wm_copy[i])
#
# for key in clusters:
#     average = np.average(clusters_values[key])
#     for i in range(len(clusters[key])):
#         wm_copy[clusters[key][i]] = average
#
#
# print("values relating to specific clusters calculated and ready")
#
# fig3 = plt.figure(figsize=(6, 6))
# plt.scatter(lon, lat,
#            c=wm_copy)
# plt.title("Wind clusters, ranked with color, max-p")
#
# end_wind = time.time()
# print("Computation time (h):")
# print((end_wind-start_wind)/3600)


class WardSpatial(BaseSpOptHeuristicSolver):
    """Agglomerative clustering using Ward
    linkage with a spatial connectivity constraint.

    Parameters
    ----------

    gdf : geopandas.GeoDataFrame
        Geodataframe containing original data.
    w : libpysal.weights.W
        Weights object created from given data.
    attrs_name : list
        Strings for attribute names (cols of ``geopandas.GeoDataFrame``).
    n_clusters : int (default 5)
        The number of clusters to form.
    clustering_kwds: dict
        Other parameters about clustering could be used in
        ``sklearn.cluster.AgglometariveClustering.``

    Returns
    -------

    labels_ : numpy.array
        Cluster labels for observations.


    Examples
    --------

    >>> import geopandas
    >>> import libpysal
    >>> import numpy
    >>> from spopt.region import WardSpatial

    Read the data.

    >>> libpysal.examples.load_example('AirBnB')
    >>> pth = libpysal.examples.get_path('airbnb_Chicago 2015.shp')
    >>> chicago = gpd.read_file(pth)

    Initialize the parameters.

    >>> w = libpysal.weights.Queen.from_dataframe(chicago)
    >>> attrs_name = ['num_spots']
    >>> n_clusters = 8

    Run the ``WardSpatial`` algorithm.

    >>> model = WardSpatial(chicago, w, attrs_name, n_clusters)
    >>> model.solve()

    Get the counts of region IDs for unit areas.

    >>> numpy.array(numpy.unique(model.labels_, return_counts=True)).T
    array([[ 0, 62],
           [ 1,  6],
           [ 2,  3],
           [ 3,  1],
           [ 4,  2],
           [ 5,  1],
           [ 6,  1],
           [ 7,  1]])

    """

    def __init__(self, gdf, w, attrs_name, n_clusters=5, clustering_kwds=dict()):
        self.gdf = gdf
        self.w = w
        self.attrs_name = attrs_name
        self.n_clusters = n_clusters
        self.clustering_kwds = clustering_kwds

    def solve(self):
        """Solve the Ward"""
        data = self.gdf
        X = data[self.attrs_name].values
        model = AgglomerativeClustering(
            n_clusters=self.n_clusters,
            connectivity=self.w.sparse,
            linkage="ward",
            **self.clustering_kwds
        )
        model.fit(X)
        self.labels_ = model.labels_
