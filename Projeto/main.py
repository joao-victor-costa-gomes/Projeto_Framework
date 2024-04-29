from framework.server import Server
from framework.algorithms.pca import PCA_2D

mobile = PCA_2D(
    "PCA Mobile Devices",
    "mobile_devices.csv", 
    0.2,
    ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi'],
    'price_range'
)

app = Server()

# ROTAS
@app.route('/')
def home(request, response):
    response.text = app.template("home_template.html")

@app.route('/vermelho')
def home(request, response):
    response.text = app.template("vermelho_template.html")

@app.route('/pca')
def home(request, response):
    response.text = app.template("pca_template.html", context= {
        "imagem": f"{mobile.imagem}", 
        "nome" : f"{mobile.nome}",
        "amostragem" : f"{mobile.amostragem}",
        "tempo" : f"{mobile.tempo}",
        "desempenho" : f"{mobile.desempenho}",
        "variancia" : f"{mobile.variancia}"
    })

@app.route("/error")
def error_mes(request, response):
    raise AssertionError("Mensagem de erro no terminal")

# MENSAGENS DE ERRO
def error404(request, response):
    response.text = app.template("error_404_template.html")
app.add_404_handler(error404)

def something_went_wrong(request, response, exception_cls):
    response.text = app.template("something_wrong.html")
app.add_exception_handler(something_went_wrong)



if __name__ == "__main__":
    app.run_server("localhost", 8000)