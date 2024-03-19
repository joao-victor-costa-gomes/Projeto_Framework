# EXIBINDO INFORMAÇÕES DE JSON 

# Função para criar um servidor para a aplicação
from wsgiref.simple_server import make_server

# Parte importante do framework para criar routes e views
from pyramid.config import Configurator

# Decortator para criar registros de views
from pyramid.view import view_config

@view_config(
    route_name = 'home', 
    renderer = 'json',
)
def home(request):
    return {"Nome" : "João Victor", "Idade" : 20}

if __name__ == "__main__":
    with Configurator() as config:
        config.add_route('home', '/')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()


