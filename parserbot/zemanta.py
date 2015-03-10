import requests
import urllib
import config

class ZemantaAPI(object):
    """
    Interacts with the `Zemanta API <http://zemanta.github.io/zemapi-java/>`_.

    :param api_key: Zemanta API key. Defaults to the ``ZEMANTA_API_KEY`` config variable.
    :param endpoint: Zemanta endpoint URL. Defaults to the ``ZEMANTA_ENDPOINT`` config variable.
    :type api_key: string
    :type endpoint: string
    """

    def __init__(self, api_key=None, endpoint=None):
        self.API_KEY = api_key or config.ZEMANTA_API_KEY
        self.ENDPOINT = endpoint or config.ZEMANTA_ENDPOINT
        self.session = requests.Session()

    def _access_api(self, params):
        """
        Low-level request to the Zemanta API with given request params.

        :param params: Preferences and filters for the Zemanta API
        :type params: dict
        :return: Dict of Zemanta entities.
        """
        if not 'api_key' in params.keys():
            params['api_key'] = self.API_KEY
        if not 'format' in params.keys():
            params['format'] = 'json'
        endpoint = "%s?%s" % (self.ENDPOINT, urllib.urlencode(params))
        r = self.session.get(endpoint, timeout=8, allow_redirects=True)
        return r.json()

    def suggest(self, text, **kwargs):
        """
        Calls the Zemanta API's ``suggest`` endpoint with arbitrary keyword arguments.

        :param text: Payload natural language fulltext.
        :type text: string
        :return: Dictionary of Zemanta entities.
        """
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
        """
        Calls the Zemanta API's ``suggest_markup`` endpoint.

        :param text: Payload in natural language fulltext.
        :param emphasis: Highlight matching words (defaults to False)
        :param return_rdf_links: Include linked data URIs for each entity (defaults to True)
        :param markup_limit: Set ``markup_limit`` (defaults to None)
        :type text: string
        :type emphasis: bool
        :type return_rdf_links: bool
        :type markup_limit: bool
        :return: Dictionary of Zemanta entities
        """
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
        """
        Gets your current Zemanta user preferences and status.

        :return: Dictionary of preferences.
        """
        params = {'method': 'zemanta.preferences'}
        return self._access_api(params)

    def extract_entities(self, payload):
        """
        Takes a text string as payload and returns any Zemanta markup entities found.

        First calls :py:meth:`parserbot.zemanta.ZemantaAPI.suggest_markup`, then formats the results for storage.

        :param payload: Fulltext natural language payload.
        :type payload: string
        :return: List of Zemanta entities.
        """
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
