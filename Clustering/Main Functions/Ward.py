import geopandas as gpd
import numpy as np
from spopt.region import WardSpatial
import matplotlib.pyplot as plt
import libpysal
import time


def Ward(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot, user, data, resize):
    
    ### Wind
    # Start timer wind
    start_wind = time.time()

    ## transform to GeoDataFrame
    geo = gpd.GeoSeries.from_xy(lon, lat)
    frame = gpd.GeoDataFrame(wind, geometry=geo)

    #frame["count"] = 1
    frame.rename(columns={0:'Data'}, inplace=True )

    # Name data used by Ward method
    attrs_name = ["Data"]
    attrs_name = np.array(attrs_name)

    # Spatial weights
    w = libpysal.weights.lat2W((142//resize), (191//resize))

    # Solve model wind
    print("starting model")
    model = WardSpatial(frame, w, attrs_name, number_of_clusters)
    model.solve()
    print("Model Solved, starting calculations of cluster values")

    labels_wind = model.labels_
    areas = np.arange((142//resize) * (191//resize))
    regions_wind = [areas[model.labels_ == region] for region in range(number_of_clusters)]

    # Plot resutls wind if specified (plot=True)
    fig2 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=model.labels_)
    plt.title("Wind clusters, random colors, Ward HAC")
    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.eps')
        plt.savefig(string_wind, format='eps')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.eps')
        plt.savefig(string_wind, format='eps') # @Louis TBD


    clusters = dict.fromkeys(range(1, number_of_clusters))
    clusters_values = dict.fromkeys(range(1, number_of_clusters))

    for i in range(len(clusters) + 1):
        clusters[i + 1] = list()
        clusters_values[i + 1] = list()


    for i in range(len(model.labels_)):
        clusters[model.labels_[i]+1].insert(i, i)
        clusters_values[model.labels_[i]+1].insert(i, wind_copy[i])

    for key in clusters:
        average = np.average(clusters_values[key])
        for i in range(len(clusters[key])):
            wind_copy[clusters[key][i]] = average

    fig3 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=wind_copy)
    plt.title("Wind clusters, ranked with color, Ward HAC")
    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.eps')
        plt.savefig(string_wind, format='eps')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.eps')
        plt.savefig(string_wind, format='eps') # @Louis TBD

    # Stop timer wind
    end_wind = time.time()
    print("Computation time wind (h):")
    print((end_wind-start_wind)/3600)


    ### Sun
    # Start timer sun
    start_sun = time.time()

    # Transform to GeoDataFrame
    frame = gpd.GeoDataFrame(solar, geometry=geo)
    frame.rename(columns={0:'Data'}, inplace=True )

    # Name data used by Ward method
    attrs_name = ["Data"]
    attrs_name = np.array(attrs_name)

    # Solve model solar
    print("starting model")
    model = WardSpatial(frame, w, attrs_name, number_of_clusters)
    model.solve()
    print("Model Solved, starting calculations of cluster values")

    labels_solar = model.labels_
    regions_solar = [areas[model.labels_ == region] for region in range(number_of_clusters)]

    # Plot results solar if specified (plot=True)
    fig5 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=model.labels_)
    plt.title("Sun clusters, random colors, Ward HAC")

    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.eps')
        plt.savefig(string_solar, format='eps')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.eps')
        plt.savefig(string_solar, format='eps') # @Louis TBD

    clusters = dict.fromkeys(range(1, number_of_clusters))
    clusters_values = dict.fromkeys(range(1, number_of_clusters))

    for i in range(len(clusters) + 1):
        clusters[i + 1] = list()
        clusters_values[i + 1] = list()

    for i in range(len(model.labels_)):
        clusters[model.labels_[i]+1].insert(i, i)
        clusters_values[model.labels_[i]+1].insert(i, solar_copy[i])

    for key in clusters:
        average = np.average(clusters_values[key])
        for i in range(len(clusters[key])):
            solar_copy[clusters[key][i]] = average

    fig6 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=solar_copy)
    plt.title("Sun clusters, ranked with color, Ward HAC")

    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.eps')
        plt.savefig(string_solar, format='eps')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.eps')
        plt.savefig(string_solar, format='eps') # @Louis TBD

    # End timer solar
    end_sun = time.time()
    print("Computation time sun (h):")
    print((end_sun-start_sun)/3600)
    
    return(labels_wind, regions_wind, labels_solar, regions_solar)