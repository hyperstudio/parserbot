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

@app.route('/stanford', methods=['GET', 'POST'])
def run_stanford():
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = stanford.get_entities(payload)
    # dedupe the lists so that we aren't calling dbpedia repeatedly
    results = dict((key, list(set(value))) for key, value in results.items())
    # now get dbpedia URLs for them
    for entity_type, entity_list in results.items():
        for index, item in enumerate(entity_list):
            dbp_resp = dbpedia.keyword_search(item)
            dbp_results = dbp_resp['results']
            default_response = {
                'label': item,
                'uri': None
            }
            results[entity_type][index] = dbp_results[0] if dbp_results else default_response
    return jsonify(results)

@app.route('/dbpedia', methods=['GET', 'POST'])
def run_dbpedia():
    if request.method == 'GET':
        payload = request.args.get('payload')
    elif request.method == 'POST':
        payload = request.form.get('payload')
    results = dbpedia.get_entities(payload)
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)