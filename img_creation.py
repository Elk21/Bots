from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import telebot

coins = ['ripple', 'bitcoin', 'cardano', 'iota', 'litecoin', 'bitcoin-cash', 'ethereum']
font = 'RML.ttf'
width = 300
height = 150


def draw_text(d, pos, color=(0, 0, 0, 255), text='', size=16):
    fnt = ImageFont.truetype("fonts/" + font, size)
    d.text(pos, fill=color, text=text, font=fnt)


def get_html(url):
    r = requests.get(url)
    return r.text


# Get graph image of price change in last 7 days
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
        return str(round(float(x) / 1000000000, 3)) + ' M'


def create_single_coin_img(coin='bitcoin'):
    # Здесь, первый параметр это тип картинки, может быть:
    # 1 (черно-белый), L (монохромный, оттенки серого),
    # RGB, RGBA (RGB с альфа каналом), CMYK, YCbCr, I (32 bit Integer pixels),
    # F (32 bit Float pixels).
    img = Image.new("RGBA", (width, height), (240, 240, 240, 255))
    draw = ImageDraw.Draw(img)

    url = 'https://api.coinmarketcap.com/v1/ticker/' + coin + '/'
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

    dx = 2
    dy = 2
    s_font = 16
    m_font = 22
    l_font = 34

    # Graph
    img_rq = requests.get(get_image(_id))
    graph = Image.open(BytesIO(img_rq.content)).convert('RGBA')
    img.paste(graph, (width - graph.width - 2, 10), graph)

    # Coin icon
    icon = Image.new("RGBA", (l_font, l_font), (0, 0, 0, 255))
    img.paste(icon,
              (width - graph.width + 5 * dx, height - (l_font + dy)),
              icon)

    # Symbol
    draw_text(draw,
              pos=(width - graph.width + l_font + 6 * dx, height - (l_font + dy)),
              text=symbol,
              size=l_font)

    # Price USD
    draw_text(draw,
              pos=(6, height / 8),
              text=price_usd + '$',
              size=m_font)

    # Price change
    draw_text(draw,
              pos=(6, height / 2 - s_font - dy),
              text='1H  ' + percent_change_1h + '%',
              color=get_color(percent_change_1h),
              size=s_font)
    draw_text(draw,
              pos=(6, height / 2),
              text='1D  ' + percent_change_24h + '%',
              color=get_color(percent_change_24h),
              size=s_font)
    draw_text(draw,
              pos=(6, height / 2 + s_font + dy),
              text='7D  ' + percent_change_7d + '%',
              color=get_color(percent_change_7d),
              size=s_font)

    # Price volume
    draw_text(draw,
              pos=(6, height - (s_font * 2 + dy)),
              text='MC  ' + convert_big_value(market_cap_usd) + '$',
              size=s_font)
    draw_text(draw,
              pos=(6, height - (s_font + dy)),
              text='VOL ' + convert_big_value(volume_usd_24h) + '$',
              size=s_font)
    del draw
    img.save('img/' + coin + '.png', "PNG")
    return img


#
#
#
#
#
#
#
#
#
#

bot = telebot.TeleBot('488210005:AAFtVtoY4lk4_ZmXGAScM-xeMxyL_J6TDMo')


# @bot.message_handler(commands=['music'])
# def find_file_ids(message):
#     for file in os.listdir('music/'):
#         if file.split('.')[-1] == 'ogg':
#             f = open('music/' + file, 'rb')
#             msg = bot.send_voice(message.chat.id, f, None)
#             # А теперь отправим вслед за файлом его file_id
#             bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)
#         time.sleep(3)


@bot.message_handler(content_types=['text'])
def answer(message):
    in_coin = message.text
    if in_coin in coins:
        create_single_coin_img(in_coin)
        with open('img/' + in_coin + '.png', 'rb') as photo:
            # Create button
            keyboard = telebot.types.InlineKeyboardMarkup()
            url_button = telebot.types.InlineKeyboardButton(text="to CoinMarketCap",
                                                            url='https://coinmarketcap.com/currencies/' + in_coin + '/')
            keyboard.add(url_button)
            # Send photo with reply markup
            bot.send_photo(message.chat.id, photo=photo, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'no such crypto')


def main():
    create_single_coin_img('iota')
    for c in coins:
        create_single_coin_img(c)


if __name__ == '__main__':
    bot.polling(none_stop=True)
