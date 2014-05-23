import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
JSON_AS_ASCII = False

STANFORD_BASE = os.path.join(_basedir, "stanford-ner")
STANFORD_JARFILE = os.path.join(STANFORD_BASE, "stanford-ner.jar")
STANFORD_DEFAULT_CLASSIFIER = os.path.join(STANFORD_BASE, "english.all.3class.distsim.crf.ser.gz")

CALAIS_API_KEY = os.environ.get('CALAIS_API_KEY') # add this
CALAIS_ENDPOINT = 'http://api.opencalais.com/tag/rs/enrich'

FREEBASE_API_KEY = os.environ.get('FREEBASE_API_KEY') # add this
FREEBASE_ENDPOINT = "https://www.googleapis.com/freebase/v1/mqlread"

ZEMANTA_API_KEY = os.environ.get('ZEMANTA_API_KEY') # add this
ZEMANTA_ENDPOINT = 'http://api.zemanta.com/services/rest/0.0/'
