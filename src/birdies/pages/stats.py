import json
from pathlib import Path

from dash import Dash, Input, Output, dash_table, dcc, html, register_page

meta_tags = {
    "name": "viewport",
    "content": "width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=1.2, user-scalable=1.0",
}
register_page(__name__, meta_tags=meta_tags)

path = Path(__file__).parent.parent / "data" / "locales_dict.txt"
with open(path) as file:
    locales_dict = json.load(file)

locales = list(locales_dict.keys())

layout = html.Div(
    [
        dcc.Location(id="recent_url_loc"),
        html.Div(id="stats-div")
    ]
)
