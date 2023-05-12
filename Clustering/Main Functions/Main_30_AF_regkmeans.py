from Read_data import Read_data
from Kmeans import Kmeans
from Kmedoids import Kmedoids
from Maxp import Maxp
from RegionalKmeans import RegionalKmeans
from Ward import Ward
# from Political_regions import PoliticalRegions
from Split_offshore_onshore import Split_offshore_onshore
from Convert_to_timeseries import Convert_to_timeseries
from Assign_clusters_to_countries import Asign_clusters_to_countries
import matplotlib.pyplot as plt
import time
import warnings


## Main Function
# This function converts the weather data from Era to clusters with their
# respective capacity factors in time series:
# Inputs:
# - method: kmeans, maxp, kmedoids, regional_kmeans, ward, political_regions
# - data: weather, af (default: weather)
# - size: 1,2,3,4 (default: 1)
# - number_of_clusters: (default: None)
# - threshold=None
# - Documentation: True, False (default=True)
# - plot: True, False (default: False)
# - User: Olivier, Louis  (default: Olivier)
#
# Outputs:
# - clusters with their time series
# - file with allocation of clusters to countries


def Clustering(method="kmeans", data="af", resize=1, number_of_clusters=None, threshold=None, documentation=True,
               plot=False, user="Olivier"):
    warnings.filterwarnings("ignore")
    # Check if right inputs:
    if not method == "kmeans" and not method == "maxp" and not method == "kmedoids" and not method == "regional_kmeans" and not method == "ward" and not method == "political_regions":
        print(
            "!!!WARNING!!! Wrong input in method field, only possibility are: 'kmeans', 'maxp', 'kmedoids', 'regional_kmeans', 'ward' and 'political_regions'. You put ",
            method)
        return

    if not data == "af" and not data == "weather":
        print("!!!WARNING!!! Wrong input in method field, only possibility are: 'af', 'weather'. You put:", data)
        return

    if not user == "Olivier" and not user == "Louis":
        print("!!!WARNING!!! User not know to the code, please contact either Olivier or Louis to fix this. You put:",
              user)
        return

    # Resize and load in the correct data
    if documentation:
        print("Start Clustering", method, number_of_clusters, data)
        print("----------------------------------------------")
        print("start resizing and loading data")
        start_resizing = time.time()

    wind, wind_copy, wind_time, solar, solar_copy, solar_time, lon, lat, coordinates, res_resized = Read_data(data,
                                                                                                              resize,
                                                                                                              plot,
                                                                                                              user,
                                                                                                              documentation)
    number_of_clusters_solar = number_of_clusters
    number_of_clusters_wind = number_of_clusters

    # Compute the clusters
    if documentation:
        stop_resizing = time.time()
        print("Data loading and resizing done")
        print("start computing clusters")
        print("------------------------------------")
        start_clustering = time.time()

    if method == "kmeans":
        labels_wind, regions_wind, labels_solar, regions_solar = Kmeans(wind, wind_copy, solar, solar_copy, lon, lat,
                                                                        number_of_clusters, res_resized, plot, user,
                                                                        data, resize)
    elif method == "maxp":
        labels_wind, regions_wind, number_of_clusters_wind, labels_solar, regions_solar, number_of_clusters_solar = Maxp(
            wind, wind_copy, solar, solar_copy, lon, lat, threshold, res_resized, plot, user, data, resize)
    elif method == "kmedoids":
        labels_wind, regions_wind, labels_solar, regions_solar = Kmedoids(wind, wind_copy, solar, solar_copy, lon, lat,
                                                                          number_of_clusters, res_resized, plot, user,
                                                                          data, resize)
    elif method == "regional_kmeans":
        labels_wind, regions_wind, labels_solar, regions_solar = RegionalKmeans(wind, solar, lon, lat,
                                                                                number_of_clusters, res_resized, plot,
                                                                                user, data, resize)
    elif method == "ward":
        labels_wind, regions_wind, labels_solar, regions_solar = Ward(wind, wind_copy, solar, solar_copy, lon, lat,
                                                                      number_of_clusters, res_resized, plot, user, data,
                                                                      resize)
    elif method == "political_regions":
        labels_wind, regions_wind, number_of_clusters_wind, labels_solar, regions_solar, number_of_clusters_solar, number_of_clusters = PoliticalRegions(
            lon, lat, coordinates, resize, user)

    # Split in off-shore and on-shore
    if documentation:
        stop_clustering = time.time()
        print("Clustering done")
        print("------------------------------------")
        print("start splitting off-shore and on-shore")
        start_splitting_ofonshore = time.time()

    regions_wind, regions_off_shore_wind, labels_wind, current_amount_of_clusters_wind, to_remove_wind, regions_solar, regions_off_shore_solar, labels_solar, current_amount_of_clusters_solar, to_remove_solar = Split_offshore_onshore(
        method, regions_wind, labels_wind, number_of_clusters_wind, regions_solar, labels_solar,
        number_of_clusters_solar, coordinates, lon, lat, plot, user, number_of_clusters, threshold, data, resize)

    # Compute time series for clusters and save them in a csv
    if documentation:
        stop_splitting_ofonshore = time.time()
        print("Splitting of off-shore and on-shore done")

    if plot:
        plt.show()

    if documentation:
        print("------------------------------------")
        print("Start converting to time series per cluster")
        start_time_series = time.time()

    Convert_to_timeseries(wind_copy, wind_time, labels_wind, number_of_clusters_wind, current_amount_of_clusters_wind,
                          to_remove_wind, solar_copy, solar_time, labels_solar, number_of_clusters_solar,
                          current_amount_of_clusters_solar, to_remove_solar, method, data, resize, documentation, plot,
                          user)

    # Assign clusters to countries and save it in a csv
    if documentation:
        stop_time_series = time.time()
        print("Conversion to time series of capacity factor")
        print("------------------------------------")
        print("Start asigning clusters to countries")
        start_asigning_cluster = time.time()

    Asign_clusters_to_countries(regions_wind, regions_off_shore_wind, number_of_clusters_wind, regions_solar,
                                regions_off_shore_solar, number_of_clusters_solar, coordinates, method, data, resize,
                                documentation, plot, user)

    if documentation:
        stop_asigning_cluster = time.time()
        print("------------------------------------")
        print("Assignment of clusters done:", method, number_of_clusters, data)
        print("------------------------------------")
        print("Total time (hours:minutes:seconds):", (stop_asigning_cluster - start_resizing) // 3600, ":",
              (stop_asigning_cluster - start_resizing) % 3600 // 60, ":",
              (stop_asigning_cluster - start_resizing) % 60 // 1)
        print('')
        print("Time contribution of each segment:")
        print("----------------------------------")
        print("   Resizing - ", (stop_resizing - start_resizing) / (stop_asigning_cluster - start_resizing) // 0.01,
              "% - ", (stop_resizing - start_resizing) // 3600, ":", (stop_resizing - start_resizing) % 3600 // 60, ":",
              (stop_resizing - start_resizing) % 60 // 1)
        print("   Clustering - ",
              (stop_clustering - start_clustering) / (stop_asigning_cluster - start_resizing) // 0.01, "% - ",
              (stop_clustering - start_clustering) // 3600, ":", (stop_clustering - start_clustering) % 3600 // 60, ":",
              (stop_clustering - start_clustering) % 60 // 1)
        print("   On/offshore - ",
              (stop_splitting_ofonshore - start_splitting_ofonshore) / (stop_asigning_cluster - start_resizing) // 0.01,
              "% - ", (stop_splitting_ofonshore - start_splitting_ofonshore) // 3600, ":",
              (stop_splitting_ofonshore - start_splitting_ofonshore) % 3600 // 60, ":",
              (stop_splitting_ofonshore - start_splitting_ofonshore) % 60 // 1)
        print("   Time series conversion - ",
              (stop_time_series - start_time_series) / (stop_asigning_cluster - start_resizing) // 0.01, "% - ",
              (stop_time_series - start_time_series) // 3600, ":", (stop_time_series - start_time_series) % 3600 // 60,
              ":", (stop_time_series - start_time_series) % 60 // 1)
        print("   Clusters to Countries - ",
              (stop_asigning_cluster - start_asigning_cluster) / (stop_asigning_cluster - start_resizing) // 0.01,
              "% - ", (stop_asigning_cluster - start_asigning_cluster) // 3600, ":",
              (stop_asigning_cluster - start_asigning_cluster) % 3600 // 60, ":",
              (stop_asigning_cluster - start_asigning_cluster) % 60 // 1)
        print("")
    if plot:
        plt.show()

    return ()

### Regional Kmeans

## 1/9 resolution
Clustering(method="regional_kmeans", data="af", resize=3, number_of_clusters=30, plot=False)

## 1/4 resolution
Clustering(method="regional_kmeans", data="af", resize=2, number_of_clusters=30, plot=False)

## full resolution
Clustering(method="regional_kmeans", data="af", resize=1, number_of_clusters=30, plot=False)


