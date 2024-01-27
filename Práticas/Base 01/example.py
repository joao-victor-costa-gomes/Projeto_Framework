from components.app import App
from components.routercom import Path
from components.responsecom import HttpResponse
from components.requestcom import Request

# Para rodar algo, precisamos de um servidor WSGI
from wsgiref.simple_server import make_server 

app = App()

def hello_world(request: Request):
    return HttpResponse(request,'''
    <html>
    <body>
    <h2>HELLO, WORLD!</h2>
    </body>
    </html>
    ''')

routes = [
    Path('/', hello_world),
]

app.set_routes(routes)
server = make_server('127.0.0.1', 8001, app)
print("Server running on port 8001")
server.serve_forever()