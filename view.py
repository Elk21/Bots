import telebot
import mics


class View:
    tb = telebot.TeleBot(mics.token)
    tb.set_webhook(url=mics.webhook_url_path)

    def send(self, chat_id):
        with open('img/single_coin.png', 'rb') as photo:
            self.tb.send_photo(chat_id=chat_id, photo=photo)
