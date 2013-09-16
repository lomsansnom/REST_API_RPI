import cherrypy

class HelloWorld:
    def index(self):
        return "Hello world!"
    index.exposed = True

conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8000,
    },
}

cherrypy.quickstart(HelloWorld(), '/', conf)

