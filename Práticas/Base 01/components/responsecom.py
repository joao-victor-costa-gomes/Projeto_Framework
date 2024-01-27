from .requestcom import Request
from typing import Callable # Para indicar que o objeto pode ser chamado como uma função

# A ideia de resposta é que mandamos valores para ela e a mesma retorna valores para o cliente 
class Response:
    def __init__(self, request: Request, status_code: str, content_type: str):
        self.status_code: str = status_code 
        self.start_response: Callable = request.start_response
        self.content_type: str = content_type
        self.headers: list= [('Content-Type', self.content_type)]
        self.response_content = []

    # Exibe a resposta da página, até mesmo se for códigos de status
    def make_response(self):
        self.start_response(self.status_code, self.headers)
        return self.response_content

class HttpResponse(Response): 
    def __init__(self, request: Request, content: str, status_code: str ='200 - OK', content_type: str ='text/html'):
        super().__init__(request, status_code, content_type)
        if type(content) == str:
            content = content.encode() # Converte string em sequência de bytes    
        self.response_content.append(content)

class JsonResponse(Response): 
    def __init__(self, request: Request, content: str, status_code: str ='200 - OK', content_type: str ='application/json'):
        super().__init__(request, status_code, content_type)
        content = json.dumps(content).encode() # Converter para JSON
        self.response_content.append(content)

class ErrorResponse(Response): 
    def __init__(self, request: Request, error_code: str):
        super().__init__(request, '404 Not Found', 'text/html')


class Http404(ErrorResponse): 
    def __init__(self, request):
        super().__init__(request, '404 Not Found')
        self.response_content.append('404 Not Found'.encode())
