import json

from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
from io import BytesIO


def get_image(name):
    url = 'https://coinmarketcap.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    image = soup.find('a', text=name).parent.parent.find('img').attrs['src']
    return image


def get_html(url):
    r = requests.get(url)
    return r.text


def get_color(x):
    if float(x) >= 0:
        return 0, 200, 0
    else:
        return 220, 0, 0


def convert_big_value(x):
    if float(x) >= 1000000:
        return str(round(float(x) / 1000000000, 3)) + ' M'


def draw_text(self, draw, pos, color=(0, 0, 0, 255), text='', size=16):
    fnt = ImageFont.truetype("fonts/" + self.font, size)
    draw.text(pos, fill=color, text=text, font=fnt)


def shit_to_name(x):
    x = x.lower()
    file = json.load(open('data/coin_names.json'))

    for i in range(1, len(file)):
        print(file[str(i)])
        if x in file[str(i)]:
            return file[str(i)][1]
    else:
        return None


class SingleCoin:
    coins = ['ripple', 'bitcoin', 'cardano', 'iota', 'litecoin', 'bitcoin-cash', 'ethereum']
    font = 'RML.ttf'
    width = 300
    height = 150
    dx = 2
    dy = 2
    s_font = 16
    m_font = 22
    l_font = 34
    img_url = ''

    def __init__(self, coin):
        self.coin = shit_to_name(coin)
        self.draw()

    def draw(self):
        # Здесь, первый параметр это тип картинки, может быть:
        # 1 (черно-белый), L (монохромный, оттенки серого),
        # RGB, RGBA (RGB с альфа каналом), CMYK, YCbCr, I (32 bit Integer pixels),
        # F (32 bit Float pixels).
        img = Image.new("RGBA", (self.width, self.height), (240, 240, 240, 255))
        draw = ImageDraw.Draw(img)

        url = 'https://api.coinmarketcap.com/v1/ticker/' + self.coin + '/'
        rq = requests.get(url).json()[0]
        print(rq)
        _id = rq['name']
        price_usd = rq['price_usd']
        symbol = rq['symbol']
        market_cap_usd = rq['market_cap_usd']
        volume_usd_24h = rq['24h_volume_usd']
        percent_change_1h = rq['percent_change_1h']
        percent_change_24h = rq['percent_change_24h']
        percent_change_7d = rq['percent_change_7d']

        # Graph
        img_rq = requests.get(get_image(_id))
        graph = Image.open(BytesIO(img_rq.content)).convert('RGBA')
        img.paste(graph, (self.width - graph.width - 2, 10), graph)

        # Coin icon
        icon = Image.new("RGBA", (self.l_font, self.l_font), (0, 0, 0, 255))
        img.paste(icon,
                  (self.width - graph.width + 5 * self.dx, self.height - (self.l_font + self.dy)),
                  icon)

        # Symbol
        draw_text(draw,
                  pos=(
                      self.width - graph.width + self.l_font + 6 * self.dx, self.height - (self.l_font + self.dy)),
                  text=symbol,
                  size=self.l_font)

        # Price USD
        draw_text(draw=draw,
                  pos=(6, self.height / 8),
                  text=price_usd + '$',
                  size=self.m_font)

        # Price change
        draw_text(draw=draw,
                  pos=(6, self.height / 2 - self.s_font - self.dy),
                  text='1H  ' + percent_change_1h + '%',
                  color=get_color(percent_change_1h),
                  size=self.s_font)
        draw_text(draw=draw,
                  pos=(6, self.height / 2),
                  text='1D  ' + percent_change_24h + '%',
                  color=get_color(percent_change_24h),
                  size=self.s_font)
        draw_text(draw=draw,
                  pos=(6, self.height / 2 + self.s_font + self.dy),
                  text='7D  ' + percent_change_7d + '%',
                  color=get_color(percent_change_7d),
                  size=self.s_font)

        # Price volume
        draw_text(draw=draw,
                  pos=(6, self.height - (self.s_font * 2 + self.dy)),
                  text='MC  ' + convert_big_value(market_cap_usd) + '$',
                  size=self.s_font)
        draw_text(draw=draw,
                  pos=(6, self.height - (self.s_font + self.dy)),
                  text='VOL ' + convert_big_value(volume_usd_24h) + '$',
                  size=self.s_font)
        del draw
        self.img_url = 'img/' + self.coin + '.png'
        img.save(self.img_url, "PNG")

    def get_url(self):
        return self.img_url
