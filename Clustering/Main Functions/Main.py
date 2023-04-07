from Read_data import Read_data
from Kmeans import Kmeans
from Kmedoids import Kmedoids
from Maxp import Maxp
from RegionalKmeans import RegionalKmeans
from Ward import Ward
from Split_offshore_onshore import Split_offshore_onshore
from Convert_to_timeseries import Convert_to_timeseries
from Assign_clusters_to_countries import Asign_clusters_to_countries
import matplotlib.pyplot as plt
import time

## Main Function
# This function converts the weather data from Era to clusters with their 
# respective capacity factors in time series:
# Inputs: 
# - method: kmeans, maxp, kmedoids, regional_kmeans, ward
# - data: weather, af (default: weather)
# - size: number (default: 1)
# - number_of_clusters: (default: None)
# - threshold=None
# - Documentation: True, False (default=True)
# - plot: True, False (default: False)
# - User: Olivier, Louis  (default: Olivier)
# 
# Outputs:
# - clusters with their time series
# - file with allocation of clusters to countries


def Clustering(method= "kmeans", data="af",  resize=1, number_of_clusters=None, threshold=None, documentation=True, plot=False, user="Olivier"):
    
    # Check if right inputs:
    if not method=="kmeans" and not method=="maxp" and not method=="kmedoids" and not method=="regional_kmeans" and not method=="ward":
        print("!!!WARNING!!! Wrong input in method field, only possibility are: 'kmeans', 'maxp', 'kmedoids', 'regional_kmeans', 'ward'. You put ", method)
        return

    if not data=="af" and not data=="weather":
        print("!!!WARNING!!! Wrong input in method field, only possibility are: 'af', 'weather'. You put:", data)
        return
    
    if not user=="Olivier" and not user=="Louis":
        print("!!!WARNING!!! User not know to the code, please contact either Olivier or Louis to fix this. You put:", user)
        return

    # Resize and load in the correct data  
    if documentation:
        print("start resizing and loading data")
        print("------------------------------------")
        start_resizing = time.time()

    wind, wind_copy, wind_time, solar, solar_copy, solar_time, lon, lat, coordinates, res_resized = Read_data(data, resize, plot, user, documentation)
    
    # Compute the clusters
    if documentation:
        stop_resizing = time.time()
        print("Data loading and resizing done with a computation time (h):", (stop_resizing-start_resizing)/3600)
        print("start computing clusters")
        print("------------------------------------")
        start_clustering = time.time()

    if method == "kmeans":
        labels_wind, regions_wind, labels_solar, regions_solar = Kmeans(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot)
    elif method == "maxp":
        labels_wind, regions_wind, labels_solar, regions_solar = Maxp(wind, wind_copy, solar, solar_copy, lon, lat, threshold, res_resized, plot)
    elif method == "kmedoids":
        labels_wind, regions_wind, labels_solar, regions_solar = Kmedoids(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot)
    elif method == "regional_kmeans":
        labels_wind, regions_wind, labels_solar, regions_solar = RegionalKmeans(wind, solar, lon, lat, number_of_clusters, res_resized, plot)
    elif method == "ward":
        labels_wind, regions_wind, labels_solar, regions_solar = Ward(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot)

    # Split in off-shore and on-shore
    if documentation:
        stop_clustering = time.time()
        print("Clustering done with a computation time (h):", (stop_clustering-start_clustering)/3600)
        print("start splitting off-shore and on-shore")
        print("------------------------------------")
        start_splitting_ofonshore = time.time()

    regions_wind, regions_off_shore_wind, labels_wind, regions_solar, regions_off_shore_solar, labels_solar = Split_offshore_onshore(regions_wind, labels_wind, regions_solar, labels_solar, coordinates, number_of_clusters, user)

    # Compute time series for clusters and save them in a csv
    if documentation:
        stop_splitting_ofonshore = time.time()
        print("Splitting of off-shore and on-shore done with a computation time (h):", (stop_splitting_ofonshore-start_splitting_ofonshore)/3600)
        print("Start converting to time series per cluster")
        print("------------------------------------")
        start_time_series = time.time()

    Convert_to_timeseries(wind, wind_copy, wind_time, regions_wind, regions_off_shore_wind, labels_wind, solar, solar_copy, solar_time, regions_solar, regions_off_shore_solar, labels_solar, method, data, number_of_clusters, adjusted_size, plot, user)

    # Assign clusters to countries and save it in a csv
    if documentation:
        stop_time_series = time.time()
        print("Conversion to time series of capacity factor done with a computation time (h):", (stop_time_series-start_time_series)/3600)
        print("Start asigning clusters to countries")
        print("------------------------------------")
        start_asigning_cluster = time.time()

    Asign_clusters_to_countries(regions_wind, regions_off_shore_wind, regions_solar, regions_off_shore_solar, coordinates, method, data, number_of_clusters, plot, user)
    
    if documentation:
        stop_asigning_cluster = time.time()
        print("Assignment of clusters done with a computation time (h):", (stop_asigning_cluster-start_asigning_cluster)/3600)
        print("------------------------------------")
    if plot:
        plt.show()

    return()

    
Clustering(method="ward", data="weather", number_of_clusters=10, plot=True)
    
