from single_coin import SingleCoin


class Model:
    single_coin = SingleCoin()

    def __init__(self):
        self.message = ''

    def set_message(self, message):
        self.message = message

    def get_image(self):
        self.single_coin.create_image(self.message)
