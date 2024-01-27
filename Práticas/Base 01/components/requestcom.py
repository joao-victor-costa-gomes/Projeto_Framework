import cgi 

# Criar um objeto para segurar armazenar todos os dados e parâmetros de "POST"
class PostBody:
    def __init__(self, data):
        self.data = data

    # Pegar data do POST
    def get(self, key):
        value = self.data.get(key, [''])
        if type(value) == str:
            value = cgi.escape(value)
        return value 

    # Maneira de setar valores 
    def set(self, key, value):
        self.data[key] = value

    def __iter__(self):
        for key, value in self.data:
            yield key, value 

class Request:
    def __init__(self, environment, start_response):
        # Atribui o argumento 'environment' ao atributo 'environment' da instância
        self.environment = environment

        # Atribui valores associados às chaves do dicionário 'environment' aos atributos (aqueles que começam com self.)
        self.http_host = environment['HTTP_HOST']
        self.http_user_agent = environment['HTTP_USER_AGENT']
        self.lang = environment.get('LANG')
        self.method = environment.get('REQUEST_METHOD')
        self.path = environment.get('PATH_INFO')
        self.host_address = environment.get('HTTP_HOST')
        self.gateway_interface = environment.get('GATEWAY_INTERFACE')
        self.server_port = environment.get('SERVER_PORT')
        self.remote_host = environment.get('REMOTE_HOST')
        self.content_type = environment.get('CONTENT_TYPE')
        self.content_length = environment.get('CONTENT_LENGTH')

        # Recebe os query sets que serão mandados para o endpoint, query sets representam "consultas" 
        # google.com/search?q="O que vem aqui dentro são nossos queries"
        self.parse_query_set()

    def parse_query_set(self):
        if self.method != 'POST':
            return 
        self.post = PostBody({})    
        environment = self.environment

        # Um objeto FieldStorage é responsável por receber e processsar dados
        field_storage = cgi.FieldStorage(
            fp = environment['wsgi.input'], 
            environment = environment, 
            keep_blank_values = True
        ) 

        for item in field_storage.list:
            if not item.filename:
                self.post.set(item.name, item.value) 
            else: 
                self.post.set(item.name, item) 
                

