from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
from io import BytesIO

coin = 'bitcoin'
URL = 'https://api.coinmarketcap.com/v1/ticker/' + coin + '/'
width = 320
height = 120


def draw_text(d, pos, color=(0, 0, 0, 255), text='', size=16):
    fnt = ImageFont.truetype("data/HLR.TTF", size)
    d.text(pos, fill=color, text=text, font=fnt)


def get_html(url):
    r = requests.get(url)
    return r.text


def get_image(name):
    url = 'https://coinmarketcap.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    image = soup.find('a', text=name).parent.parent.find('img').attrs['src']
    return image


def get_color(x):
    if float(x) >= 0:
        return 0, 200, 0
    else:
        return 220, 0, 0


def convert_big_value(x):
    if float(x) >= 1000000:
        y = int(float(x) / 1000000)
        return str(round(float(x) / 1000000000, 3)) + ' M'


def main():
    # Здесь, первый параметр это тип картинки, может быть:
    # 1 (черно-белый), L (монохромный, оттенки серого),
    # RGB, RGBA (RGB с альфа каналом), CMYK, YCbCr, I (32 bit Integer pixels),
    # F (32 bit Float pixels).
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    rq = requests.get(URL).json()[0]
    _id = rq['id'][0].title() + rq['id'][1:]
    price_usd = rq['price_usd']
    rank = rq['rank']
    symbol = rq['symbol']
    market_cap_usd = rq['market_cap_usd']
    volume_usd_24h = rq['24h_volume_usd']
    percent_change_1h = rq['percent_change_1h']
    percent_change_24h = rq['percent_change_24h']
    percent_change_7d = rq['percent_change_7d']

    img_rq = requests.get(get_image(_id))
    graph = Image.open(BytesIO(img_rq.content)).convert('RGBA')
    dx = height / 6

    img.paste(graph, (width - graph.width - 2, 10), graph)

    draw_text(draw, (width / 2 + 10, height - 50), text=symbol, size=50)
    draw_text(draw, (width / 2 + 10, height - 19), text=rank)

    draw_text(draw, (2, dx * 0), text=price_usd + '$', size=18)
    draw_text(draw, (2, dx * 1), text='1H    ' + percent_change_1h + '%', color=get_color(percent_change_1h))
    draw_text(draw, (2, dx * 2), text='1D    ' + percent_change_24h + '%', color=get_color(percent_change_24h))
    draw_text(draw, (2, dx * 3), text='7D    ' + percent_change_7d + '%', color=get_color(percent_change_7d))
    draw_text(draw, (2, dx * 4), text='MC    ' + convert_big_value(market_cap_usd) + '$')
    draw_text(draw, (2, dx * 5), text='VOL   ' + convert_big_value(volume_usd_24h) + '$')
    del draw
    img.save('img/' + coin + '.png', "PNG")
    print(rq)


if __name__ == '__main__':
    main()
