from webob import Request, Response
from inspect import isclass 

class Request_Handler:
    def __init__(self, router):
        self.router = router
        self.exception_handler = None 

    def handle_request(self, request):
        handler = self.router.find_handler(request.path)
        response = Response()

        try:
            if handler:

                if isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None) 

                    if handler is None:
                        raise AttributeError("Method now allowed", request.method)

                handler(request, response)

            else:  
                response.status_code = 404
                response.text = "<h1>ERROR 404 - PAGE NOT FOUND.</h1>"
        
        except Exception as exception:
            if self.exception_handler is None:
                raise exception       
            else:
                self.exception_handler(request, response, exception)

        return response


    
            

        

