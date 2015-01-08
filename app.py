from flask import Flask, jsonify, request
from parsers import calais, dbpedia, freebase, stanford, zemanta
from user import User

app = Flask(__name__)


@app.route('/')
def hello_world():
    message = {
        'status': 200,
        'message': 'Hello world. Find me on github at https://github.com/mailbackwards/parserbot'
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.route('/opencalais', methods=['GET', 'POST'])
def run_calais():
    if not authorized():
        return forbidden()
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = calais.entity_call(payload)
    return respond(results)


@app.route('/zemanta', methods=['GET', 'POST'])
def run_zemanta():
    if not authorized():
        return forbidden()
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = zemanta.ZemantaAPI().entity_query(payload)
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


@app.route('/stanford', methods=['GET', 'POST'])
def run_stanford():
    if not authorized():
        return forbidden()
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    stanford_results = stanford.get_entities(payload)
    # dedupe the lists so that we aren't calling dbpedia repeatedly
    stanford_results = dict((key, list(set(value))) for key, value in stanford_results.items())
    # now get dbpedia URLs for them
    dbp_results = get_dbpedia_resources(stanford_results)
    return respond(dbp_results)


@app.route('/dbpedia', methods=['GET', 'POST'])
def run_dbpedia():
    if not authorized():
        return forbidden()
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = dbpedia.DbpediaAPI().get_entities(payload)
    return respond(results)


@app.route('/scrape/<path:path>')
def scrape(path):
    if not authorized():
        return forbidden()
    scraper_module = __import__('scrapers', globals(), locals(), [str(path)], -1)
    path_module = getattr(scraper_module, path)
    results = path_module.scrape()
    return respond(results)


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


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(500)
def internal_server_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal server error'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp


@app.errorhandler(403)
def forbidden(error=None):
    message = {
        'status': 403,
        'message': 'Forbidden'
    }
    resp = jsonify(message)
    resp.status_code = 403
    return resp


def authorized():
    params = request.args if request.method == 'GET' else request.form
    if not 'key' in params:
        return False
    try:
        user = User(params.get('key'))
    except:
        return False
    return True
