from flask import (Flask, jsonify)
from flask_cors import CORS

from marvel import marvel

import os
import signal


app = Flask(__name__)

signal.signal(signal.SIGINT, lambda s, f: os._exit(0))

cors = CORS(app, resources={
    r"/find/*": {"origins": "http://localhost:3000"}
})

public_key = os.getenv('MARVEL_PUBLIC_KEY', '')
private_key = os.getenv('MARVEL_PRIVATE_KEY', '')
marvel_api = marvel.Marvel(public_key, private_key)


@app.route('/find')
@app.route('/find/')
@app.route('/find/<name>')
def find_character(name=""):
    response = marvel_api.find_character(name)
    if not response:
        return jsonify([])

    results = response['data']['results']
    characters = []
    thumbnail_format = 'standard_medium'
    image_format = 'standard_amazing'

    for result in results:
        image = result['thumbnail']
        if image['path'].find('image_not_available') == -1:
            character = {
                "id": result['id'],
                "name": result['name'],
                "thumbnail": "{}/{}.{}".format(image['path'], thumbnail_format, image['extension']),
                "image": "{}/{}.{}".format(image['path'], image_format, image['extension'])
            }
            characters.append(character)

    return jsonify(characters)


app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

