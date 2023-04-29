from sklearn.cluster import KMeans
import time
import matplotlib.pyplot as plt
import numpy as np

def Kmeans(wind, wind_copy, solar, solar_copy, lon, lat, number_of_clusters, res_resized, plot, user, data, resize):
    RANDOM_SEED = 123456

    ### Wind
    # Start timer
    start_wind = time.time()
    print("starting model")

    # Solve model wind
    model = KMeans(number_of_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(wind)
    print("Model Solved, starting calculations of cluster values")

    # Get values
    labels_wind = model.labels_
    areas = np.arange((142//resize) * (191//resize))
    regions_wind = [areas[model.labels_ == region] for region in range(number_of_clusters)]

    clusters = dict.fromkeys(range(1, number_of_clusters))
    clusters_values = dict.fromkeys(range(1, number_of_clusters))

    # Plot results if specified in plot variable (=True)

    fig2 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=model.labels_)
    plt.title("Wind clusters, random colors, KMeans++")

    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.svg')
        plt.savefig(string_wind, format='svg')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.svg')
        plt.savefig(string_wind, format='svg') # @Louis TBD

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
    plt.title("Wind clusters, ranked with color, KMeans++")

    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.svg')
        plt.savefig(string_wind, format='svg')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.svg')
        plt.savefig(string_wind, format='svg') # @Louis TBD

    # End timer
    end_wind = time.time()
    print("Computation time (h):")
    print((end_wind-start_wind)/3600)

    ### Sun
    # Start timer
    start_sun = time.time()

    # Solver model solar
    print("starting model")
    model = KMeans(number_of_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(solar)
    print("Model Solved, starting calculations of cluster values")

    labels_solar = model.labels_
    regions_solar = [areas[model.labels_ == region] for region in range(number_of_clusters)]

    clusters = dict.fromkeys(range(1, number_of_clusters))
    clusters_values = dict.fromkeys(range(1, number_of_clusters))


    fig5 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
            c=model.labels_)
    plt.title("Sun clusters, random colors, KMeans++")

    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.svg')
        plt.savefig(string_solar, format='svg')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.svg')
        plt.savefig(string_solar, format='svg') # @Louis TBD


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
    plt.title("Sun clusters, ranked with color, KMeans++")

    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.svg')
        plt.savefig(string_solar, format='svg')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.svg')
        plt.savefig(string_solar, format='svg') # @Louis TBD

    end_sun = time.time()
    print("Computation time (h):")
    print((end_sun-start_sun)/3600)

    return(labels_wind, regions_wind, labels_solar, regions_solar)
