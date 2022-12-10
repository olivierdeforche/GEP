from spopt.region import MaxPHeuristic as MaxP
import matplotlib.pyplot as plt

import geopandas
import libpysal
import matplotlib
import numpy
import spopt
import warnings

# Skip warnings
plt.rcParams["figure.figsize"] = [12, 8]
warnings.filterwarnings("ignore")

RANDOM_SEED = 123456


