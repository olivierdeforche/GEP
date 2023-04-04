from sklearn.cluster import KMeans
import time
import matplotlib.pyplot as plt
import numpy as np

def Kmeans(wind, wind_copy, solar, solar_copy, lon, lat, n_clusters, res_resized, plot):
    RANDOM_SEED = 123456

    ### Wind
    # Start timer
    start_wind = time.time()
    print("starting model")

    # Solve model wind
    model = KMeans(n_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(wind)
    model.solve()
    print("Model Solved, starting calculations of cluster values")

    # Get values
    labels_wind = model.labels_
    clusters = dict.fromkeys(range(1, n_clusters))
    clusters_values = dict.fromkeys(range(1, n_clusters))

    # Plot results if specified in plot variable (=True)
    if plot:
        fig2 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=model.labels_)
        plt.title("Wind clusters, random colors, KMeans++")

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

    # End timer
    end_wind = time.time()
    print("Computation time (h):")
    print((end_wind-start_wind)/3600)

    ### Sun
    # Start timer
    start_sun = time.time()

    # Solver model solar
    print("starting model")
    model = KMeans(n_clusters, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0).fit(solar)
    print("Model Solved, starting calculations of cluster values")

    labels_solar = model.labels_

    clusters = dict.fromkeys(range(1, n_clusters))
    clusters_values = dict.fromkeys(range(1, n_clusters))

    if plot: 
        fig5 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=model.labels_)
        plt.title("Sun clusters, random colors, KMeans++")

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

    end_sun = time.time()
    print("Computation time (h):")
    print((end_sun-start_sun)/3600)

    return(labels_wind, labels_solar)
