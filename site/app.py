# %%
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

from navbar import navbar
from callbacks import add_call_backs

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div([
    navbar,
    page_container
])
app = add_call_backs(app)

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
# %%
