from dash import html
import dash

meta_tags = {
    "name":"viewport",
    "content":"width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=1.2, user-scalable=1.0"
}
dash.register_page(__name__, path='/', meta_tags=meta_tags)

layout = html.Div(children=[
    html.H1(children='Welcome!'),

    html.Div([
        dash.dcc.Link('Map', href='map'),
    ]),
    html.Div([
        dash.dcc.Link('Recent spots', href='recent'),
    ]),
    html.Div([
        dash.dcc.Link('Bird', href='bird'),
    ]),
])
