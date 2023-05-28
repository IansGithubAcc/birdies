# %%
import geopy.distance
import plotly.express as px
import pandas as pd
from pathlib import Path

def plot_density_map(df:'pd.DataFrame'):
    density_map_list = []
    for group, bird_size in zip(df.index.unique(), df.index.value_counts(sort=False)):
        lat, lon, _ = geopy.distance.distance(kilometers=group[1]).destination(geopy.distance.distance(kilometers=group[0]).destination((0, 0), bearing=0), bearing=90)
        density_map_list.append([lat, lon, bird_size])

    density_map_df = pd.DataFrame(density_map_list, columns=['Latitude', 'Longitude', 'Spots'])
    fig = px.density_mapbox(density_map_df, lat='Latitude', lon='Longitude', z='Spots', radius=50,
                            center=dict(lat=52.3, lon=5), zoom=6,
                            mapbox_style="stamen-terrain")
    fig.update_layout(
        margin=dict(l=0, t=2, r=0, b=0),
    )
    fig.update_coloraxes()
    return fig

# def plot_density_map(bird_df:'pd.DataFrame', df:'pd.DataFrame'):
#     density_map_list = []
#     for group, bird_size in zip(bird_df.index.unique(), bird_df.index.value_counts(sort=False)):
#         lat, lon, _ = geopy.distance.distance(kilometers=group[1]).destination(geopy.distance.distance(kilometers=group[0]).destination((0, 0), bearing=0), bearing=90)
#         df_dize = df.loc[group].shape[0]
#         density_map_list.append([lat, lon, bird_size/df_dize*100])

#     density_map_df = pd.DataFrame(density_map_list, columns=['Latitude', 'Longitude', 'Spot rate'])
#     fig = px.density_mapbox(density_map_df, lat='Latitude', lon='Longitude', z='Spot rate', radius=50,
#                             center=dict(lat=52.3, lon=5), zoom=6,
#                             mapbox_style="stamen-terrain")
#     fig.update_layout(
#         margin=dict(l=0, t=2, r=0, b=0),
#     )
#     fig.update_coloraxes(colorbar_ticksuffix='%')
#     return fig
