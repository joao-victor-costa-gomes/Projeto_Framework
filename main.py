from framework.server import Server
from framework.algorithms.pca import PCA

# Criando um gráfico para ser utilizado na rota "/pca"
mobile = PCA(
    "PCA-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi'],
    ['price_range'],
    2,
    'png',
    False
    )

app = Server()

# Rota padrão
@app.route('/')
def home(request, response):
    response.text = "<h1>ESSA É A HOME PAGE</h1>"

# Rota para testar algoritmo
@app.route('/pca')
def template(request, response):
    response.text = app.template("pca.html", context={
        "title":"Gráficos gerados pelo algoritmo PCA",
        "imagem": mobile.imagem,
        "tempo": mobile.tempo,
        "variancia": mobile.variancia,
    })

if __name__ == "__main__":
    app.run_server("localhost", 8000)