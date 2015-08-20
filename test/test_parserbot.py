import pytest
import hashlib
import json
from urllib2 import urlopen
from flask import url_for
import config
from parserbot import create_parser_app

headers = {'Authentication': hashlib.md5(config.SECRET_KEY).hexdigest()}
sample_payload = 'This is a test for Pablo Picasso.'

@pytest.fixture
def app():
	app = create_parser_app()
	return app

def post_request(endpoint, payload, client):
	data = {'payload': payload}
	res = client.post(url_for('.'+endpoint),
		data=json.dumps(data),
		headers=headers,
		content_type='application/json')
	return res

def test_app(app):
	"""App should exist."""
	assert app is not None

def test_debug(app):
	"""App should be in debug mode."""
	assert app.config['DEBUG'] is True

def test_no_auth(client):
	"""App should respond with 403 when no auth header is provided."""
	res = client.post(url_for('.run_stanford'))
	assert res.status_code == 403

def test_bad_auth(client):
	"""App should respond with 403 when bad auth is provided."""
	bad_headers = {'Authentication': 'Bad_token'}
	res = client.post(url_for('.run_stanford'), headers=bad_headers)
	assert res.status_code == 403

def test_no_data(client):
	"""App should respond with 422 when no data is provided."""
	res = client.post(url_for('.run_stanford'), headers=headers)
	assert res.status_code == 422

def test_bad_data(client):
	"""App should respond with 422 when bad data is provided."""
	bad_data = {'bad_key': 'No payload in this data.'}
	res = client.post(url_for('.run_stanford'), data=json.dumps(bad_data), headers=headers)
	assert res.status_code == 422

def test_bad_json_data(client):
	"""App should respond with 422 when the JSON data is invalid."""
	bad_json = {'payload': 'This will not be json encoded.'}
	res = client.post(url_for('.run_stanford'), data=bad_json, headers=headers)
	assert res.status_code == 422

# Endpoints

def test_hello_world(client):
	"""The hello world page should work and include a message."""
	res = client.get(url_for('.hello_world'))
	assert res.status_code == 200
	assert 'Hello world!' in res.json['message']

def test_stanford(client):
	"""The Stanford endpoint should respond with an entity."""
	res = post_request('run_stanford', sample_payload, client)
	assert res.status_code == 200
	assert res.json['message'] == 'Success'
	assert len(res.json['results']) == 1

def test_opencalais(client):
	"""The OpenCalais endpoint should respond with an entity."""
	res = post_request('run_calais', sample_payload, client)
	assert res.status_code == 200
	# Calais returns 8 results
	assert len(res.json['results']) == 8

def test_zemanta(client):
	"""The Zemanta endpoint should respond with an entity."""
	res = post_request('run_zemanta', sample_payload, client)
	assert res.status_code == 200
	assert len(res.json['results']) == 1

def test_dbpedia(client):
	"""The Dbpedia endpoint should respond with an entity."""
	res = post_request('run_dbpedia', sample_payload, client)
	assert res.status_code == 200
	assert len(res.json['results']) == 1

def test_no_entities_in_payload(client):
	"""The Stanford endpoint should not give an entity if there is not one in the payload."""
	res = post_request('run_stanford', 'No entities here', client)
	assert res.status_code == 200
	assert len(res.json['results']) == 0

# Live!

def test_server_is_running(live_server):
	res = urlopen(url_for('.hello_world', _external=True))
	assert res.getcode() == 200
	assert 'Hello world!' in json.loads(res.read())['message']
