from parserbot import create_app

app = create_app()
host = '127.0.0.1' if app.config['DEBUG'] else '0.0.0.0'

if __name__ == "__main__":
    app.run(host=host, debug=app.config['DEBUG'])
