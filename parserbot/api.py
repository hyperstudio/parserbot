"""
This module wraps the various parsers into a Flask request/response pattern.
This includes authorization, validation, and response handling features.

.. note:: **All functions** within this module require **two things**:

    - An ``Authorization`` header that is a md5 hash of your application's secret key.
    - ``POST`` request data that has a ``payload`` key.

"""

from flask import current_app, Blueprint, jsonify, request, abort
from parserbot import calais, dbpedia, stanford, zemanta
import hashlib

bp = Blueprint('parserbot', __name__)


def _authorized():
    """
    Checks to see if the Authorization header is a hash of this application's secret key.
    """
    return request.headers.get('Authorization') == hashlib.md5(current_app.config['SECRET_KEY']).hexdigest()


def _valid_request():
    """
    Checks to see if the request has a JSON payload with `payload` argument.
    """
    if request.json is None or request.json.get('payload') is None:
        return False
    return True


def _handle(func):
    """
    Checks authorization and validity of request, and runs `func` on the request payload.

    :param func: Function to run using the request payload as an argument.
    :type func: function
    """
    if not _authorized():
        abort(403)
    elif not _valid_request():
        abort(422)
    payload = request.json.get('payload')
    return func(payload)


def _respond(results):
    """
    Generates JSON response with provided results.

    :param results: List of items returned by a given parser.
    :type results: list of dictionaries
    """
    message = {
        'status': 200,
        'message': 'Success',
        'count': len(results),
        'results': results
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@bp.route('/', methods=['GET'])
def hello_world():
    """
    Used for the ``/`` endpoint. No authorization or payload needed; used for testing purposes.

    :return: JSON response object with status and message.
    """
    message = {
        'status': 200,
        'message': 'Hello world! Find me on github at https://github.com/hyperstudio/parserbot'
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@bp.route('/opencalais', methods=['POST'])
def run_calais():
    """
    Used for the ``/opencalais`` endpoint. Calls :py:meth:`parserbot.calais.CalaisAPI.extract_entities`.

    :return: JSON response object with matching entities.
    """
    results = _handle(calais.CalaisAPI().extract_entities)
    return _respond(results)


@bp.route('/zemanta', methods=['POST'])
def run_zemanta():
    """
    Used for the ``/zemanta`` endpoint. Calls :py:meth:`parserbot.zemanta.ZemantaAPI.extract_entities`.

    :return: JSON response object with matching entities.
    """
    results = _handle(zemanta.ZemantaAPI().extract_entities)
    return _respond(results)


@bp.route('/stanford', methods=['POST'])
def run_stanford():
    """
    Used for the ``/stanford`` endpoint. Runs methods in two stages:

    - Calls :py:meth:`parserbot.stanford.StanfordNER.extract_entities` and dedupes the results
    - Runs the results through :py:meth:`dbpedia.DbpediaAPI.wikify_stanford` to link the entities to Wikipedia

    :return: JSON response object with matching entities.
    """
    stanford_results = _handle(stanford.StanfordNER().extract_entities)
    # dedupe the lists so that we aren't calling dbpedia repeatedly
    stanford_results = dict((key, list(set(value))) for key, value in stanford_results.items())
    # now get dbpedia URLs for them
    dbp_results = dbpedia.DbpediaAPI().wikify_stanford(stanford_results)
    return _respond(dbp_results)


@bp.route('/dbpedia', methods=['POST'])
def run_dbpedia():
    """
    Used for the ``/dbpedia`` endpoint. Calls :py:meth:`parserbot.dbpedia.DbpediaAPI.get_entities`

    :return: JSON response object with matching entities.
    """
    results = _handle(dbpedia.DbpediaAPI().extract_entities)
    return _respond(results)
