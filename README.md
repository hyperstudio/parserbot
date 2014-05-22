artx-ner
========

NER application for ArtX. Built on Flask.

Requires [virtualenv](http://www.virtualenv.org/en/latest/).

* `virtualenv .`
* `. bin/activate`
* `pip install -r requirements.txt`
* `mv config.sample.py config.py`
* Open `config.py` and add specific API keys and paths.
* `python run.py`

For use:

* `http://localhost:5000/stanford?payload=This+is+a+test+Pablo+Picasso`
* For long queries, also accepts data in a `POST` request