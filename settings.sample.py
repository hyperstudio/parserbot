import os

BASE = os.path.abspath(os.path.dirname(__name__))

STANFORD_BASE = os.path.join(BASE, "stanford-ner")
STANFORD_JARFILE = os.path.join(STANFORD_BASE, "stanford-ner.jar")
STANFORD_DEFAULT_CLASSIFIER = os.path.join(STANFORD_BASE, "english.all.3class.distsim.crf.ser.gz")

CALAIS_API_KEY = "" # Add this
CALAIS_ENDPOINT = "http://api.opencalais.com/tag/rs/enrich"

FREEBASE_API_KEY = "" # Add this
FREEBASE_ENDPOINT = "https://www.googleapis.com/freebase/v1/mqlread"

ZEMANTA_API_KEY = "" # Add this
ZEMANTA_ENDPOINT = "http://api.zemanta.com/services/rest/0.0/"