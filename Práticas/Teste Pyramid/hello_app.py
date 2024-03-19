# CRIANDO UMA PÁGINA SIMPLES 

# Função para criar um servidor para a aplicação
from wsgiref.simple_server import make_server

# Parte importante do framework para criar routes e views
from pyramid.config import Configurator

# Função para criar respostas para requisições 
from pyramid.response import Response

def hello_world(request):
    return Response('Olá, Mundo!')

if __name__ == "__main__":
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

