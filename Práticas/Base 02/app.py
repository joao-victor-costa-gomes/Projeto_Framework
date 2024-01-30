from api import API
# waitress-serve --listen=*:8000 app:app

app = API()

@app.route("/")
def home(request, response):
        response.text = "<h1> Essa é a primeira página <h1/> "

@app.route("/home")
def home(request, response):
        response.text = "Hello! This is the HOME page!"

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
        