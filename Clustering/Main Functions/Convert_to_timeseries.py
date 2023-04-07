import numpy as np
import pandas as pd

def Convert_to_timeseries(wind, wind_copy, wind_time, regions_wind, regions_off_shore_wind, labels_wind, solar, solar_copy, solar_time, regions_solar, regions_off_shore_solar, labels_solar, method, data, number_of_clusters, adjusted_size, plot, user):

    ### Wind
    clusters_wind = dict.fromkeys(range(0, number_of_clusters-1))
    clusters_values_wind = dict.fromkeys(range(0, number_of_clusters-1))
    clusters_time_wind = dict.fromkeys(range(0, number_of_clusters-1))
    clusters_one_time_wind = dict.fromkeys(range(0, number_of_clusters-1))

    # Put a list after every key
    for i in range(len(clusters_wind) + 1):
        clusters_wind[i] = list()
        clusters_values_wind[i] = list()
        clusters_time_wind[i] = list()
        clusters_one_time_wind[i] = list()

    # Time series per point
    for i in range(len(labels_wind)):
        clusters_wind[labels_wind[i]].append(i)
        clusters_values_wind[labels_wind[i]].append(wind_copy[i])

    # Put the average time series per cluster in the dict
    for key in clusters_wind:
        for i in range(len(wind_time)):
            average_wind = list()
            for value in clusters_wind[key]:
                average_wind.append(wind_time[i][value])
            average_wind = np.average(average_wind)
            clusters_one_time_wind[key].append(average_wind)

    df_clustered_on_wind = pd.DataFrame(data=clusters_one_time_wind, index=[0])

    
    df_clustered_on_wind = (df_clustered_on_wind.T)

    if plot:
        print(df_clustered_on_wind)
    
    if user=="Olivier":
        df_clustered_on_wind.to_excel('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Timeseries/',method,'_',number_of_clusters,'_',data,'_clustered_on_wind.xlsx')
    else:
        df_clustered_on_wind.to_excel('TBD',method,'_',number_of_clusters,'_',data,'_clustered_on_wind.xlsx') #@Louis



    ## solar
    clusters_solar = dict.fromkeys(range(1, number_of_clusters))
    clusters_values_solar = dict.fromkeys(range(1, number_of_clusters))
    clusters_time_solar = dict.fromkeys(range(1, number_of_clusters))
    clusters_one_time_solar = dict.fromkeys(range(1, number_of_clusters))

    for i in range(len(clusters_solar) + 1):
        clusters_solar[i + 1] = list()
        clusters_values_solar[i + 1] = list()
        clusters_time_solar[i+1] = list()
        clusters_one_time_solar[i+1] = list()


    for i in range(len(labels_solar)):
        clusters_solar[labels_solar[i]+1].append(i)
        clusters_values_solar[labels_solar[i]+1].append(solar_copy[i])

    for key in clusters_solar:
        for i in range(len(solar_time)):
            average_solar = list()
            for value in clusters_solar[key]:
                average_solar.append(solar_time[i][value])
            average_solar = np.average(average_solar)
            clusters_one_time_solar[key].append(average_solar)


    df_clustered_on_solar = pd.DataFrame(data=clusters_one_time_solar, index=[0])
    df_clustered_on_solar = (df_clustered_on_solar.T)

    if plot:
        print(df_clustered_on_solar)
    
    if user=="Olivier":
        df_clustered_on_solar.to_excel('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Timeseries/',method,'_',number_of_clusters,'_',data,'_clustered_on_solar.xlsx')
    else:
        df_clustered_on_solar.to_excel('TBD',method,'_',number_of_clusters,'_',data,'_clustered_on_solar.xlsx') #@Louis



    return()