import urllib
import json
import settings

def mql(query):
    """ Main mql query. Put in any valid kwargs and get response. """
    params = {
        "query": json.dumps(query),
        "key": settings.FREEBASE_API_KEY
    }
    url = settings.FREEBASE_ENDPOINT + "?" + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    return response