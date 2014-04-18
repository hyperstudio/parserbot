import os

CALAIS_API_KEY = "" # Add this
CALAIS_ENDPOINT = "http://api.opencalais.com/tag/rs/enrich"

FREEBASE_API_KEY = "" # Add this
FREEBASE_ENDPOINT = "https://www.googleapis.com/freebase/v1/mqlread"

ZEMANTA_API_KEY = "" # Add this
ZEMANTA_ENDPOINT = "http://api.zemanta.com/services/rest/0.0/"

STANFORD_NER_HOME = '/Applications/stanford_ner'
DEFAULT_CLASSIFIER = STANFORD_NER_HOME + '/classifiers/english.all.3class.distsim.crf.ser.gz'
STANFORD_JARFILE = os.path.join(STANFORD_NER_HOME, 'stanford-ner.jar')