from dash import Dash
import dash_bootstrap_components as dbc
from pathlib import Path

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    pages_folder=str(Path(__file__).parents[1] / "pages"),
)
