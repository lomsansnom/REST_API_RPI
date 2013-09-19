#!/usr/bin/python

import cherrypy
from cherrypy import expose
import simplejson

class restRPI:
    
    def __init__(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
        
    def test(self):
        ret={"year":"test"}
        ret['month']='nothing'
        return simplejson.dumps(ret)
    
conf={
        'global':{
                  'server.socket_host' : '0.0.0.0',
                  'server.socket_port' : 8282
        },
        '/' : {
                 'tools.encode.on':True,
                 'tools.encode.encoding':'utf-8',
                 'tools.proxy.on':True,   # Required to handle https url base properly.
        }
}

cherrypy.config.update(conf)
cherrypy.quickstart(restRPI(),"/", conf)