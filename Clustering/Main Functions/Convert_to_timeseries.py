import numpy as np
import pandas as pd
import time

def Convert_to_timeseries(wind_copy, wind_time, labels_wind, number_of_clusters_wind, current_amount_of_clusters_wind, to_remove_wind, solar_copy, solar_time, labels_solar, number_of_clusters_solar, current_amount_of_clusters_solar, to_remove_solar, method, data, documentation, plot, user):

    ### Wind
    # Start timer wind
    start_wind = time.time()

    clusters_wind = dict()
    # clusters_values_wind = dict()
    clusters_one_time_wind = dict()
    clusters_one_time_wind_offshore = dict()
    
    # Put a list after every key
    for i in range(current_amount_of_clusters_wind):
        
        clusters_wind[i] = list()
        # clusters_values_wind[i] = list()
        
        if i < number_of_clusters_wind-len(to_remove_wind):
            clusters_one_time_wind[i] = list()
        if i < current_amount_of_clusters_wind-number_of_clusters_wind:
            clusters_one_time_wind_offshore[i] = list()

    # Time series per point
    for i in range(len(labels_wind)):
        clusters_wind[labels_wind[i]].append(i)
        # clusters_values_wind[labels_wind[i]].append(wind_copy[i])

    # Put the average time series per cluster in the dict
    k = 0
    for key in clusters_wind.keys():
        if key in to_remove_wind:
            k += 1
        else:
            for i in range(len(wind_time)):
                average_wind = list()
                for value in clusters_wind[key]:
                    average_wind.append(wind_time[i][value])
                average_wind = np.average(average_wind) 
                if key < number_of_clusters_wind:
                    clusters_one_time_wind[key-k].append(average_wind)
                else:
                    clusters_one_time_wind_offshore[key-number_of_clusters_wind].append(average_wind)

    # Convert dictionaries to be able to save
    df_clustered_on_wind = pd.DataFrame.from_dict(clusters_one_time_wind)   
    df_clustered_on_wind_offshore = pd.DataFrame.from_dict(clusters_one_time_wind_offshore)

    if documentation:
        print("conversion wind done, saving now")
    if user=="Olivier":
        string = str('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Timeseries/')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_clustered_on_wind.xlsx')
        string_offshore = str('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Timeseries/')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_clustered_on_wind_offshore.xlsx')
        df_clustered_on_wind.to_excel(string)
        df_clustered_on_wind_offshore.to_excel(string_offshore)
    else:
        string = str('TBD')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_clustered_on_wind.xlsx')
        string_offshore = str('TBD')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_clustered_on_wind_offshore.xlsx')
        df_clustered_on_wind.to_excel(string) #@Louis
        df_clustered_on_wind_offshore.to_excel(string_offshore) #@Louis

    # Stop timer wind
    end_wind = time.time()
    print("Computation time wind (h):")
    print((end_wind-start_wind)/3600)

    ### Solar
    # Start timer solar
    start_solar = time.time()
    
    clusters_solar = dict()
    clusters_values_solar = dict()
    clusters_one_time_solar = dict()
    clusters_one_time_solar_offshore = dict()
    
    # Put a list after every key
    for i in range(current_amount_of_clusters_solar):
        
        clusters_solar[i] = list()
        clusters_values_solar[i] = list()
        
        if i < number_of_clusters_solar-len(to_remove_solar):
            clusters_one_time_solar[i] = list()
        if i < current_amount_of_clusters_solar-number_of_clusters_solar:
            clusters_one_time_solar_offshore[i] = list()

    # Time series per point
    for i in range(len(labels_solar)):
        clusters_solar[labels_solar[i]].append(i)
        clusters_values_solar[labels_solar[i]].append(solar_copy[i])

    # Put the average time series per cluster in the dict
    k = 0
    for key in clusters_solar.keys():
        if key in to_remove_solar:
            k += 1
        else:
            for i in range(len(solar_time)):
                average_solar = list()
                for value in clusters_solar[key]:
                    average_solar.append(solar_time[i][value])
                average_solar = np.average(average_solar) 
                if key < number_of_clusters_solar:
                    clusters_one_time_solar[key-k].append(average_solar)
                else:
                    clusters_one_time_solar_offshore[key-number_of_clusters_solar].append(average_solar)

    # Convert dictionaries to be able to save
    df_clustered_on_solar = pd.DataFrame.from_dict(clusters_one_time_solar)   
    df_clustered_on_solar_offshore = pd.DataFrame.from_dict(clusters_one_time_solar_offshore)

    if documentation:
        print("conversion solar done, saving now")
    

    if user=="Olivier":
        string = str('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Timeseries/')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_clustered_on_solar.xlsx')
        string_offshore = str('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Timeseries/')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_clustered_on_solar_offshore.xlsx')
        df_clustered_on_solar.to_excel(string)
        df_clustered_on_solar_offshore.to_excel(string_offshore)
    else:
        string = str('TBD')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_clustered_on_solar.xlsx')
        string_offshore = str('TBD')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_clustered_on_solar_offshore.xlsx')
        df_clustered_on_solar.to_excel(string) #@Louis
        df_clustered_on_solar_offshore.to_excel(string_offshore) #@Louis

    # Stop timer solar
    end_solar = time.time()
    print("Computation time wind (h):")
    print((end_solar-start_solar)/3600)

    return()