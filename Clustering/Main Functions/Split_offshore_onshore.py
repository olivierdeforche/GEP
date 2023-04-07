import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

def Split_offshore_onshore(regions_wind, labels_wind, regions_solar, labels_solar, coordinates, number_of_clusters, user):

    # Load in polygon of Europe
    if user=='Olivier':
        europe_land = gpd.read_file("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/europe.geojson")
    else:
        europe_land = gpd.read_file("[TODO]") #@Louis check


    # Take out geometry out of Geoseries file
    europe_land = europe_land.geometry[0]

    # Wind: Split clusters in off and on shore
    regions_off_shore_wind = list()
    current_amount_of_clusters = number_of_clusters

    for i in range(len(regions_wind)):

        # Create list in list of Off-shore clusters
        regions_off_shore_wind.append(list())
        
        # Check for every coordinate in the cluster if they are in the sea, if so --> take the coordinate
        # out of the current cluster and put it in a new cluster of off-shore locations of that cluster
        for number in regions_wind[i]:
            if not europe_land.contains(coordinates[number]):
                regions_wind[i] = regions_wind[i][regions_wind[i] != number]
                regions_off_shore_wind[-1].append(number)
                labels_wind[number] = current_amount_of_clusters
        
        # If no point of the cluster is in the sea, delete the empty list, else update the current 
        # amount of clusters        
        if len(regions_off_shore_wind[-1])==0:
            regions_off_shore_wind = regions_off_shore_wind[:-1]
        else:
            current_amount_of_clusters += 1              

    # Sun: split clusters in off and on shore
    regions_off_shore_solar = list()
    current_amount_of_clusters = number_of_clusters

    for i in range(len(regions_solar)):

        # Create list in list of Off-shore clusters
        regions_off_shore_solar.append(list())

        # Check for every coordinate in the cluster if they are in the sea, if so --> take the coordinate
        # out of the current cluster and put it in a new cluster of off-shore locations of that cluster
        for number in regions_solar[i]:
            if not europe_land.contains(coordinates[number]):
                regions_solar[i] = regions_solar[i][regions_solar[i] != number]
                regions_off_shore_solar[-1].append(number)
                labels_solar[number] = current_amount_of_clusters
        
        # If no point of the cluster is in the sea, delete the empty list, else update the current 
        # amount of clusters
        if len(regions_off_shore_solar[-1])==0:
            regions_off_shore_solar = regions_off_shore_solar[:-1]    
        else:
            current_amount_of_clusters += 1   
              
    print("regions_wind",regions_wind)
    print("regions_off_shore_wind",regions_off_shore_wind)
    print("regions_solar",regions_solar)
    print("regions_off_shore_solar",regions_off_shore_solar)
    return(regions_wind, regions_off_shore_wind, labels_wind, regions_solar, regions_off_shore_solar, labels_solar)
