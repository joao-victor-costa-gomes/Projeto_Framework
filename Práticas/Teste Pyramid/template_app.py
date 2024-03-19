from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

@view_config(
    route_name='hello',
    renderer='templates/home.jinja2'
)
def home(request):
    return {"greet": 'Welcome', "name": 'Tut Ankh Amun!'}


if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_static_view(name='static', path='static')
        config.include('pyramid_debugtoolbar')
        config.add_route('hello', '/')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()