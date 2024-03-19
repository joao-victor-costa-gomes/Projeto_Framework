# Rota que aceita parâmetros

import random
import string

import cherrypy

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    # Aceita parâmetros de até 16 dígitos na própria URL
    # http://127.0.0.1:8080/generate?length=15 (Basta trocar o número por outro)
    @cherrypy.expose
    def generate(self, length=16):
        return ''.join(random.sample(string.hexdigits, int(length)))


if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())