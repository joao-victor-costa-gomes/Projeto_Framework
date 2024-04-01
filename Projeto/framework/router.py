class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler):
        
        if path in self.routes:
            raise AssertionError(f"\n\nThe path '{path}' already exists.\n")

        self.routes[path] = handler 

    def find_handler(self, path):
        return self.routes.get(path)