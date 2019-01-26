from flask import (Flask, jsonify)
from flask_cors import CORS

import random
import string

app = Flask(__name__)
cors = CORS(app, resources={r"/items": {"origins": "http://localhost:3000"}})


@app.route('/items')
def get_items():
    # Generate values for cards
    count = 8
    alphabet = list(string.ascii_uppercase)
    items = alphabet[0:count]
    items += items
    random.shuffle(items)

    return jsonify(items)


app.run(debug=True, port=8000, host='127.0.0.1')
