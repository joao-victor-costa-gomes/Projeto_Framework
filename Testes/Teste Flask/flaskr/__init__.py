#__init__.py indica que o diretório flaskr deve ser tratado como um pacote 

import os 
from flask import Flask 

def create_app(test_config=None): 
    # Cria e configura o app 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # Carrega a instância config, se ela existir, quando não estiver testando
        app.config.from_pyfile('config.py', silent=True)
    else: 
        # Carrega a test config se passada 
        app.config.from_mapping(test_config)

    # Assegurar que a pasta da instância existe
    try:
        os.makedirs(app.instance_path)
    except OSError: 
        pass 

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
        
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app 
