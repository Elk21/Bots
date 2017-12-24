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

rq = requests.get(URL).json()
price_usd = rq[0]['price_usd']
font = ImageFont.truetype("data/arial.ttf", 40)
draw.text((10, 10), fill=(0, 0, 0), text=price_usd, font=font)

del draw
img.save("test.png", "PNG")
print(rq[0])