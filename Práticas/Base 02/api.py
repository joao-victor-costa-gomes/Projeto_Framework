from webob import Request, Response
from parse import parse 
import inspect
from requests import Session 
from wsgiadapter import WSGIAdapter
import os
from jinja2 import Environment, FileSystemLoader

class API:

    def __init__(self, templates_dir="templates"):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath("templates")))

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)
 

    def add_route(self, path, handler):
        if path in self.routes:
           raise AssertionError("Such path already exists.") 
        self.routes[path] = handler 

    def route(self, path):
        if path in self.routes:
            raise AssertionError("Such path already exists.")

        def wrapper(handler):
            self.routes[path] = handler 
            return handler 

        return wrapper

    def __call__(self, environment, start_response):
        request = Request(environment)

        response = self.handle_request(request)

        return response(environment, start_response)

    def default_response(self, response):
        response.status_code = 404 
        response = "Not Found."

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method now allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        
        return None, None 

    def test_session(self, base_url="http://testserver"):
        session = Session()
        session.mount(prefix=base_url, adapter=WSGIAdapter(self))
        return session 

    

    


