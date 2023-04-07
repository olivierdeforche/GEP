import geopandas
import atlite
import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon


def Asign_clusters_to_countries(regions_wind, regions_off_shore_wind, regions_solar, regions_off_shore_solar, coordinates, method, data, number_of_clusters, plot, user):
    
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

    # Save the dictionaries to excel files
    df_wind = pd.DataFrame(data=dict_wind, index=[0])
    df_wind_offshore = pd.DataFrame(data=dict_wind_offshore, index=[0])
    df_solar = pd.DataFrame(data=dict_solar, index=[0])
    df_solar_offshore = pd.DataFrame(data=dict_solar_offshore, index=[0])

    df_wind = (df_wind.T)
    df_wind_offshore = (df_wind_offshore.T)
    df_solar = (df_solar.T)
    df_solar_offshore = (df_solar_offshore.T)

    if plot:
        print(df_wind, df_wind_offshore, df_solar, df_solar_offshore)

    if user=="Olivier":
        df_wind.to_excel('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Asigned_To_Countries/',method,'_',number_of_clusters,'_',data,'_df_wind.xlsx')
        df_wind_offshore.to_excel('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Asigned_To_Countries/',method,'_',number_of_clusters,'_',data,'_df_wind_offshore.xlsx')
        df_solar.to_excel('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Asigned_To_Countries/',method,'_',number_of_clusters,'_',data,'_df_solar.xlsx')
        df_solar_offshore.to_excel('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Output_Clusters_Asigned_To_Countries/',method,'_',number_of_clusters,'_',data,'_df_solar_offshore.xlsx')
    else:
        df_wind.to_excel('TBD/df_wind.xlsx') #@Louis
        df_wind_offshore.to_excel('TBD/df_wind_offshore.xlsx') #@Louis
        df_solar.to_excel('TBD/df_solar.xlsx') #@Louis
        df_solar_offshore.to_excel('TBD/df_solar_offshore.xlsx') #@Louis

    return()