from dash import html, Output, Input, dash_table
from ebird.api import get_nearby_observations
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from .init_app import app

api_key='tkm5gu05mifl'

path = Path(__file__).parent.parent/ 'data' / 'locales_dict.txt'
with open(path) as file:
    locales_dict = json.load(file)

locales = list(locales_dict.keys())

# set location
@app.callback(
    Output('latitude', 'value'),
    Output('longitude', 'value'),
    Output("geolocation", "update_now"),
    Input("geolocation", "position"),
    Input("update_btn", "n_clicks"),
    Input('recent_url_loc', 'hash'),
)
def set_location(loc, n_clicks, url_loc):
    if n_clicks is not None and n_clicks > 0:
        update_now = True if n_clicks and n_clicks > 0 else False
        if loc is not None:
            return loc['lat'], loc['lon'], update_now
        
    elif url_loc != '' and url_loc[0] == '#' and len(url_loc[1:].split('_'))==2:
            lat, lon = url_loc[1:].split('_')
            return round(float(lat),3), round(float(lon),3), False

    else:
        return '', '', False

# Get birds and set dropdown
@app.callback(
    Output("dropdown", "options"),
    Output("dropdown", "value"),
    Output("records", 'data'),
    Input("latitude", "value"),
    Input("longitude", "value"),
    Input("next", 'n_clicks'),
    Input("previous", 'n_clicks'),
    Input("locales", "value"),
)
def set_bird_data(lat, lon, next_clicks, previous_clicks, locale):
    if lat != '' and lon != '':
        records = get_nearby_observations(api_key, lat, lon, dist=10, back=30, locale=locales_dict[locale])
        birds_dd = [f'{record["obsDt"]}: {record["comName"]}' for record in records]
        next_clicks = 0 if next_clicks is None else next_clicks
        previous_clicks = 0 if previous_clicks is None else previous_clicks
        default = birds_dd[max(0, 0+next_clicks-previous_clicks)] if len(birds_dd)>0 else None
        return birds_dd, default, records
    
    else:
        return [], None, []

# Resets the clicks when selecting a bird
@app.callback(
    Output('recent-tabs-content', 'n_clicks'),
    Input('dropdown', 'value'),
)
def set_bird(bird_entry):
    if bird_entry != None:
        return 0
    
    else:
        return 0

# set main content
@app.callback(
    Output("recent_loading_output", "children"), 
    Output('recent-tabs-content', 'children', allow_duplicate=True),
    Output('go_to_bird', 'href'),
    Input('dropdown', 'value'),
    Input('records', 'data'),
    Input('recent-tabs-content', 'n_clicks'),
    Input('tabs', 'value'), 
    prevent_initial_call=True
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
                return True, html.Div(children=[html.Img(src=img_url, style={"max-height": "65vh", "max-width": "100%"})]), f"/bird#{bird_dict['speciesCode']}"
            else:
                return True, html.Div(children='No image url found'), f"/bird#{bird_dict['speciesCode']}"
        else:
            return  True, html.Div(children=dash_table.DataTable([{'key':key,'value':value} for key, value in bird_dict.items()], [{"name": i, "id": i} for i in ['key', 'value']])), f"/bird#{bird_dict['speciesCode']}"
    else:
        return True, [], ''