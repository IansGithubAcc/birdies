from dash import Dash
from .navbar import add_nav_bar
from .bird import add_bird, add_tabs, add_search
def add_call_backs(app:Dash):
    app.config['suppress_callback_exceptions'] = True
    app = add_nav_bar(app)
    app = add_bird(app)
    app = add_search(app)
    app = add_tabs(app)

    return app