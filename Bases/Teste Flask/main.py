from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jogos")
def jogos():
    return render_template("jogos.html")

@app.route("/usuarios")
def usuarios(nome_usuario="João Victor"):
    return render_template("usuario.html", nome_usuario=nome_usuario)

if __name__ == "__main__":
    app.run(debug=True)

