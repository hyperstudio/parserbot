import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Flask variables

DEBUG = os.environ.get('DEBUG') or True
JSON_AS_ASCII = False
SECRET_KEY = os.environ.get('PARSERBOT_SECRET_KEY')

# Resource-specific variables

_stanford_ner_basedir = os.path.join(_basedir, "parserbot", "stanford-ner")
STANFORD_JARFILE = os.path.join(_stanford_ner_basedir, "stanford-ner.jar")
STANFORD_DEFAULT_CLASSIFIER = os.path.join(_stanford_ner_basedir, "english.all.3class.distsim.crf.ser.gz")

CALAIS_API_KEY = os.environ.get('CALAIS_API_KEY')
CALAIS_ENDPOINT = 'http://api.opencalais.com/tag/rs/enrich'

FREEBASE_API_KEY = os.environ.get('FREEBASE_API_KEY') # add this
FREEBASE_ENDPOINT = "https://www.googleapis.com/freebase/v1/mqlread"

ZEMANTA_API_KEY = os.environ.get('ZEMANTA_API_KEY') # add this
ZEMANTA_ENDPOINT = 'http://api.zemanta.com/services/rest/0.0/'

PARSERBOT_USER_KEYS = os.environ.get('PARSERBOT_USER_KEYS')
