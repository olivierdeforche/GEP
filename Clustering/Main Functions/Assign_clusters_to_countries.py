import geopandas
import atlite
import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon


def Asign_clusters_to_countries(regions_wind, regions_off_shore_wind, number_of_clusters_wind, regions_solar, regions_off_shore_solar, number_of_clusters_solar, coordinates, method, data, documentation, plot, user):
    
    # Load data of Exclusive Economic Zones 
    if user =="Olivier":
        EEZ = geopandas.read_file('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/EEZ_Europe_land.geojson')
    else:
        EEZ = geopandas.read_file('"C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/EEZ_Europe_land.geojson')

    # Create dictionaries for each file we want to create 
    dict_wind = dict()
    dict_wind_offshore = dict()
    dict_solar = dict()
    dict_solar_offshore = dict()

    # Put each zone of the EEZ as keys in the dictionaries with 
    for country_name in EEZ["UNION"]:
        dict_wind[country_name] = np.zeros(len(regions_wind))
        dict_wind_offshore[country_name] = np.zeros(len(regions_off_shore_wind))
        dict_solar[country_name] = np.zeros(len(regions_solar))
        dict_solar_offshore[country_name] = np.zeros(len(regions_off_shore_solar))
        
    dict_wind["total"] = np.zeros(len(regions_wind))
    dict_wind_offshore["total"] = np.zeros(len(regions_off_shore_wind))
    dict_solar["total"] = np.zeros(len(regions_solar))
    dict_solar_offshore["total"] = np.zeros(len(regions_off_shore_solar))


    ## Wind
    # Regions wind: assign the correct percentages to the respective country
    cluster_number = 0
    for cluster in regions_wind:
        size_cluster = len(cluster)
        for number in cluster:
            i = 0
            for polygon in EEZ["geometry"]:
                if polygon.contains(coordinates[number]):
                    dict_wind[EEZ["UNION"][i]][cluster_number] += 1/size_cluster
                i += 1
        cluster_number +=1

    
    for i in range(cluster_number):
        total_percentage = 0
        for country in EEZ["UNION"]:
            total_percentage += dict_wind[country][i]
        dict_wind["total"][i] = total_percentage


    # Regions offshore wind: assign the correct percentages to the respective country
    cluster_number = 0
    for cluster in regions_off_shore_wind:
        size_cluster = len(cluster)
        for number in cluster:
            i = 0
            for polygon in EEZ["geometry"]:
                if polygon.contains(coordinates[number]):
                    dict_wind_offshore[EEZ["UNION"][i]][cluster_number] += 1/size_cluster
                i += 1
        cluster_number +=1

    for i in range(cluster_number):
        total_percentage = 0
        for country in EEZ["UNION"]:
            total_percentage += dict_wind_offshore[country][i]
        dict_wind_offshore["total"][i] = total_percentage

    if documentation:
        print("wind done")

    ## Solar
    # Regions solar: assign the correct percentages to the respective country
    cluster_number = 0
    for cluster in regions_solar:
        size_cluster = len(cluster)
        for number in cluster:
            i = 0
            for polygon in EEZ["geometry"]:
                if polygon.contains(coordinates[number]):
                    dict_solar[EEZ["UNION"][i]][cluster_number] += 1/size_cluster
                i += 1
        cluster_number +=1

    for i in range(cluster_number):
        total_percentage = 0
        for country in EEZ["UNION"]:
            total_percentage += dict_solar[country][i]
        dict_solar["total"][i] = total_percentage

    # Regions offshore solar: assign the correct percentages to the respective country
    cluster_number = 0
    for cluster in regions_off_shore_solar:
        size_cluster = len(cluster)
        for number in cluster:
            i = 0
            for polygon in EEZ["geometry"]:
                if polygon.contains(coordinates[number]):
                    dict_solar_offshore[EEZ["UNION"][i]][cluster_number] += 1/size_cluster
                i += 1
        cluster_number +=1

    for i in range(cluster_number):
        total_percentage = 0
        for country in EEZ["UNION"]:
            total_percentage += dict_solar_offshore[country][i]
        dict_solar_offshore["total"][i] = total_percentage

    if documentation:
        print("solar done")

    # Save the dictionaries to excel files
    df_wind = pd.DataFrame.from_dict(dict_wind)
    df_wind_offshore = pd.DataFrame.from_dict(dict_wind_offshore)
    df_solar = pd.DataFrame.from_dict(dict_solar)
    df_solar_offshore = pd.DataFrame.from_dict(dict_solar_offshore)

    df_wind = df_wind.T
    df_wind_offshore = df_wind_offshore.T
    df_solar = df_solar.T
    df_solar_offshore = df_solar_offshore.T

    if plot:
        print(df_wind, df_wind_offshore, df_solar, df_solar_offshore)

    if user=="Olivier":
        string_wind = str('C:/Users/defor/Desktop/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_df_wind.xlsx')
        string_wind_offshore = str('C:/Users/defor/Desktop/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_df_wind_offshore.xlsx')
        string_solar = str('C:/Users/defor/Desktop/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_df_solar.xlsx')
        string_solar_offshore = str('C:/Users/defor/Desktop/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_df_solar_offshore.xlsx')
        
        df_wind.T.to_excel(string_wind)
        df_wind_offshore.T.to_excel(string_wind_offshore)
        df_solar.T.to_excel(string_solar)
        df_solar_offshore.T.to_excel(string_solar_offshore)
    else:
        string_wind = str('C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_df_wind.xlsx')
        string_wind_offshore = str('C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_wind)+str('_')+str(data)+str('_df_wind_offshore.xlsx')
        string_solar = str('C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_df_solar.xlsx')
        string_solar_offshore = str('C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/Output_Clusters_Asigned_To_Countries/')+str(method)+str('_')+str(number_of_clusters_solar)+str('_')+str(data)+str('_df_solar_offshore.xlsx')
        
        df_wind.T.to_excel(string_wind)
        df_wind_offshore.T.to_excel(string_wind_offshore)
        df_solar.T.to_excel(string_solar)
        df_solar_offshore.T.to_excel(string_solar_offshore)

    return()    