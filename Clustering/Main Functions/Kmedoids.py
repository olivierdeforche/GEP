import time
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import kmedoids
import numpy as np

def Kmedoids(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot, user, data, resize):
    
    ### Wind
    # Start timer
    start_wind = time.time()

    # Select distance wind
    diss = euclidean_distances(wind)

    # Solve model wind
    print("starting model")
    model = kmedoids.fasterpam(diss, number_of_clusters, max_iter=100, init='random', random_state=None, n_cpu=-1)
    print("Model Solved, starting calculations of cluster values")

    labels_wind = model.labels
    areas = np.arange((142//resize) * (191//resize))
    regions_wind = [areas[labels_wind == region] for region in range(number_of_clusters)]

    # Plot results wind if specified (plot=True)

    fig22 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=model.labels)
    plt.title("Wind clusters, random colors, k-medoids")
    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.eps')
        plt.savefig(string_wind, format='eps')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.eps')
        plt.savefig(string_wind, format='eps') # @Louis TBD


    clusters = dict.fromkeys(range(1, number_of_clusters))
    clusters_values = dict.fromkeys(range(1, number_of_clusters))

    for i in range(len(clusters) + 1):
        clusters[i + 1] = list()
        clusters_values[i + 1] = list()

    for i in range(len(model.labels)):
        clusters[model.labels[i]+1].insert(i, i)
        clusters_values[model.labels[i]+1].insert(i, wind_copy[i])

    for key in clusters:
        average = np.average(clusters_values[key])
        for i in range(len(clusters[key])):
            wind_copy[clusters[key][i]] = average

    fig3 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=wind_copy)
    plt.title("Wind clusters, ranked with color, k-medoids")
    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.eps')
        plt.savefig(string_wind, format='eps')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.eps')
        plt.savefig(string_wind, format='eps') # @Louis TBD

    # End timer
    end_wind = time.time()
    print("Computation time (h):")
    print((end_wind-start_wind)/3600)


    ### Sun
    # Start timer solar
    start_sun = time.time()

    # Select distance solar
    diss = euclidean_distances(solar)

    # Solve model solar
    print("starting model")
    model = kmedoids.fasterpam(diss, number_of_clusters, max_iter=100, init='random', random_state=None, n_cpu=-1)
    print("Model Solved, starting calculations of cluster values")

    labels_solar = model.labels
    regions_solar = [areas[labels_solar == region] for region in range(number_of_clusters)]

    # Plot results solar if specified (plot=True)

    fig5 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=model.labels)
    plt.title("Sun clusters, random colors, k-medoids")
    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.eps')
        plt.savefig(string_solar, format='eps')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.eps')
        plt.savefig(string_solar, format='eps') # @Louis TBD


    clusters = dict.fromkeys(range(1, number_of_clusters))
    clusters_values = dict.fromkeys(range(1, number_of_clusters))

    for i in range(len(clusters) + 1):
        clusters[i + 1] = list()
        clusters_values[i + 1] = list()

    for i in range(len(model.labels)):
        clusters[model.labels[i]+1].insert(i, i)
        clusters_values[model.labels[i]+1].insert(i, solar_copy[i])

    for key in clusters:
        average = np.average(clusters_values[key])
        for i in range(len(clusters[key])):
            solar_copy[clusters[key][i]] = average

    fig6 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=solar_copy)
    plt.title("Sun clusters, ranked with color, k-medoids")
    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.eps')
        plt.savefig(string_solar, format='eps')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.eps')
        plt.savefig(string_solar, format='eps') # @Louis TBD

    # End timer solar
    end_sun = time.time()
    print("Computation time (h):")
    print((end_sun-start_sun)/3600)

    return(labels_wind, regions_wind, labels_solar, regions_solar)