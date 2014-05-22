from flask import Flask, jsonify, request
from parsers import calais, dbpedia, freebase, stanford, zemanta
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/all', methods=['GET', 'POST'])
def run_all():
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    return jsonify({"results": results})

@app.route('/calais', methods=['GET', 'POST'])
def run_calais():
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = calais.entity_call(payload, id_str)
    return jsonify({"results": results})

@app.route('/zemanta', methods=['GET', 'POST'])
def run_zemanta():
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = zemanta.ZemantaAPI().entity_query(payload)
    return jsonify({"results": results})

def get_dbpedia_resources(stanford_results):
    dbp_results = []
    for entity_type, entity_list in stanford_results.items():
        for keyword in entity_list:
            dbp_response = dbpedia.keyword_search(keyword)['results']
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
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    stanford_results = stanford.get_entities(payload)
    # dedupe the lists so that we aren't calling dbpedia repeatedly
    stanford_results = dict((key, list(set(value))) for key, value in stanford_results.items())
    # now get dbpedia URLs for them
    dbp_results = get_dbpedia_resources(stanford_results)
    return jsonify({"results": dbp_results})

@app.route('/dbpedia', methods=['GET', 'POST'])
def run_dbpedia():
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = dbpedia.get_entities(payload)
    return jsonify({"results": results})