"""TODO: fix next and prev button -> make them update and index. Let this index select the DD value. """
from dash import Dash, html, dcc, Output, Input, dash_table, register_page
from ebird.api import get_nearby_observations
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import dash

meta_tags = {
    "name":"viewport",
    "content":"width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=1.2, user-scalable=1.0"
}
dash.register_page(__name__, meta_tags=meta_tags)

path = Path(__file__).parent.parent/ 'data' / 'locales_dict.txt'
with open(path) as file:
    locales_dict = json.load(file)

locales = list(locales_dict.keys())

layout = html.Div([
    dcc.Location(id='loc'),
    dcc.Tabs(id="tabs", value='Photo', children=[
        dcc.Tab(label='Photo', value='Photo'),
        dcc.Tab(label='Details', value='Details'),
    ]),
    dcc.Geolocation(id="geolocation"),
    dcc.Store(id='records', storage_type='local'),
    
    dcc.Dropdown([], id='dropdown', style={'float':'left', "width": "100%"}),
    html.Div(id='tabs-outer', children= [
        dcc.Loading(id="loading", children=[html.Div(id="recent_loading_output")], type="circle"),
        html.Div(id='recent-tabs-content', style={"text-align": "center"})
    ]),

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

    html.Button(html.H4('<'), style={'width':"50%", 'display': 'inline-block'}, id='previous'),
    html.Button(html.H4('>'), style={'width':"50%", 'display': 'inline-block'}, id='next')
])

