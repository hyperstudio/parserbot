artx-ner
========

Two apps for the price of one. Tools for the [ArtX](http://github.com/hyperstudio/artx) project. Built on [Flask](http://flask.pocoo.org/).

1. Live parsing (named entity recognition and categorization) of text using various web resources (Stanford NER, DBpedia, OpenCalais, Zemanta).
2. Dynamic scraping of relevant event information from museum websites.

### Setup

Requires [virtualenv](http://www.virtualenv.org/en/latest/). After cloning:

* `virtualenv .`
* `. bin/activate`
* `pip install -r requirements.txt`
* `python run.py`

### Use

* Parser app: `/stanford?payload=This+is+a+test+Pablo+Picasso` *(also accepts data in a `POST` request)*
* Scraper app: `/scrape/peabody`

* * *

*To connect to some resources (e.g. OpenCalais), you need an API key. Set this in an environment variable (e.g. `export` or `heroku config CALAIS_API_KEY={your-key}`. See `config.py` for all the options.*