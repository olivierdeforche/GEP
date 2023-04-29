import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

def Split_offshore_onshore(method, regions_wind, labels_wind, number_of_clusters_wind, regions_solar, labels_solar, number_of_clusters_solar, coordinates, lon, lat, plot, user, number_of_clusters, threshold, data, resize):

    # Load in polygon of Europe
    if user=='Olivier':
        europe_land = gpd.read_file("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/europe.geojson")
    else:
        europe_land = gpd.read_file("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Main Functions/europe.geojson")


    # Take out geometry out of Geoseries file
    europe_land = europe_land.geometry[0]

    # Wind: Split clusters in off and on shore
    regions_off_shore_wind = list()
    current_amount_of_clusters_wind = number_of_clusters_wind
    
    for i in range(len(regions_wind)):

        # Create list in list of Off-shore clusters
        regions_off_shore_wind.append(list())
        
        # Check for every coordinate in the cluster if they are in the sea, if so --> take the coordinate
        # out of the current cluster and put it in a new cluster of off-shore locations of that cluster
        for number in regions_wind[i]:
            if not europe_land.contains(coordinates[number]):
                regions_wind[i] = regions_wind[i][regions_wind[i] != number]
                regions_off_shore_wind[-1].append(number)
                labels_wind[number] = current_amount_of_clusters_wind
        
        # If no point of the cluster is in the sea, delete the empty list, else update the current 
        # amount of clusters        
        if len(regions_off_shore_wind[-1])==0:
            regions_off_shore_wind = regions_off_shore_wind[:-1]
        else:
            current_amount_of_clusters_wind += 1

    # Delete regions that are full in the sea
    to_remove_wind = list()
    for i in reversed(range(number_of_clusters_wind)):
        if len(regions_wind[i])==0:
            to_remove_wind.append(i)
            # regions_wind.pop(i)
            

    # Sun: split clusters in off and on shore
    regions_off_shore_solar = list()
    current_amount_of_clusters_solar = number_of_clusters_solar

    for i in range(len(regions_solar)):

        # Create list in list of Off-shore clusters
        regions_off_shore_solar.append(list())

        # Check for every coordinate in the cluster if they are in the sea, if so --> take the coordinate
        # out of the current cluster and put it in a new cluster of off-shore locations of that cluster
        for number in regions_solar[i]:
            if not europe_land.contains(coordinates[number]):
                regions_solar[i] = regions_solar[i][regions_solar[i] != number]
                regions_off_shore_solar[-1].append(number)
                labels_solar[number] = current_amount_of_clusters_solar
        
        # If no point of the cluster is in the sea, delete the empty list, else update the current 
        # amount of clusters
        if len(regions_off_shore_solar[-1])==0:
            regions_off_shore_solar = regions_off_shore_solar[:-1]    
        else:
            current_amount_of_clusters_solar += 1   

    # Delete regions that are full in the sea
    to_remove_solar = list()
    for i in reversed(range(number_of_clusters_solar)):
        if len(regions_solar[i])==0:
            to_remove_solar.append(i)
            regions_solar.pop(i)

    if user == 'Olivier':
        EEZ = gpd.read_file('C:/Users/defor/Desktop/Thesis/GEP/Clustering/Main Functions/EEZ_Europe_land.geojson')
    else:
        EEZ = gpd.read_file('C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Main Functions/EEZ_Europe_land.geojson')
    
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax1.scatter(lon, lat, c=labels_wind, alpha=0.5, s=100)
    EEZ.plot(edgecolor='k', facecolor=None, ax=ax1, alpha=0.5)

    ax2.scatter(lon, lat, c=labels_solar, alpha=0.5, s=100)
    EEZ.plot(edgecolor='k', facecolor=None, ax=ax2, alpha=0.5)

# kmeans, maxp, kmedoids, regional_kmeans, ward

    if user=="Olivier":
        if method=="kmeans":
            string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png')
            string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png')
        elif method=="maxp":
            string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/MaxP/")+str("MaxP")+str('_')+str(threshold)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png')
            string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/MaxP/")+str("MaxP")+str('_')+str(threshold)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png')
        elif method=="kmedoids":
            string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png')
            string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png')
        elif method=="regional_kmeans":
            string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png')
            string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png')
        elif method=="ward":
            string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png')
            string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png')
        elif method=="political_regions":
            string_wind = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("polytical_regions")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png')
            string_solar = str("C:/Users/defor/Desktop/Thesis/GEP/Clustering/Figures/Ward/")+str("polytical_regions")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png')
    else:
        if method=="kmeans":
            string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png') #@Louis
            string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmeans/")+str("Kmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png') #@Louis
        elif method=="maxp":
            string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/MaxP/")+str("MaxP")+str('_')+str(threshold)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png') #@Louis
            string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/MaxP/")+str("MaxP")+str('_')+str(threshold)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png') #@Louis
        elif method=="kmedoids":
            string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png') #@Louis
            string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Kmedoids/")+str("Kmedoids")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png') #@Louis
        elif method=="regional_kmeans":
            string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png') #@Louis
            string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/RegionalKmeans/")+str("RegionalKmeans")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png') #@Louis
        elif method=="ward":
            string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png') #@Louis
            string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/Ward/")+str("Ward")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png') #@Louis
        elif method=="political_regions":
            string_wind = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/PoliticalRegions/")+str("polytical_regions")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_wind_split_off_on.png')
            string_solar = str("C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Figures/PoliticalRegions/")+str("polytical_regions")+str('_')+str(number_of_clusters)+str('_')+str(data)+str('_')+str(resize)+str('_solar_split_off_on.png')
    
    fig1.savefig(string_wind, format='png')
    fig2.savefig(string_solar, format='png')

    return(regions_wind, regions_off_shore_wind, labels_wind, current_amount_of_clusters_wind, to_remove_wind, regions_solar, regions_off_shore_solar, labels_solar, current_amount_of_clusters_solar, to_remove_solar)
