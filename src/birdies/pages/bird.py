from dash import html, dcc
import dash

meta_tags = {
    "name":"viewport",
    "content":"width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=1.2, user-scalable=1.0"
}
dash.register_page(__name__, meta_tags=meta_tags)

layout = html.Div(children=[
    dcc.Location(id='bird_url_loc'),
    dcc.Store(id='input', data={"common_name":"European Robin"}),
    html.H1(id='header', children='No bird chosen', style={'zIndex':1}),

    dcc.Tabs(id="tabs", value='Photo', style={'zIndex':1}, children=[
        dcc.Tab(label='Photo', value='Photo'),
        dcc.Tab(label='Map', value='Map'),
    ]),
    html.Div(id='tabs-outer', children= [
        dcc.Loading(id="loading", children=[html.Div(id="loading_output")], type="circle", style={'zIndex':2, 'position':'absolute', 'bottom':'0', 'height':'25vh'}),
        html.Div(id='tabs-content', style={"text-align": "center"})
    ])
])

