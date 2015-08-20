from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from parserbot import create_parser_app
try:
	from scraperbot import create_scraper_app
except ImportError:
	secondary_apps = {}
else:
	secondary_apps = {'/scraper': create_scraper_app()}

app = create_parser_app()

wsgi_middleware = DispatcherMiddleware(app, secondary_apps)
host = '127.0.0.1' if app.config['DEBUG'] else '0.0.0.0'

if __name__ == '__main__':
    if app.config['DEBUG']:
    	run_simple(host, 3000, wsgi_middleware, use_reloader=True)
    else:
        app.run(host=host, debug=app.config['DEBUG'])
