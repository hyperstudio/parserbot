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

* `python setup.py install`
* the install script will spit out a `PARSERBOT_SECRET_KEY` variable and authentication header token. Save these in environment variables (e.g. a shell profile, `.env` file, etc.)
* `python run.py`
* navigate to (http://localhost:3000) and you should see a welcome message

**Note:** All resources require a valid secret key, and some (e.g. OpenCalais) need additional API keys. Set all API keys in environment variables:

- `PARSERBOT_SECRET_KEY` is the app's secret key, used for permissions. A hash of this key must go in the header of every request.
- `CALAIS_API_KEY` is an [OpenCalais API key](http://www.opencalais.com/APIkey) for the `/opencalais` endpoint.
- `ZEMANTA_API_KEY` is a [Zemanta API key](http://www.zemanta.com/developer/) for the `/zemanta` endpoint.
- `FREEBASE_API_KEY` is...not currently in use.

### Use

Python example:

	headers = {'Authentication': '<YOUR_TOKEN_HERE>', 'Content-Type': 'application/json'}
	data = json.dumps({'payload': 'This is a test for a man named Pablo Picasso'})
	r = requests.post("http://127.0.0.1:5000/stanford", data=data, headers=headers)

Tests (runs on [pytest-flask](https://github.com/vitalk/pytest-flask/)):

	python setup.py test

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
