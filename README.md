artx-ner
========

NER application for ArtX. Built on Flask.

Requires [virtualenv](http://www.virtualenv.org/en/latest/).

* `virtualenv .`
* `. bin/activate`
* `pip install -r requirements.txt`
* Set specific API keys either directly in `config.py` or in environment variables (e.g. Heroku config)
* `python run.py`

For use:

* `http://localhost:5000/stanford?payload=This+is+a+test+Pablo+Picasso`
* For long queries, also accepts data in a `POST` request