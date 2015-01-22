Parserbot
=========

Parserbot wants to be your one-stop shop for natural language parsing, tagging, and entity extraction. It wraps a variety of services and APIs into one app for easy parsing and cross-reference. Currently:

- [Stanford NER](http://nlp.stanford.edu/software/CRF-NER.shtml)
- [DBpedia](http://dbpedia.org)
- [OpenCalais](http://www.opencalais.com/)
- [Zemanta](http://www.zemanta.com/)
- roughly, [Freebase](http://www.freebase.com/)

Built for the [Artbot](http://github.com/hyperstudio/artbot-api) project on [Flask](http://flask.pocoo.org/).

### Setup

Best to do this in a [virtualenv](http://www.virtualenv.org/en/latest/), or even better, a [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/). After setting up and activating the virtualenv:

* `pip install .`
* `python run.py`

**Note:** All resources require a valid secret key, and some (e.g. OpenCalais) need additional API keys. Set all API keys in environment variables:

- `PARSERBOT_SECRET_KEY` is the app's secret key, which you need to generate and hash in order to get your "authentication token"
- `CALAIS_API_KEY` is an [OpenCalais API key](http://www.opencalais.com/APIkey) for all of the `/opencalais` endpoints.
- `ZEMANTA_API_KEY` is a [Zemanta API key](http://www.zemanta.com/developer/) for all of the `/zemanta` endpoints.
- `FREEBASE_API_KEY` is...not currently in use.

### Use

Python example:

	headers = {'Authentication': '<YOUR_TOKEN_HERE>', 'Content-Type': 'application/json'}
	data = json.dumps({'payload': 'This is a test for a man named Pablo Picasso, have you heard of him?'})
	r = requests.post("http://127.0.0.1:5000/stanford", data=data, headers=headers)

### Future

Parsers to add:

* [Getty Vocabularies](http://www.getty.edu/research/tools/vocabularies/) (especially [Union List of Artist Names](http://www.getty.edu/research/tools/vocabularies/ulan/index.html))
* [OpenNLP](https://opennlp.apache.org/)
* [AlchemyAPI](http://www.alchemyapi.com/)
* [Diffbot](http://www.diffbot.com/)
* [CLAVIN](http://clavin.bericotechnologies.com/)
