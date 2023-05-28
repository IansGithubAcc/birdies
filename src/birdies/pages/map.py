from dash import html
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import dash

meta_tags = {
    "name":"viewport",
    "content":"width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=1.2, user-scalable=1.0"
}
dash.register_page(__name__, meta_tags=meta_tags)

layout = html.Div(children=[
    dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer")], id="map", style={'width': '100%', 'height':'70vh'}, center=(53, 4)),
    html.Div([
        html.Div([
        html.H1(id = 'coordinates', children='Select a location'),
        ], style={'float':'left', "max-width": "50%"}),
        html.Div([
        dbc.Button("Select location", id="location_button", color="primary", className="ms-2")
        ], style={'float':'right', "width": "50%"})
    ])
])
