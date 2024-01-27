from webob import Request, Response

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

    def handle_request(self, request):
        response = Response()

        handler = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)

        return response 

    def default_response(self, response):
        response.status_code = 404 
        response = "Not Found."

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    


