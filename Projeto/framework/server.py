# BIBLIOTECAS EXTERNAS
import os
import sys 
from webob import Request, Response 
from waitress import serve
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# ARQUIVOS DO FRAMEWORK
from framework.request_handler import Request_Handler
from framework.router import Router

class Server:

    def __init__(self):
        self.router = Router() 
        self.request_handler = Request_Handler(self.router)

        self.templates_environment = Environment(loader=FileSystemLoader(os.path.abspath("templates")))
        self.whitenoise = WhiteNoise(self.wsgi_app, root="static")

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.request_handler.handle_request(request)
        return response(environ, start_response) 

    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)

    def route(self, path):
        def decorator(handler):
            self.router.add_route(path, handler)
            return handler 
        return decorator

    def template(self, template_name, context=None):
        if context is None:
            context = {}
        return self.templates_environment.get_template(template_name).render(**context)
        
    def add_exception_handler(self, exception_handler):
        self.request_handler.exception_handler = exception_handler

    def add_404_handler(self, error_handler):
        self.request_handler.error_handler = error_handler

    def run_server(self, host, port):
        print(f"\nServidor rodando em http://{host}:{port}\n")
        serve(self, host=host, port=port)