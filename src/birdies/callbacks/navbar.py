from dash import Output, Input, State
from .init_app import app
# we use a callback to toggle the collapse on small screens

@app.callback(
    Output(f"logo-navbar-collapse", "is_open"),
    [Input(f"logo-navbar-toggler", "n_clicks")],
    [State(f"logo-navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open