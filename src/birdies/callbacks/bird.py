from dash import Input, Output, State, dcc, html
import pandas as pd
from functions import plot_density_map, get_image_url, get_code, get_name
from pathlib import Path
from .init_app import app

@app.callback(
    Output(f"header", "children"),
    Input(f"input", "data"),
)
def set(_input:dict):
    return _input['common_name']

@app.callback(
    Output('tabs-content', 'children'),
    Output("loading_output", "children"),
    Input('tabs', 'value'),
    Input("input", "data")
)
def set_main(tab, _input):
    if _input['code'] is not None:
        if tab == 'Map':
            df = pd.read_feather(Path(__file__).parent.parent/'data'/'nl_df.feather')
            df = df.set_index(['lat_km', 'lon_km'])
            df = df[df['COMMON NAME'] == _input['common_name']]

            div_content = [
                html.Div(children = [
                dcc.Graph(figure=plot_density_map(df), style={"width": "100%", "height": "100%"})
                ], style={'position':'absolute', "width": "100%", "bottom":"0", "height":"65%"})
            ]
            return div_content, True
        
        elif tab == 'Photo':
            div_content = [
                html.Img(src=get_image_url(_input['code']), style={"max-height": "65vh", "max-width": "100%"})
            ]
            return div_content, True
    else:
        return 'Error', True
    
@app.callback(
    Output("input", "data"),
    Input("search_button", "n_clicks"),
    State("search", 'value')
)
def search(_, bad_name):
    code = get_code(bad_name)
    common_name = get_name(code) if code is not None else "Cannot find bird..."
    _dict = {
        "common_name":common_name,
        "code":code
        }
    return _dict