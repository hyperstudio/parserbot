from flask import current_app, Blueprint, jsonify, request, abort
from parserbot import calais, dbpedia, stanford, zemanta
import hashlib

bp = Blueprint('parserbot', __name__)


def authorized():
    return request.headers.get('Authentication') == hashlib.md5(app.config['SECRET_KEY']).hexdigest()


def handle(f):
    if not authorized():
        abort(403)
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


@bp.route('/', methods=['GET'])
def hello_world():
    message = {
        'status': 200,
        'message': 'Hello world! Find me on github at https://github.com/mailbackwards/parserbot'
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@bp.route('/opencalais', methods=['POST'])
def run_calais():
    results = handle(calais.entity_call)
    return respond(results)


@bp.route('/zemanta', methods=['POST'])
def run_zemanta():
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


@bp.route('/stanford', methods=['POST'])
def run_stanford():
    stanford_results = handle(stanford.get_entities)
    # dedupe the lists so that we aren't calling dbpedia repeatedly
    stanford_results = dict((key, list(set(value))) for key, value in stanford_results.items())
    # now get dbpedia URLs for them
    dbp_results = get_dbpedia_resources(stanford_results)
    return respond(dbp_results)


@bp.route('/dbpedia', methods=['POST'])
def run_dbpedia():
    results = handle(dbpedia.DbpediaAPI().get_entities)
    return respond(results)
