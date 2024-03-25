# Código responsável por criar um servidor e fazer ele rodar 

# BIBLIOTECAS 
from webob import Request, Response 
from waitress import serve

# ARQUIVOS DO FRAMEWORK
from framework.router import Router
from framework.request_handler import Request_Handler

class Server:

    def __init__(self):
        self.router = Router() 
        self.request_handler = Request_Handler(self.router)
        
    def route(self, path):
        def decorator(handler):
            self.router.add_route(path, handler)
            return handler 
        return decorator

    def __call__(self, environ, start_response):
        request = Request(environ )
        response = self.request_handler.handle_request(request)
        return response(environ, start_response) 

    def run_server(self, host, port):
        serve(self, host=host, port=port)





