import telebot
import mics


class View:
    tb = telebot.TeleBot(mics.token)
    tb.remove_webhook()
    tb.set_webhook(url=mics.webhook_url_path)

    def __init__(self, chat_id=''):
        self.chat_id = chat_id

    def send_message(self, text):
        self.tb.send_message(chat_id=self.chat_id, text=text)

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def send_buttons(self):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Top 10 🔝', 'BTC 📈')
        markup.row('ETH 📈', 'XRP 📈', 'BCH 📈')
        markup.row('LTC 📈', 'ADA 📈', 'MIOTA 📈')
        self.tb.send_message(self.chat_id, "Press button or enter yours:", reply_markup=markup)

    def send_image(self, filename):
        with open('img/' + filename + '.png', 'rb') as image:
            self.tb.send_photo(chat_id=self.chat_id, photo=image)

