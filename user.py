import hashlib
import datetime
import random
from config import PARSERBOT_USER_KEYS

class User(object):

    def __init__(self, api_key):
        assert PARSERBOT_USER_KEYS is not None, 'No API keys configured'
        assert api_key in PARSERBOT_USER_KEYS, 'Invalid API key'
        self.api_keys = api_key

    @staticmethod
    def generate_api_key(self):
        return hashlib.md5(datetime.datetime.utcnow().strftime(
            '%Y %M %d %H:%M:%S' + 10*str(random.randint(0,9)))).hexdigest()