#!/usr/bin/python

import cherrypy
from cherrypy import expose
import simplejson

class restRPI:
    @expose
    def GET(self):
        return "It's working"
    
    @expose
    def POST(self, json):
        dict = simplejson.loads(json)
        return dict

if __name__ == '__main__':

    cherrypy.tree.mount(
        restRPI(), '/',
        {
         'global': {
                    'server.socket_host': '0.0.0.0',
                    'server.socket_port': 8282,
                    },
         '/': {
               'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
               }
        })

    cherrypy.engine.start()
    cherrypy.engine.block()   
