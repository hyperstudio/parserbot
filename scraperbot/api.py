"""
This module wraps the various parsers into a Flask request/response pattern.
This includes authorization, validation, and response handling features.

.. note:: **All functions** within this module require **two things**:

    - An ``Authorization`` header that is a md5 hash of your application's secret key.
    - ``POST`` request data that has a ``payload`` key.

"""

from flask import current_app, Blueprint, jsonify, request, abort
import hashlib

bp = Blueprint('parserbot', __name__)


def _authorized():
    """
    Checks to see if the Authorization header is a hash of this application's
    secret key.
    """
    valid_auth = current_app.config['SCRAPERBOT_SECRET_KEY']
    return request.args.get('key') == valid_auth


def _respond(results):
    """
    Generates JSON response with provided results.

    :param results: List of items returned by a given scraper.
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


@bp.route('/<path:path>')
def scrape(path):
    if not _authorized():
        abort(403)
    try:
        scraper_module = __import__('scraperbot', globals(), locals(),
            [str(path)], -1)
        path_module = getattr(scraper_module, path)
    except ImportError:
        abort(404)
    results = path_module.scrape()
    return _respond(results)
