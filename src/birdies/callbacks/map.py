from dash import Input, Output, State, dcc, html
from .init_app import app
import dash_leaflet as dl

@app.callback(
    Output("layer", "children"),
    Output("coordinates", "children"),
    Output("location_button", "href"),
    Input("map", "click_lat_lng"),
    prevent_initial_call=True
    )
def map_click(click_lat_lng):
    marker = [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]
    lat, lon = click_lat_lng
    return marker, f'Lat:{round(lat, 3)}, Lon:{round(lon, 3)}', f'recent/#{lat}_{lon}'