from webob import Request, Response
from parse import parse 

class API:

    def __init__(self):
        self.routes = {}

    def route(self, path):

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

    


