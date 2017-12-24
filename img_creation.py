from PIL import Image, ImageDraw, ImageFont
import requests
import json

URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'

# Здесь, первый параметр это тип картинки, может быть:
# 1 (черно-белый), L (монохромный, оттенки серого),
# RGB, RGBA (RGB с альфа каналом), CMYK, YCbCr, I (32 bit Integer pixels),
# F (32 bit Float pixels).
img = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

rq = requests.get(URL).json()[0]
price_usd = rq['price_usd']
rank = rq['rank']
symbol = rq['symbol']
market_cap_usd = rq['market_cap_usd']
percent_change_1h = rq['percent_change_1h']
percent_change_24h = rq['percent_change_24h']
percent_change_7d = rq['percent_change_7d']


font = ImageFont.truetype("data/arial.ttf", 40)
draw.text((15, 10), fill=(0, 0, 0), text=symbol, font=font)

font = ImageFont.truetype("data/arial.ttf", 24)
draw.text((230, 15), fill=(0, 0, 0), text=price_usd, font=font)

font = ImageFont.truetype("data/arial.ttf", 24)
draw.text((2, 24), fill=(0, 0, 0), text=rank, font=font)

font = ImageFont.truetype("data/arial.ttf", 24)
draw.text((200, 40), fill=(0, 0, 0), text=percent_change_1h, font=font)

font = ImageFont.truetype("data/arial.ttf", 24)
draw.text((200, 60), fill=(0, 0, 0), text=percent_change_24h, font=font)

font = ImageFont.truetype("data/arial.ttf", 24)
draw.text((200, 80), fill=(0, 0, 0), text=percent_change_7d, font=font)

del draw
img.save("test.png", "PNG")
print(rq)

