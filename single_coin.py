from PIL import Image, ImageDraw
import requests
from io import BytesIO
from config import get_color, get_image, convert_big_value, draw_text, shit_to_name, get_icon


class SingleCoin:
    width = 300
    height = 150
    dx = 2
    dy = 2
    s_font = 16
    m_font = 22
    l_font = 34
    img_url = ''

    def create_image(self, coin):
        coin = shit_to_name(coin)
        if coin:

            img = Image.new("RGBA", (self.width, self.height), (240, 240, 240, 255))
            draw = ImageDraw.Draw(img)

            url = 'https://api.coinmarketcap.com/v1/ticker/' + coin + '/'
            rq = requests.get(url).json()[0]
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
            img.paste(graph, (self.width - graph.width - 2, 20), graph)


            # Name
            name = _id[0].capitalize() + _id[1:]
            draw_text(draw=draw,
                      pos=(self.width - graph.width + self.l_font + 9 * self.dx,
                           self.height - (self.l_font + self.dy) - self.s_font),
                      text=name,
                      size=self.s_font)

            # Coin icon
            icon_rq = requests.get(get_icon(_id))
            icon = Image.open(BytesIO(icon_rq.content)).convert('RGBA')
            img.paste(icon,
                      (self.width - graph.width + 8 * self.dx, self.height - (self.l_font + self.dy)),
                      icon)

            # Symbol
            draw_text(draw=draw,
                      pos=(self.width - graph.width + self.l_font + 8 * self.dx,
                           self.height - (self.l_font + self.dy)),
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

            self.img_url = 'img/single_coin.png'
            img.save(self.img_url, "PNG")
            return self.img_url
        else:
            print('Wrong input.\nPlz try again')

    def get_path(self):
        return self.img_url

