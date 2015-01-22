import requests

DBPEDIA_ENDPOINT = "http://lookup.dbpedia.org/api/search.asmx/"
SPOTLIGHT_ENDPOINT = "http://spotlight.dbpedia.org/rest/"

class DbpediaAPI(object):

    def spotlight_annotate(self, payload):
        url = SPOTLIGHT_ENDPOINT + "annotate"
        headers = {
            "accept": "application/json"
        }
        params = {
            "text": payload,
            "confidence": 0.3
        }
        r = requests.get(url, params=params, headers=headers)
        return r.json()

    def get_entities(self, payload):
        results = self.spotlight_annotate(payload)
        return [resource['@URI'] for resource in results['Resources']]

    def keyword_search(self, keyword):
        url = DBPEDIA_ENDPOINT + "KeywordSearch"
        headers = {
            "accept": "application/json"
        }
        params = {
            "QueryClass": "",
            "QueryString": keyword
        }
        r = requests.get(url, params=params, headers=headers)
        return r.json()

    def prefix_search(self, prefix):
        url = DBPEDIA_ENDPOINT + "PrefixSearch"
        headers = {
            "accept": "application/json"
        }
        params = {
            "QueryClass": "",
            "QueryString": prefix,
            "MaxHits": 5
        }
        r = requests.get(url, params=params, headers=headers)
        return r.json()