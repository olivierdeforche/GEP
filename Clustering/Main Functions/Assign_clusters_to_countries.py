import geopandas
import atlite
import numpy as np
import geopandas as gpd
import pandas as pd
import tabulate


def Asign_clusters_to_countries(labels_wind, labels_solar, plot, user):
    if user =="Olivier":
        EZZ = geopandas.read_file('C:/Users/defor/Desktop/Thesis/Data/EEZ_Land_v3_202030.shp')
        EZZ.to_file('C:/Users/defor/Desktop/Thesis/Data/EEZ_Land_v3_202030.geojson', driver='GeoJSON')
        cutout = atlite.Cutout("C:/Users/defor/Desktop/Thesis/Data/europe-2013-era5.nc")
    else:
        shp_file = geopandas.read_file('"C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/EEZ_Land_v3_202030.shp')
        shp_file.to_file('C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/EEZ_Land_v3_202030.geojson', driver='GeoJSON')
        cutout = atlite.Cutout("C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/europe-2013-era5.nc")

    # Get the x and y coordinates from the cutout object as numpy arrays
    x = cutout.coords['x'].values
    y = cutout.coords['y'].values

    # Use np.meshgrid to create a grid of x and y coordinates
    xx, yy = np.meshgrid(x, y)

    # Use np.ravel to flatten the grid arrays into one-dimensional arrays
    xx = xx.ravel()
    yy = yy.ravel()

    # Use pd.DataFrame to create a pandas dataframe with columns for x, y and capacity
    df = pd.DataFrame({'x': xx, 'y': yy, 'capacity': 1})

    # Create a column with the combined xy coordinate to be the future column name for the results
    df['XY'] = df['x'].astype(str).str.cat(df['y'].astype(str), sep=',')

    # Turn this into a GeoDataFrame, like a pandas dataframe but with a geography attribute
    sites = gpd.GeoDataFrame(df)

    # Set the XY column as the index
    sites = gpd.GeoDataFrame(sites).set_index('XY')

    # Create dictionary to convert to an excel later
    dict_solar = {}
    dict_wind = {}


    for country_name in EZZ:
        dict_solar[country_name] = None
        dict_wind[country_name] = None

    for label in labels_wind:
        size = label.length()
        for point in label:
            for country_name in EZZ:
                country_polygon = country_name.polygon()
                if country_polygon.contains_point(point):
                    dict_wind[country_name] = 
                    

 

    df_solar = pd.DataFrame(data=dict_solar, index=[0])
    df_wind = pd.DataFrame(data=dict_wind, index=[0])

    df_solar = (df_solar.T)
    df_wind = (df_wind.T)

    if plot:
        print(df_solar, df_wind)

    df_solar.to_excel('df_solar.xlsx')
    df_wind.to_excel('df_wind.xlsx')

    return()