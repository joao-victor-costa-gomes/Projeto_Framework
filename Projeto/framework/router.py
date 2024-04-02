class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler):
        
        if path in self.routes:
            raise AssertionError(f"\n\nO caminho '{path}' já está em uso.\n")

        self.routes[path] = handler 

    def find_handler(self, path):
        return self.routes.get(path)