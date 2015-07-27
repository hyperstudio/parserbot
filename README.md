Parserbot
=========

Parserbot is your one-stop shop for natural language parsing, tagging, and entity extraction. It wraps a variety of services and APIs into one app for easy parsing and cross-reference. Currently:

- [Stanford NER](http://nlp.stanford.edu/software/CRF-NER.shtml)
- [DBpedia](http://dbpedia.org)
- [OpenCalais](http://www.opencalais.com/)
- [Zemanta](http://www.zemanta.com/)
- roughly, [Freebase](http://www.freebase.com/)

Built for the [Artbot](http://github.com/hyperstudio/artbot-api) project on [Flask](http://flask.pocoo.org/).

### Setup

Tested with Python 2.7.x. Setup within a [virtualenv](http://www.virtualenv.org/en/latest/) is recommended, or even better, a [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/). After cloning the repo and activating the virtualenv:

* `pip install .`
* run `python key.py`. It will spit out a secret key and auth header token; save these in environment variables (e.g. a shell profile, `.env` file, etc.). This is a convenience function that you can run as many times as you like.
* `python run.py` to start the server
* navigate to (http://localhost:3000) and you should see a welcome message

**NOTE:** All services require a `PARSERBOT_SECRET_KEY` environment variable.

Setting up specific NLP services:

#### Stanford NER -- `/stanford`

* you must have [Java](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) of some flavor installed
* `pip install nltk==3.0.1`

#### OpenCalais -- `/opencalais`

* get an [OpenCalais API key](http://www.opencalais.com/APIkey) and set as a `CALAIS_API_KEY` environment variable

#### Zemanta -- `/zemanta`

* get a [Zemanta API key](http://www.zemanta.com/developer/) and set as a `ZEMANTA_API_KEY` environment variable

#### Freebase

* not currently configured. If you set it up, let us know!

### Use

Python example:

	headers = {'Authentication': '<YOUR_TOKEN_HERE>', 'Content-Type': 'application/json'}
	data = json.dumps({'payload': 'This is a test for a man named Pablo Picasso'})
	r = requests.post('http://127.0.0.1:5000/stanford', data=data, headers=headers)

### Tests

Tests are built for local setup only for now:

* `pip install pytest pytest-flask`
* `python setup.py test`

### Documentation

You can find the docs in the `docs/` subfolder. To generate new docs:

* `pip install sphinx`
* `sphinx-build docs/source docs/`

### Deployment

Currently set up to deploy on Heroku; configure the environment variables you need and it should be good to go.

### Future

Parsers to add someday:

* [Getty Vocabularies](http://www.getty.edu/research/tools/vocabularies/) (especially [Union List of Artist Names](http://www.getty.edu/research/tools/vocabularies/ulan/index.html))
* [OpenNLP](https://opennlp.apache.org/)
* [AlchemyAPI](http://www.alchemyapi.com/)
* [Diffbot](http://www.diffbot.com/)
* [CLAVIN](http://clavin.bericotechnologies.com/)

### License

Copyright (C) 2015 Massachusetts Institute of Technology

This program is free software; you can redistribute it and/or modify
it under the terms of version 2 of the GNU General Public License as
published by the Free Software Foundation (http://opensource.org/licenses/GPL-2.0).
