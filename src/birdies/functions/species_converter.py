# %%
import pandas as pd
from pathlib import Path

def get_code(name:str):
    if type(name) == str:
        name = name.lower()
        df = pd.read_csv(Path(__file__).parent.parent/'data'/'ebird_taxonomy_v2022.csv')
        df['PRIMARY_COM_NAME'] = df['PRIMARY_COM_NAME'].apply(lambda x:x.lower())
        _dict = dict(zip(df['PRIMARY_COM_NAME'], df['SPECIES_CODE']))
        if name in _dict:
            return _dict[name] 

def get_name(code:str):
    if type(code) == str:
        df = pd.read_csv(Path(__file__).parent.parent/'data'/'ebird_taxonomy_v2022.csv')
        _dict = dict(zip(df['SPECIES_CODE'], df['PRIMARY_COM_NAME']))
        if code in _dict:
            return _dict[code]