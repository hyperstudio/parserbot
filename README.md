artx-ner
========

Two apps for the price of one. Tools for the [ArtX](http://github.com/hyperstudio/artx) project. Built on [Flask](http://flask.pocoo.org/).

1. JSON endpoints for various text parsers, categorizers, and entity recognizers: [Stanford NER](http://nlp.stanford.edu/software/CRF-NER.shtml), [DBpedia](http://dbpedia.org), [OpenCalais](http://www.opencalais.com/), [Zemanta](http://www.zemanta.com/).
2. JSON scraper that extracts structured data from various museum websites.

### Setup

Requires [virtualenv](http://www.virtualenv.org/en/latest/). After cloning:

* `virtualenv .`
* `. bin/activate`
* `pip install -r requirements.txt`
* `python run.py`

**Note:** All resources require a valid API key, and some (e.g. OpenCalais) need additional API keys. Set all API keys in environment variables:

- `ARTX_USER_KEYS` is a comma-separated list of keys to serve as valid user API keys (we don't have a database, we're improvising here)
- `CALAIS_API_KEY` is an [OpenCalais API key](http://www.opencalais.com/APIkey) for all of the `/opencalais` endpoints.
- `ZEMANTA_API_KEY` is a [Zemanta API key](http://www.zemanta.com/developer/) for all of the `/zemanta` endpoints.
- `FREEBASE_API_KEY` is...not currently in use.

### Use

* Parser app: `/stanford?payload=This+is+a+test+Pablo+Picasso&key=My+API+Key` *(also accepts data in a `POST` request)*
* Scraper app: `/scrape/peabody?key=My+API+Key`
