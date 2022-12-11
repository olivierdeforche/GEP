from spopt.region import MaxPHeuristic as MaxP
import matplotlib.pyplot as plt

import libpysal
import matplotlib
import numpy
import spopt
import warnings
import geopandas as gpd

# Skip warnings
warnings.filterwarnings("ignore")

RANDOM_SEED = 123456

pth = libpysal.examples.get_path("mexicojoin.shp")
mexico = gpd.read_file(pth)
mexico["count"] = 1
print(mexico)
print(len(mexico))
print(mexico.geometry)
print(mexico["PCGDP1950"])

w = libpysal.weights.Queen.from_dataframe(mexico)

print(w.weights)

attrs_name = [f"PCGDP{year}" for year in range(1950, 2010, 10)]

print(attrs_name)

threshold_name = "count"
# How many points should it take together?
threshold = 4

model = MaxP(mexico, w, attrs_name, threshold_name, threshold)
model.solve()

print(model.p)
print(model.labels_)

# x = [0,1,2,3,4,5]
# y = [0,1,2,3,4,5]
#
#
#
# test = gpd.GeoSeries.from_xy(x, y)
# print(type(test))
# print(test)
# frame = gpd.GeoDataFrame(geometry=test)
#
# print(type(frame))
# print(frame)



# def subplotter(gdf, incrs, W, threshold=5, top_n=2, seed=RANDOM_SEED):
#     """Helper plotting function, also solves MaxP instances if desired."""
#     rows, cols = incrs.shape
#     f, axs = plt.subplots(rows, cols, figsize=(9, 14))
#     for i in range(rows):
#         for j in range(cols):
#             year, _ax = incrs[i, j], axs[i, j]
#             if not year:
#                 # plot country geographies
#                 _attr = "Mexico"
#                 gdf.plot(ax=_ax, ec="grey", fc="white")
#             else:
#                 _attr = "PCGDP%s" % year
#                 if not W:
#                     # plot country geographies by attributes
#                     plt_kws = dict(scheme="Quantiles", cmap="GnBu", ec="grey")
#                     plt_kws.update(dict(legend_kwds={"fmt": "{:.0f}"}))
#                     gdf.plot(column=_attr, ax=_ax, legend=True, **plt_kws)
#                 else:
#                     # solve a MaxP instance and plot regions
#                     numpy.random.seed(seed)
#                     maxp_args = gdf, W, _attr, "count", threshold
#                     model = MaxP(*maxp_args, top_n=top_n)
#                     model.solve()
#                     label = year+"labels_"
#                     gdf[label] = model.labels_
#                     gdf.plot(column=label, ax=_ax, cmap="tab20")
#             _ax.set_title(_attr)
#             _ax.set_axis_off()
#             _ax.set_aspect("equal")
#     plt.subplots_adjust(wspace=-.7, hspace=-0.65)
#     plt.tight_layout()
