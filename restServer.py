#!/usr/bin/python

import cherrypy
from cherrypy import expose
import simplejson
import RPi.GPIO as gpio

class restRPI:
    
    def __init__(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
    
    @expose   
    def setGpio(self):
        try:
            strParams = simplejson.dumps(cherrypy.request.body.readline())
            params = simplejson.loads(strParams)
            ret = {"OK" : true}
        except:
            ret = {"OK" : false}
            ret['Erreur'] = "Parametres invalides"
            return simplejson.dumps(ret)
        
        try:
            gpio.setmode(gpio.BOARD)
            gpio.setup(params[u'numGpio'],gpio.OUT)
            gpio.output(params[u'numGpio'], params[u'etat'])
        except:
           ret['OK'] = false
           ret['Erreur'] = "Echec lors du changement d'état du GPIO" 
    
conf={
        'global':{
                  'server.socket_host' : '0.0.0.0',
                  'server.socket_port' : 8282
        }
}

cherrypy.config.update(conf)
cherrypy.quickstart(restRPI(),"/", conf)