from parserbot.app import *

app.config.from_object('config')
host = '127.0.0.1' if app.config['DEBUG'] else '0.0.0.0'

if __name__ == "__main__":
    app.run(host=host, debug=app.config['DEBUG'])
