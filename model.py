from single_coin import SingleCoin
from top10 import Top10


class Model:
    single_coin = SingleCoin()
    top10 = Top10()

    def __init__(self):
        self.message = ''

    def set_message(self, message):
        self.message = message

    def get_image(self):
        msg = self.message

        if msg == 'Top 10 🔝':
            self.top10.create_image()
            return 'top'
        if '📈' in msg:
            msg = msg[:-2]
            self.single_coin.create_image(msg)
            return 'single_coin'
        else:
            self.single_coin.create_image(msg)
            return 'single_coin'
