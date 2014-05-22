import requests
import config

class CalaisAPI(object):

   def __init__(self):
       self.api_key = config.CALAIS_API_KEY
       self.endpoint = config.CALAIS_ENDPOINT

   def call(self, payload, id_str=None):
       headers = {
           'x-calais-licenseID': '%s' % self.api_key,
           'content-type': 'text/raw',
           'accept': 'application/json',
           'enableMetadataType': "SocialTags",
           'calculateRelevanceScore': "true",
           'externalID': "artx-%s" % id_str,
           }
       r = requests.post(self.endpoint, data=payload, headers=headers)
       try: result = r.json()
       except JSONDecodeError: result = None
       return result

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
            'entity_type': entity_type
            })
    return sorted(finals, key=lambda x: x['score'], reverse=True)