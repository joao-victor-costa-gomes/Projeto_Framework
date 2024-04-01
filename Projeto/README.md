## Instalando os requisitos 

Primeiro, após clonar o projeto, é ideal que você crie um ambiente virtual e instale todos os requisitos do framework utilizando o comando listado abaixo:

```bash
pip install -r requirements.txt
```

## Rodando o framework

Para utilizar o framework, primeiro você deve criar um objeto Server cujo construtor deve ser importado do arquivo server.py do diretório framework. Depois disso, você deve criar uma rota e sua função (por padrão recomendo deixar como está abaixo). Por fim, basta indicar em qual host e em qual porta você quer que o servidor rode e então você executa o arquivo main.py. Agora só abrir o seu navegador em uma página com seu host e porta selecionada. 

```bash
from framework.server import Server

app = Server()

@app.route('/')
def home(request, response):
    response.text = "<h1>HOME PAGE</h1>"

if __name__ == "__main__":
    app.run_server("localhost", 8000)
 ```

## Adicionando mais rotas

Você pode adicionar quantas portas você quiser, contanto que sua rota e nome de função sejam diferentes.

```bash
from framework.server import Server

app = Server()

@app.route('/')
def home(request, response):
    response.text = "<h1>HOME PAGE</h1>"

@app.route('/about')
def about(request, response):
    response.text = "<h1>ABOUT PAGE</h1>"

@app.route('/contacts')
def contacts(request, response):
    response.text = "<h1>CONTACTS PAGE</h1>"

if __name__ == "__main__":
    app.run_server("localhost", 8000)
 ```

## Adicionando rotas com templates

Se você quiser criar uma página utilizando arquivos html, css ou js, basta seguir o exemplo abaixo. Lembre de deixar os arquivos .html em uma pasta chamada "templates" e os arquivos css e js dentro de uma página chamada "static", para o framework importar elas automaticamente.

```bash
from framework.server import Server

app = Server()

@app.route('/template')
def template(request, response):
    response.text = app.template("index.html", context={"title":"TÍTULO DA PÁGINA", "name":"NOME DA PÁGINA"}).encode()

if __name__ == "__main__":
    app.run_server("localhost", 8000)
 ```

Esse "context={}" serve para adicionar "inputs" em um arquivo .html, basta colocar o nome do input entre {{ nome_input }}. Aqui um exemplo:

```bash
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/main.css" type="text/css" rel="stylesheet">
    <title>{{title}}</title>
</head>
<body>
    <h1> {{name}} </h1>
</body>
</html>
 ```

## Mensagens de comportamentos inesperados 

Sabe quando você entra em algum site e aparece aquelas mensagens de "Oops! Ocorreu algo inesperado. Tente novamente mais tarde"? Também é possível adicionar elas tendo como referência o seguinte modelo: 

```bash
def something_went_wrong(request, response, exception_cls):
    response.text = "<h1>Oops! Something went wrong.</h1>"

app.add_exception_handler(something_went_wrong)

@app.route("/error")
def exception_throwing_handler(request, response):
    raise AssertionError("Mensagem de erro no terminal")
 ```