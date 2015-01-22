import pytest

@pytest.fixture
def app():
	from parserbot.app import *
	return app

def test_app(app):
	assert app is not None
