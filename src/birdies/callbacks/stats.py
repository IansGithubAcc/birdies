from .init_app import app
from dash import Output, Input, no_update


# set location
@app.callback(
    Output("stats-div", "children"),
    Input("recent_url_loc", "hash"),
)
def set_location(url_loc):
    if (
        not isinstance(url_loc, str)
        or url_loc == ""
        or url_loc[0] != "#"
        or len(url_loc[1:].split("_")) != 2
    ):
        return no_update

    lat, lon = url_loc[1:].split("_")
    return f"{round(float(lat), 3)}, {round(float(lon), 3)}"
