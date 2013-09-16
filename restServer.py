import cherrypy

class HelloWorld:
    def index(self):
        return "Hello world!"
    index.exposed = True

cherrypy.quickstart(HelloWorld())
#conf = {
#    'global': {
 #       'server.socket_host': '0.0.0.0',
  #      'server.socket_port': 8000,
   # },
#}

##cherrypy.quickstart(root, '/', conf)