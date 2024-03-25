from api import API
from middleware import Middleware
# waitress-serve --listen=*:8000 app:app

app = API()

@app.route("/")
def home(request, response):
        response.text = "<h1> Essa é a primeira página <h1/> "

@app.route("/home")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be user")

@app.route("/about")
def about(request, response):
        response.text = "Hello! This is the ABOUT page!"  

@app.route("/hello/{name}")
def hello(request, response, name):
        response.text = f"Hello, {name}!"

@app.route("/book")
class BooksResource:
        def get(self, request, response):
                response.text = "Books page"

def alternative_add_route(request, response):
        response.text = "Another way to add routes."
app.add_route("/alternative", alternative_add_route)

@app.route("/template_test")
def template_test_handler(req, resp):
        resp.body = app.template("index.html", context={"name": "COMIDAS", "title": "Lista de comidas", "input":"Batata frita :)"}).encode()

def custom_exception(request, response, exception_cls):
        response.text = "Oops! Something went wrong. Please contact our support."
app.add_exception_handler(custom_exception)

class SimpleCustomMiddleware(Middleware):
        def process_request(self, req):
                print("Processing request ", req.url)
        
        def process_response(self, req, resp):
                print("Processing response ", req.url)

app.add_middleware(SimpleCustomMiddleware)