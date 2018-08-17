from werkzeug.wsgi import DispatcherMiddleware
from parserbot import create_parser_app
try:
    from scraperbot import create_scraper_app
except ImportError:
    create_scraper_app = None

app = create_parser_app()

if create_scraper_app is not None:
    app.wsgi_app = DispatcherMiddleware(
        app.wsgi_app, {'/scrape': create_scraper_app()})
host = '127.0.0.1' if app.config['DEBUG'] else '0.0.0.0'

if __name__ == '__main__':
    app.run(host=host, debug=app.config['DEBUG'])
