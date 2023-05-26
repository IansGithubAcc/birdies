# %%
import pandas as pd
import geopy.distance
from typing import List
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'browser'

lat_to_km = lambda lat: round(geopy.distance.distance((lat, 0), (0, 0)).km, -1)
lon_to_km = lambda lat, lon: round(geopy.distance.distance((lat, lon), (lat, 0)).km, -1)

# %% Load original data 

path = 'ebd_NL_relMar-2023/ebd_NL_relMar-2023.txt'
df = pd.read_csv(path, delimiter='\t')#, chunksize=10000).get_chunk(10000)

# %% Make groups (Takes long) and save
df['lat_km'] = df['LATITUDE'].apply(lat_to_km)
df['lon_km'] = df.apply(lambda df: lon_to_km(df['LATITUDE'], df['LONGITUDE']), axis=1)
df = df.set_index(['lat_km', 'lon_km'])
df = df.sort_index()
df = df.reset_index()
df.to_feather('nl_df.feather')

# %% load groups from file
df = pd.read_feather('nl_df.feather')
df = df.set_index(['lat_km', 'lon_km'])

# %%
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
# %% local spot rate
local_df = get_bird_data(df, 50.755002, 6.020325)
local_df['COMMON NAME'].value_counts()/local_df.shape[0]

# %% Bird spot Density map NL
def density_map(df):
    density_map_list = []
    for group, size in zip(df.index.unique(), df.index.value_counts(sort=False)):
        lat, lon, _ = geopy.distance.distance(kilometers=group[1]).destination(geopy.distance.distance(kilometers=group[0]).destination((0, 0), bearing=0), bearing=90)
        density_map_list.append([lat, lon, size])

    density_map_df = pd.DataFrame(density_map_list, columns=['Latitude', 'Longitude', 'spots'])
    fig = px.density_mapbox(density_map_df, lat='Latitude', lon='Longitude', z='spots', radius=50,
                            center=dict(lat=52.3, lon=5), zoom=6,
                            mapbox_style="stamen-terrain", hover_name="spots", hover_data=['Latitude', 'Longitude'])
    fig.show()

# %% Pie chart
def pie_chart(df, min_spots=0):
    count = df['COMMON NAME'].value_counts()
    plot_df = pd.DataFrame({'COMMON NAME':count.keys(), 'count':count.values})
    plot_df.loc[plot_df['count'] < min_spots, 'COMMON NAME'] = 'Other birdies'
    fig = px.pie(plot_df, values='count', names='COMMON NAME', title='Birds spotted in NL')
    fig.update_traces(textposition='inside', textinfo='label')
    return fig

# %% barplot
def bar_plot(df, min_spots=0, orientation='h'):
    count = df['COMMON NAME'].value_counts()
    plot_df = pd.DataFrame({'COMMON NAME':count.keys(), 'count':count.values})
    plot_df = plot_df[plot_df['count'] >= min_spots]
    # if orientation == 'h':
    #     x = "count"
    #     y = "COMMON NAME"
    #     plot_df = plot_df.iloc[::-1]
    # else:
    #     x = "COMMON NAME"
    #     y = "count"

    # fig = px.bar(plot_df, x=x, y=y, orientation=orientation)

    if orientation == 'h':
        plot_df = plot_df.iloc[::-1]
        x = plot_df["count"]
        y = plot_df["COMMON NAME"]
    else:
        x = plot_df["COMMON NAME"]
        y = plot_df["count"]

    fig = go.Figure(go.Bar(
                x=x,
                y=y,
                orientation='h'))

    return fig

# %%
from dash import Dash, html, dcc, Output, Input, dash_table
import json

api_key='tkm5gu05mifl'
app = Dash(__name__)

with open('locales_dict.txt') as file:
    locales_dict = json.load(file)

locales = list(locales_dict.keys())

# fig = bar_plot(get_bird_data(groups, 52.124653, 4.643599, 5), orientation='h')
# fig.layout

app.layout = html.Div([
    dcc.Geolocation(id="geolocation"),
    html.Div([
        html.Div([
            html.Div([
                dcc.Input(id="latitude", placeholder="Latitude", type="number", style={'width': '97%'}),
                dcc.Input(id="longitude", placeholder="Longitude", type="number", style={'width': '97%'}),
            ], style={'float':'left', 'width': '50%'}),
            html.Button("My location", id="update_btn", style={'float':'right', 'width':'50%', 'height':'42.67px'}),
        ], style={'width': '50%', 'float': 'left'}),
        html.Div([
            dcc.Dropdown(locales, id='locales', value='English', style={"width": "100%"}),
        ], style={"width": "50%", 'float': 'right'})
    ], style={"width": "100%", 'float': 'left'}),


    dcc.Graph(figure=fig)

])

# set location
@app.callback(
    Output('latitude', 'value'),
    Output('longitude', 'value'),
    Output("geolocation", "update_now"),
    Input("geolocation", "position"),
    Input("update_btn", "n_clicks")
)
def set_location(loc, n_clicks):
    update_now = True if n_clicks and n_clicks > 0 else False
    if loc is not None:
        return loc['lat'], loc['lon'], update_now
    else:
        return '', '', update_now

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
# %%
