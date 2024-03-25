# Código reponsável por associar paths (caminhos) às routes (rotas) da URL da aplicação

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler):
        self.routes[path] = handler 

    def find_handler(self, path):
        return self.routes.get(path)