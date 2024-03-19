# Código mais básico usando o CherryPy

import cherrypy

class Hello_World(object):
    @cherrypy.expose
    def index(self):
        return "Hello, World!"


if __name__ == "__main__":
    cherrypy.quickstart(Hello_World())