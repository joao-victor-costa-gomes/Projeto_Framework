# Código responsável por lidar com as requests (requisições) e dar uma resposta equivalente

from webob import Request, Response 

class Request_Handler:
    def __init__(self, router):
        self.router = router

    def handle_request(self, request):
        handler = self.router.find_handler(request.path)
        response = Response()

        if handler:
            handler(request, response)
            return response   

        else:  
            response.status_code = 404
            response.text = "<h1>ERROR 404 - PAGE NOT FOUND.</h1>"

        return response

        

