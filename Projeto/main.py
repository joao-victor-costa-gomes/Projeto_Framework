from framework.server import Server
from framework.algorithms.pca import PCA_2D

app = Server()

@app.route('/')
def home(request, response):
    response.text = "<h1>ESSA É A HOME PAGE</h1>"

if __name__ == "__main__":
    app.run_server("localhost", 8000)