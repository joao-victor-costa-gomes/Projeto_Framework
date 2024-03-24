from framework.server import Server

app = Server()


@app.route('/')
def home(request, response):
    response.text = "<h1>HOME PAGE</h1>"

@app.route('/about')
def about(request, response):
    response.text = "<h1>ABOUT PAGE</h1>"

@app.route('/contacts')
def about(request, response):
    response.text = "<h1>CONTACTS PAGE</h1>"


if __name__ == "__main__":
    app.run_server("localhost", 8000)
