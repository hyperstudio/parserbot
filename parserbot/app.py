from flask import app, jsonify, request
from parserbot import calais, dbpedia, stanford, zemanta
import hashlib

app = Flask(__name__)


def authorized():
    return request.headers.get('Authentication') == hashlib.md5(app.config['SECRET_KEY']).hexdigest()


def handle(f):
    payload = request.json.get('payload')
    return f(payload)


def respond(results):
    message = {
        'status': 200,
        'message': 'Success',
        'count': len(results),
        'results': results
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.route('/', methods=['GET'])
def hello_world():
    message = {
        'status': 200,
        'message': 'Success',
        'results': 'Hello world! Find me on github at https://github.com/mailbackwards/parserbot'
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.route('/opencalais', methods=['POST'])
def run_calais():
    if not authorized():
        return forbidden()
    results = handle(calais.entity_call)
    return respond(results)


@app.route('/zemanta', methods=['POST'])
def run_zemanta():
    if not authorized():
        return forbidden()
    results = handle(zemanta.ZemantaAPI().entity_query)
    return respond(results)


def get_dbpedia_resources(stanford_results):
    dbp_results = []
    for entity_type, entity_list in stanford_results.items():
        for keyword in entity_list:
            dbp_response = dbpedia.DbpediaAPI().keyword_search(keyword)['results']
            dbp_resource = dbp_response[0] if dbp_response else {}
            response = {
                'uri': None,
                'stanford_type': entity_type.lower(),
                'stanford_name': keyword
            }
            response.update(dbp_resource)
            dbp_results.append(response)
    return dbp_results


@app.route('/stanford', methods=['POST'])
def run_stanford():
    if not authorized():
        return forbidden()
    stanford_results = handle(stanford.get_entities)
    # dedupe the lists so that we aren't calling dbpedia repeatedly
    stanford_results = dict((key, list(set(value))) for key, value in stanford_results.items())
    # now get dbpedia URLs for them
    dbp_results = get_dbpedia_resources(stanford_results)
    return respond(dbp_results)


@app.route('/dbpedia', methods=['POST'])
def run_dbpedia():
    if not authorized():
        return forbidden()
    results = handle(dbpedia.DbpediaAPI().get_entities)
    return respond(results)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    if error is not None:
        message['error'] = error
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(500)
def internal_server_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal server error'
    }
    if error is not None:
        message['error'] = error
    resp = jsonify(message)
    resp.status_code = 500
    return resp


@app.errorhandler(403)
def forbidden(error=None):
    message = {
        'status': 403,
        'message': 'Forbidden'
    }
    if error is not None:
        message['error'] = error
    resp = jsonify(message)
    resp.status_code = 403
    return resp
