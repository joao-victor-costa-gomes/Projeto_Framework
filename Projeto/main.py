from framework.server import Server
from framework.algorithms.pca import PCA_2D

app = Server()

mobile = PCA_2D(
    "PCA Mobile Devices",
    "mobile_devices.csv", 
    0.2,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    'price_range'
)

@app.route('/')
def home(request, response):
    response.text = "<h1>HOME PAGE</h1>"

@app.route('/pca')
def pca(request, response):
    response.text = app.template("index.html", context= {
        "imagem": f"{mobile.imagem}", 
        "nome" : f"{mobile.nome}",
        "amostragem" : f"{mobile.amostragem}",
        "tempo" : f"{mobile.tempo}",
        "desempenho" : f"{mobile.desempenho}",
        "variancia" : f"{mobile.variancia}",
        "base_dados": f"{mobile.base_dados}"   
    })


if __name__ == "__main__":
    app.run_server("localhost", 8000)