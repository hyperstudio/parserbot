from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/all')
def run_all():
    return

@app.route('/calais')
def run_calais():
    return

@app.route('/zemanta')
def run_zemanta():
    return

@app.route('/stanford')
def run_stanford():
    return

@app.route('/dbpedia')
def run_dbpedia():
    return

if __name__ == "__main__":
    app.run()