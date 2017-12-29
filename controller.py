from flask import Flask
from flask import request
from flask import jsonify
from view import View
from model import Model
import mics
from flask_sslify import SSLify


app = Flask(__name__)
model = Model()
view = View()


@app.route('/', methods=['GET'])
def default_answer():
    return '<h1>Bot working</h1>'


@app.route('/' + mics.token + '/', methods=['POST'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        model.set_message(message)
        image_type = model.get_image()
        view.set_chat_id(chat_id)
        view.send_buttons()
        view.send_image(image_type)

        return jsonify(r)


if __name__ == '__main__':
    app.run()
