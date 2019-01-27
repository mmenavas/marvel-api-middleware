import requests

import time
import hashlib


class Marvel:
    endpoint = 'https://gateway.marvel.com/v1/public/'

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def find_character(self, keyword=''):
        if not keyword:
            return []
        resource = 'characters'
        params = '?nameStartsWith={}&limit=10'.format(keyword)
        auth_params = self.get_auth_url_params()
        url = "{}{}{}{}".format(self.endpoint, resource, params, auth_params)
        return self.fetch_data(url)

    def get_auth_url_params(self):
        url_parameters = "";
        tokens = self.get_auth_tokens();
        for key, value in tokens.items():
            url_parameters = "{}&{}={}".format(url_parameters, key, value)

        return url_parameters

    def get_auth_tokens(self):
        timestamp = int(time.time())
        params = "{}{}{}".format(timestamp, self.private_key, self.public_key)
        api_hash = hashlib.md5()
        api_hash.update(params.encode('utf-8'))
        return {
            'apikey': self.public_key,
            'ts': timestamp,
            'hash': api_hash.hexdigest()
        }

    @staticmethod
    def fetch_data(url):
        # TODO: Add try/except for error handling
        r = requests.get(url=url)
        return r.json()
