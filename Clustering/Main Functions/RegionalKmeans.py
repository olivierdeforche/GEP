from spopt.region import RegionKMeansHeuristic
import numpy as np
import matplotlib.pyplot as plt
import time
import libpysal

def RegionalKmeans(wind, solar, lon, lat, clusters ,res_resized, plot):
    ### Wind
    # Begin timer
    start_wind = time.time()

    w = libpysal.weights.lat2W(res_resized, res_resized)

    wind = np.array(wind)

    model = RegionKMeansHeuristic(wind, clusters, w)
    model.solve()
    print("Done with clustering wind")
    labels_wind = model.labels_
    centroids_wind = model.centroids_
    areas_wind = np.arange(res_resized * res_resized)
    regions_wind = [areas_wind[model.labels_ == region] for region in range(clusters)]

    # Plot clustered zones if specified
    if plot:
        fig2 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=model.labels_)
        plt.title("Wind clusters, random colors, kmeans")

        wind = np.array(wind)
        wind = list(np.concatenate(wind).flat)

        for i in range(clusters):
            for j in range(len(regions_wind[i])):
                wind[regions_wind[i][j]] = centroids_wind[i]

        fig3 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=wind)
        plt.title("Wind clusters, ranked with color, kmeans")

    # End timer
    end_wind = time.time()
    print("Computation time wind (h):")
    print((end_wind-start_wind)/3600)

    ### Sun
    # Begin timer
    start_sun = time.time()

    solar = np.array(solar)

    model = RegionKMeansHeuristic(solar, clusters, w)
    model.solve()
    print("done with clustering sun")
    labels_solar = model.labels_
    centroids_solar = model.centroids_ 
    areas_solar = np.arange(res_resized * res_resized)
    regions_solar = [areas_solar[model.labels_ == region] for region in range(clusters)]

    # Plot results clustering sun if plot enabled 
    if plot:
        solar = np.array(solar)
        solar = list(np.concatenate(solar).flat)

        for i in range(clusters):
            for j in range(len(regions_solar[i])):
                solar[regions_solar[i][j]] = centroids_solar[i]

        fig5 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=model.labels_)
        plt.title("Sun clusters, random colors, kmeans")


        fig6 = plt.figure(figsize=(6, 6))
        plt.scatter(lon, lat,
                c=solar)
        plt.title("Sun clusters, ranked with color, kmeans")

    # End timer
    end_sun = time.time()
    print("Computation time sun (h)")
    print((start_sun-end_sun)/3600)

#     return(labels_solar, labels_wind, centroids_solar, centroids_wind, areas_wind, areas_solar) # TBC
    return(labels_wind, labels_solar) 