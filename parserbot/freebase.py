import urllib
import json
import config

def mql(query):
    """
    Main mql query. Put in any valid kwargs and get response.
    """
    params = {
        "query": json.dumps(query),
        "key": config.FREEBASE_API_KEY
    }
    url = config.FREEBASE_ENDPOINT + "?" + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    return response