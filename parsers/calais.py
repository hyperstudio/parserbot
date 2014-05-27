import requests
import config
import uuid

class CalaisAPI(object):

   def __init__(self, api_key=None, endpoint=None):
       self.api_key = api_key or config.CALAIS_API_KEY
       self.endpoint = endpoint or config.CALAIS_ENDPOINT

   def call(self, payload, id_str=None):
       if not id_str:
           id_str = str(uuid.uuid4())
       headers = {
           'x-calais-licenseID': '%s' % self.api_key,
           'content-type': 'text/raw',
           'accept': 'application/json',
           'enableMetadataType': "SocialTags",
           'calculateRelevanceScore': "true",
           'externalID': "artx-%s" % id_str,
           }
       r = requests.post(self.endpoint, data=payload, headers=headers)
       return r.json()

def entity_call(payload, id_str=None):
    results = CalaisAPI().call(payload, id_str)
    finals = []
    for key, entity in results.iteritems():
        try:
            typeGroup = entity["_typeGroup"]
        except KeyError:
            continue
        if typeGroup == "socialTag":
            name = entity["name"]
            calais_id = entity["socialTag"]
            score = 0.8 if int(entity["importance"]) > 1 else 0.6
            entity_type = ""
        elif typeGroup == "topics":
            name = entity["categoryName"]
            calais_id = entity["category"]
            score = float(entity["score"]) if "score" in entity else 0.0
            entity_type = ""
        elif typeGroup == "entities":
            name = entity["name"]
            calais_id = key
            score = float(entity["relevance"])
            entity_type = entity.get("_type", "")
        finals.append({
            'name': name,
            'calais_id': calais_id,
            'score': score,
            'entity_type': entity_type,
            'type_group': typeGroup
            })
    return sorted(finals, key=lambda x: x['score'], reverse=True)