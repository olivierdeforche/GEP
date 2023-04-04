import Read_data
import Kmeans
import Kmedoids
import Maxp
import RegionalKmeans
import Ward
import Convert_to_timeseries
import Assign_clusters_to_countries
import matplotlib.pyplot as plt

## Main Function
# This function converts the weather data from Era to clusters with their 
# respective capacity factors in time series:
# Inputs: 
# - method: kmeans, maxp, kmedoids, regional_kmeans, ward
# - data: weather, af (default: weather)
# - size: number (default: 1)
# - number_of_clusters: (default: None)
# - threshold=None
# - plot: True, False (default: False)
# - User: Olivier, Louis  (default: Olivier)
# 
# Outputs:
# - clusters with their time series
# - file with allocation of clusters to countries


def Clustering(method= "kmeans", data="af",  resize=1, number_of_clusters=None, threshold=None, plot=False, user="Olivier"):
    
    # Resize and load in the correct data
    wind, wind_copy, solar, solar_copy, lon, lat, res_resized = Read_data(data, resize, plot, user)

    # Compute the clusters
    if method == "kmeans":
        labels_wind, labels_solar = Kmeans(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot)
    elif method == "maxp":
        labels_wind, labels_solar = Maxp(wind, wind_copy, solar, solar_copy, lon, lat, threshold, res_resized, plot)
    elif method == "kmedoids":
        labels_wind, labels_solar = Kmedoids(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot)
    elif method == "regional_kmeans":
        labels_wind, labels_solar = RegionalKmeans(wind, solar, lon, lat, number_of_clusters, res_resized, plot)
    elif method == "ward":
        labels_wind, labels_solar = Ward(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot)
    
    # Compute time series for clusters and save them in a csv
    Convert_to_timeseries(wind, labels_wind, solar, labels_solar)

    # Assign clusters to countries and save it in a csv
    Assign_clusters_to_countries(wind, labels_wind, plot, solar, labels_solar)

    # plt.show()
    return()
    

    
