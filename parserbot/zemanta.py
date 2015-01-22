import requests
import urllib
import config

class ZemantaAPI(object):
    """ For high-level access to the Zemanta API. """

    def __init__(self, api_key=config.ZEMANTA_API_KEY, endpoint=config.ZEMANTA_ENDPOINT):
        self.API_KEY = api_key
        self.ENDPOINT = endpoint
        self.session = requests.Session()

    def _access_api(self, params):
        if not 'api_key' in params.keys():
            params['api_key'] = self.API_KEY
        if not 'format' in params.keys():
            params['format'] = 'json'
        endpoint = "%s?%s" % (self.ENDPOINT, urllib.urlencode(params))
        r = self.session.get(endpoint, timeout=8, allow_redirects=True)
        return r.json()

    def suggest(self, text, **kwargs):
        params = {
            'method': 'zemanta.suggest',
            'text': text.encode('utf-8')
        }
        for k, v in kwargs.items():
            if isinstance(v, basestring):
                v = v.encode('utf-8')
            elif isinstance(v, bool):
                v = int(v)
            params[k] = v
        return self._access_api(params)

    def suggest_markup(self, text, emphasis=None, return_rdf_links=False, markup_limit=None):
        params = {
            'method': 'zemanta.suggest_markup',
            'text': text.encode('utf-8')}
        if emphasis:
            params['emphasis'] = emphasis
        if return_rdf_links:
            params['return_rdf_links'] = '1'
        if markup_limit:
            params['markup_limit'] = markup_limit
        return self._access_api(params)

    def preferences(self):
        params = {'method': 'zemanta.preferences'}
        return self._access_api(params)

    def entity_query(self, payload):
        """ Takes a text string as payload and returns any Zemanta markup entities found. """
        results = self.suggest_markup(payload, return_rdf_links=True)
        entities = []
        for link in results['markup']['links']:
            entity = {
                'entity_type': link['entity_type'][0] if link['entity_type'] else '',
                'targets': ', '.join([target['url'] for target in link['target']]),
                'relevance': link['relevance'],
                'confidence': link['confidence'],
                'anchor': link['anchor']
            }
            entities.append(entity)
        return entities
