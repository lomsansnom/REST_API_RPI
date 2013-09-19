#!/usr/bin/python

import cherrypy
from cherrypy import expose
import simplejson

class restRPI:
    @expose
    def index(self):
        return "It's working"
    
    @expose
    def login(self, json):
        dict = simplejson.loads(simplejson.dumps(json))
        return dict
        
conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8282,
    },
}

cherrypy.quickstart(restRPI(), '/', conf)

