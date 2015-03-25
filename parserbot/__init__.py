"""
This is the top-level module for parserbot. App-wide functions and error handlers.
"""
from flask import Flask, jsonify


def create_parser_app(settings_override=None):
    """
    Create a parserbot app with overrideable default settings.

    :param settings_override: custom Flask settings to override the defaults
    :type settings_override: dictionary
    :return: Flask app object
    """
    app = Flask(__name__)
    app.config.from_object('config')
    if settings_override is not None:
        app.config.update(**settings_override)

    from parserbot.api import bp
    app.register_blueprint(bp)

    # Set up error handlers here because Flask doesn't let you do the 500 error in the blueprint
    # https://github.com/mitsuhiko/flask/blob/5b9826615267fd75a954db40c1decc2a9dc40a99/flask/app.py#L1140
    app.errorhandler(500)(_on_500)
    app.errorhandler(404)(_on_404)
    app.errorhandler(403)(_on_403)
    app.errorhandler(422)(_on_422)
    
    return app


def _on_500(error=None):
    message = {
        'status': 500,
        'message': error.message or 'Internal server error'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp


def _on_404(error=None):
    message = {
        'status': 404,
        'message': error.message or 'Not Found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


def _on_403(error=None):
    message = {
        'status': 403,
        'message': error.message or 'Forbidden'
    }
    resp = jsonify(message)
    resp.status_code = 403
    return resp

def _on_422(error=None):
    message = {
        'status': 422,
        'message': error.message or 'Unprocessable entity'
    }
    resp = jsonify(message)
    resp.status_code = 422
    return resp

__version__ = '0.1'
