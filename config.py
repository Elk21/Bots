import json
from PIL import ImageFont
import requests
from bs4 import BeautifulSoup


def get_image(name):
    url = 'https://coinmarketcap.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    image = soup.find('a', text=name).parent.parent.find('img').attrs['src']
    return image


def get_icon(name):
    r = requests.get('https://coinmarketcap.com/currencies/' + name + '/')
    soup = BeautifulSoup(r.text, 'lxml')
    icon = soup.find('h1').find('img').get('src')
    return icon


def get_html(url):
    r = requests.get(url)
    return r.text


def get_color(x):
    if float(x) >= 0:
        return 0, 200, 0
    else:
        return 220, 0, 0


def convert_big_value(x):
    ret = ''
    if float(x) >= 1000000:
        ret = str(round(float(x) / 1000000000, 3)) + ' M'
    dx = 9 - len(ret)
    for i in range(dx):
        ret = ' ' + ret
    return ret


def draw_text(draw, pos, color=(0, 0, 0, 255), text='', size=16, font='RML.ttf'):
    fnt = ImageFont.truetype("fonts/" + font, size)
    draw.text(pos, fill=color, text=text, font=fnt)


def shit_to_name(x):
    x = x.lower()
    file = json.load(open('data/coin_names.json'))

    for i in range(1, len(file)):
        if x in file[str(i)]:
            return file[str(i)][1]
    else:
        return None


def get_top10():
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=10'
    rq = requests.get(url).json()
    names = []
    for e in rq:
        names.append(str(e['id']))
    return names


def add_space(x):
    if float(x) >= 0:
        return ' ' + str(x)
    else:
        return x
