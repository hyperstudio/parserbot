import requests

dbpedia_endpoint = "http://lookup.dbpedia.org/api/search.asmx/"
spotlight_endpoint = "http://spotlight.dbpedia.org/rest/"

def annotate(payload):
    url = spotlight_endpoint + "annotate"
    headers = {
        "accept": "application/json"
    }
    params = {
        "text": payload,
        "confidence": 0.3
    }
    r = requests.get(url, params=params, headers=headers)
    return r.json()

def get_entities(payload):
    results = annotate(payload)
    return [resource['@URI'] for resource in results['Resources']]

def keyword_search(keyword):
    url = dbpedia_endpoint + "KeywordSearch"
    headers = {
        "accept": "application/json"
    }
    params = {
        "QueryClass": "",
        "QueryString": keyword
    }
    r = requests.get(url, params=params, headers=headers)
    return r.json()

def prefix_search(prefix):
    url = dbpedia_endpoint + "PrefixSearch"
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