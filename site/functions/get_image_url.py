import requests
from bs4 import BeautifulSoup

def get_image_url(speciescode, host:str = 'archive'):
    """ chose host from 'archive'|'google'|None """
    if host == 'archive':
        from urllib.request import urlopen
        textpage = urlopen(f"http://web.archive.org/cdx/search/cdx?url=https://ebird.org/species/{speciescode}&output=txt")
        text = str(textpage.read(), 'utf-8')
        datetimestr = text.split(' ')[1]
        url = f"http://web.archive.org/web/{datetimestr}/https://ebird.org/species/{speciescode}/"
    
    elif host == 'google':
        url = f'http://webcache.googleusercontent.com/search?q=cache:https%3A%2F%2Febird.org%2Fspecies%2F{speciescode}'

    else:
        url = f"https://ebird.org/species/{speciescode}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    if len(img_tags) > 0:
        img_url = img_tags[0]['src']

        return img_url