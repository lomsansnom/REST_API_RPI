#!/usr/bin/python

import cherrypy
from cherrypy import expose
import simplejson

class restRPI:
    
    def __init__(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
    
    @expose   
    def test(self):
        ret={"year":"test"}
        ret['month']='nothing'
        return simplejson.dumps(cherrypy.request.body)
    
conf={
        'global':{
                  'server.socket_host' : '0.0.0.0',
                  'server.socket_port' : 8282
        }
}

cherrypy.config.update(conf)
cherrypy.quickstart(restRPI(),"/", conf)