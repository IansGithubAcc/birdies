# %%
from dash import html, page_container
from navbar import navbar

from callbacks import app

app.layout = html.Div([
    navbar,
    page_container
])

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)

# %%
