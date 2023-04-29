from spopt.region import RegionKMeansHeuristic
import numpy as np
import matplotlib.pyplot as plt
import time
import libpysal

def RegionalKmeans(wind, solar, lon, lat, number_of_clusters ,res_resized, plot, user, data, resize):
    ### Wind
    # Begin timer
    start_wind = time.time()

    w = libpysal.weights.lat2W((142//resize), (191//resize))

    wind = np.array(wind)
 
    print("ready for model")
    model = RegionKMeansHeuristic(wind, number_of_clusters, w)
    model.solve()
    print("Done with clustering wind")
    labels_wind = model.labels_
    centroids_wind = model.centroids_
    areas_wind = np.arange((142//resize) * (191//resize))
    regions_wind = [areas_wind[model.labels_ == region] for region in range(number_of_clusters)]
    print("model done")
    # Plot clustered zones if specified 
    fig2 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
        c=model.labels_)
    plt.title("Wind clusters, random colors, kmeans")
    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.svg')
        plt.savefig(string_wind, format='svg')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_random.svg')
        plt.savefig(string_wind, format='svg') # @Louis TBD

    wind = np.array(wind) 
    wind = list(np.concatenate(wind).flat)

    for i in range(number_of_clusters):
        for j in range(len(regions_wind[i])):
            wind[regions_wind[i][j]] = centroids_wind[i]

    fig3 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
        c=wind)
    plt.title("Wind clusters, ranked with color, kmeans")
    if user=="Olivier":
        string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.svg')
        plt.savefig(string_wind, format='svg')
    else:
        string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind.svg')
        plt.savefig(string_wind, format='svg') # @Louis TBD



    # End timer
    end_wind = time.time()
    print("Computation time wind (h):")
    print((end_wind-start_wind)/3600)

    ### Sun
    # Begin timer
    start_sun = time.time()

    solar = np.array(solar)

    model = RegionKMeansHeuristic(solar, number_of_clusters, w)
    model.solve()
    print("done with clustering sun")
    labels_solar = model.labels_
    centroids_solar = model.centroids_ 
    areas_solar = np.arange((142//resize) * (191//resize))
    regions_solar = [areas_solar[model.labels_ == region] for region in range(number_of_clusters)]

    # Plot results clustering sun if plot enabled 
    solar = np.array(solar)
    solar = list(np.concatenate(solar).flat)

    for i in range(number_of_clusters):
        for j in range(len(regions_solar[i])):
             solar[regions_solar[i][j]] = centroids_solar[i]

    fig5 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
        c=model.labels_)
    plt.title("Sun clusters, random colors, kmeans")
    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.svg')
        plt.savefig(string_solar, format='svg')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_random.svg')
        plt.savefig(string_solar, format='svg') # @Louis TBD


    fig6 = plt.figure(figsize=(6, 6))
    plt.scatter(lon, lat,
        c=solar)
    plt.title("Sun clusters, ranked with color, kmeans")
    if user=="Olivier":
        string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.svg')
        plt.savefig(string_solar, format='svg')
    else:
        string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar.svg')
        plt.savefig(string_solar, format='svg') # @Louis TBD


    # End timer
    end_sun = time.time()
    print("Computation time sun (h)")
    print((start_sun-end_sun)/3600)

    return(labels_wind, regions_wind, labels_solar, regions_solar) 