# %%
from dash import Dash, html, dcc, Output, Input, dash_table
from ebird.api import get_nearby_observations
from collections import Counter
import requests
from bs4 import BeautifulSoup

api_key='tkm5gu05mifl'

app = Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='Photo', children=[
        dcc.Tab(label='Photo', value='Photo'),
        dcc.Tab(label='Details', value='Details'),
    ]),
    dcc.Geolocation(id="geolocation"),
    dcc.Store(id='records', storage_type='local'),
    dcc.RadioItems(['Latest', 'Popularity'], 'Latest', id = 'radio', inline=True),
    dcc.Input(id="latitude", placeholder="Latitude", type="number"),
    dcc.Input(id="longitude", placeholder="Longitude", type="number"),
    html.Button("My location", id="update_btn"),
    dcc.Dropdown([], id='dropdown'),
    html.Div(id='tabs-outer', children= [
        dcc.Loading(id="loading", children=[html.Div(id="loading_output")], type="circle"),
        html.Div(id='tabs-content', style={"text-align": "center"})
    ]),
    html.Button(html.H4('<'), style={'width':"50%", 'display': 'inline-block'}, id='previous'),
    html.Button(html.H4('>'), style={'width':"50%", 'display': 'inline-block'}, id='next')
])

# set location
@app.callback(
    Output('latitude', 'value'),
    Output('longitude', 'value'),
    Output("geolocation", "update_now"),
    Input("geolocation", "position"),
    Input("update_btn", "n_clicks")
)
def set_location(loc, n_clicks):
    update_now = True if n_clicks and n_clicks > 0 else False
    if loc is not None:
        return loc['lat'], loc['lon'], update_now
    else:
        return '', '', update_now

# Get birds and set dropdown
@app.callback(
    Output("dropdown", "options"),
    Output("dropdown", "value"),
    Output("records", 'data'),
    Input("latitude", "value"),
    Input("longitude", "value"),
    Input('radio', 'value'),
    Input("next", 'n_clicks'),
    Input("previous", 'n_clicks')
)
def set_bird_data(lat, lon, sort, next_clicks, previous_clicks):
    if lat != '' and lon != '':
        records = get_nearby_observations(api_key, lat, lon, dist=10, back=30)
        if sort == 'Popularity':
            pop_birds = Counter([record['comName'] for record in records]).most_common()
            birds_dd = [f'{amount}: {bird}' for (bird, amount) in pop_birds]

        else:
            birds_dd = [f'{record["obsDt"]}: {record["comName"]}' for record in records]

        next_clicks = 0 if next_clicks is None else next_clicks
        previous_clicks = 0 if previous_clicks is None else previous_clicks
        default = birds_dd[max(0, 0+next_clicks-previous_clicks)] if len(birds_dd)>0 else None
        return birds_dd, default, records
    
    else:
        return [], None, []

# Set bird: Resets the clicks when selecting a bird
@app.callback(
    Output('tabs-content', 'n_clicks'),
    Input('dropdown', 'value'),
)
def set_bird(bird_entry):
    if bird_entry != None:
        return 0
    
    else:
        return 0

# set main content
@app.callback(
    Output("loading_output", "children"), 
    Output('tabs-content', 'children'),
    Input('dropdown', 'value'),
    Input('records', 'data'),
    Input('tabs-content', 'n_clicks'),
    Input('tabs', 'value')
)
def set_main(bird_entry, bird_dicts, n_clicks, tabs):
    if bird_dicts != [] and bird_entry is not None:
        bird_name = bird_entry.split(': ')[1]
        bird_names = [bird_dict['comName'] for bird_dict in bird_dicts]
        bird_dict = bird_dicts[bird_names.index(bird_name)]
        if tabs == 'Photo':
            host = 'archive'
            if host == 'archive':
                from urllib.request import urlopen
                textpage = urlopen(f"http://web.archive.org/cdx/search/cdx?url=https://ebird.org/species/{bird_dict['speciesCode']}&output=txt")
                text = str(textpage.read(), 'utf-8')
                datetimestr = text.split(' ')[1]
                url = f"http://web.archive.org/web/{datetimestr}/https://ebird.org/species/{bird_dict['speciesCode']}/"
            
            elif host == 'google':
                url = f'http://webcache.googleusercontent.com/search?q=cache:https%3A%2F%2Febird.org%2Fspecies%2F{bird_dict["speciesCode"]}'

            else:
                url = f"https://ebird.org/species/{bird_dict['speciesCode']}"

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            img_tags = soup.find_all('img')
            n_clicks = 0 if n_clicks is None else n_clicks%(max(1, len(img_tags)-2))
            if len(img_tags) > 0:
                img_url = img_tags[n_clicks]['src']
                return True, html.Div(children=[html.Img(src=img_url, style={"max-height": "70vh", "max-width": "100%"})])
            else:
                return True, html.Div(children='No image url found')
        else:
            return  True, html.Div(children=dash_table.DataTable([{'key':key,'value':value} for key, value in bird_dict.items()], [{"name": i, "id": i} for i in ['key', 'value']]))
    else:
        return True, []

if __name__ == '__main__':
    app.run_server()
