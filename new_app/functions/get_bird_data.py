import geopy.distance
import numpy as np
import pandas as pd

lat_to_km = lambda lat: round(geopy.distance.distance((lat, 0), (0, 0)).km, -1)
lon_to_km = lambda lat, lon: round(geopy.distance.distance((lat, lon), (lat, 0)).km, -1)

def get_bird_data(df, lat, lon, radius:int=5):
    data = []
    index_array = np.array(list(df.index.unique()), dtype=int)
    center_lat = lat_to_km(lat)
    center_lon = lon_to_km(lat, lon)
    diff = index_array - (center_lat, center_lon)
    r = np.sqrt(diff[:,0]**2 + diff[:,1]**2)
    for lat_m, lon_m in index_array[r<=radius]:
        data.append(df.loc[lat_m, lon_m])

    return pd.concat(data)
