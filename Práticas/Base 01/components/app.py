from .requestcom import Request
from .responsecom import Response, Http404
from .routercom import Router 

class App: 

    def __init__(self):
        self.router = Router() 

    def set_routes(self, routes: list):
        for path in routes: 
            self.router.add_route(path)

    # Pare importante do código 
    def __call__(self, environment, start_response):
        print(f"Incoming request: ")

        request: Request = Request(environment, start_response)
        try:
            print(f"Incoming request: {request.path}")
            function = self.router.get_route(request.path)
            if function is not None:
                response: Response = function(request)
                return response.make_response()
            else: 
                Http404(request).make_response()
        except Exception as e:
            print(e) 
            return Http404(request).make_response()