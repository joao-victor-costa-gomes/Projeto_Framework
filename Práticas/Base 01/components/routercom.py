# Classe para validar essas rotas 
class Path:
    def __init__(self, path, function):
        self.path = path 
        self.function = function 

    # Função para verificar existência 
    def match(self, path):
        if self.path == path:
            return True
        return False 

# Classe para aceitar rotas, essas rotas devem ser no formato de lista
class Router:
    def __init__(self, routes=None): # Valor das rotas é vazio por padrão 
        self.routes = list(routes) if routes else []

    # Adiciona um caminho à variável "routes"
    def add_route(self, path):
        self.routes.append(path)

    def get_route(self, path):
        for route in self.routes:
            if route.match(path):
                return route.function
        return None