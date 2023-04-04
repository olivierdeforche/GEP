import time
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import libpysal
from spopt.region import MaxPHeuristic as MaxP


def Maxp(wind, wind_copy, solar, solar_copy, lon, lat, threshold, res_resized, plot):

    geo = gpd.GeoSeries.from_xy(lon, lat)
    w = libpysal.weights.lat2W(res_resized, res_resized)
    
    ### Wind
    # Start timer wind
    start_wind = time.time()
    
    ## transform to GeoDataFrame
    frame = gpd.GeoDataFrame(wind, geometry=geo)
    frame["count"] = wind_copy
    threshold_wind = threshold*np.average(wind_copy)
    threshold_wind = int(threshold_wind)
    frame.rename(columns={0:'Data'}, inplace=True )
    
    ## Name data used by MaxP method
    attrs_name = "Data"
    threshold_name = "count"
    
    # Solve clustering wind
    print("starting model")
    model = MaxP(frame, w, attrs_name, threshold_name, threshold_wind, verbose=True)
    model.solve()
    print("Model Solved, starting calculations of cluster values")
    
    labels_wind = model.labels_ 

    # Plot results wind if specified
    if plot:
        fig22 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=model.labels_)
        plt.title("Wind clusters, random colors, max-p")
        plt.plot()
    
        nr_of_clusters = np.ceil(res_resized*res_resized/threshold)
        nr_of_clusters = int(nr_of_clusters)
        clusters = dict.fromkeys(range(1,nr_of_clusters))
        clusters_values = dict.fromkeys(range(1,nr_of_clusters))
        
        for i in range(len(clusters) + 1):
            clusters[i + 1] = list()
            clusters_values[i + 1] = list()
        
        for i in range(len(model.labels_)):
            clusters[model.labels_[i]].insert(i, i)
            clusters_values[model.labels_[i]].insert(i, wind_copy[i])
        
        for key in clusters:
            average = np.average(clusters_values[key])
            for i in range(len(clusters[key])):
                wind_copy[clusters[key][i]] = average
        
        print("values relating to specific clusters calculated and ready")
        
        fig3 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=wind_copy)
        plt.title("Wind clusters, ranked with color, max-p")
    
    # Stop timer wind
    end_wind = time.time()
    print("Computation time (h):")
    print((end_wind-start_wind)/3600)

    ### Sun
    start_sun = time.time()

    ## transform to GeoDataFrame
    frame = gpd.GeoDataFrame(id, geometry=geo)
    frame["count"] = solar_copy
    threshold_sun = threshold*np.average(solar_copy)
    threshold_sun = int(threshold_sun)
    frame.rename(columns={0:'Data'}, inplace=True )

    ## Name data used by MaxP method
    attrs_name = "Data"
    threshold_name = "count"

    # Solve clustering solar
    print("starting model")
    model = MaxP(frame, w, attrs_name, threshold_name, threshold_sun, verbose=True)
    model.solve()
    print("Model Solved, starting calculations of cluster values")

    labels_solar = model.labels_
    
    # Plot results wind if specified
    if plot: 
        fig5 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=model.labels_)
        plt.title("Sun clusters, random colors, max-p")

        nr_of_clusters = np.ceil(res_resized*res_resized/threshold)
        nr_of_clusters = int(nr_of_clusters)
        clusters = dict.fromkeys(range(1,nr_of_clusters))
        clusters_values = dict.fromkeys(range(1,nr_of_clusters))

        for i in range(len(clusters) + 1):
            clusters[i + 1] = list()
            clusters_values[i + 1] = list()

        for i in range(len(model.labels_)):
            clusters[model.labels_[i]].insert(i, i)
            clusters_values[model.labels_[i]].insert(i, solar_copy[i])

        for key in clusters:
            average = np.average(clusters_values[key])
            for i in range(len(clusters[key])):
                solar_copy[clusters[key][i]] = average

        print("values relating to specific clusters calculated and ready")

        fig6 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=solar_copy)
        plt.title("Sun clusters, ranked with color, max-p")

    # End timer
    end_sun = time.time()
    print("Computation time sun (h)")
    print((end_sun-start_sun)/3600)

    # Returns values
    return(labels_wind, labels_solar) # TBC
