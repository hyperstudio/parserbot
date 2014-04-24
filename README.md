artx-ner
========

NER application for ArtX. Built on Flask.

Requires [virtualenv](http://www.virtualenv.org/en/latest/).

* `virtualenv .`
* `. bin/activate`
* `pip install -r requirements.txt`
* `mv settings.sample.py settings.py`
* Open `settings.py` and add specific API keys and paths.

For use:

* `http://localhost:5000/stanford?payload=This+is+a+test+Pablo+Picasso`
* For long queries, also accepts data in a `POST` request