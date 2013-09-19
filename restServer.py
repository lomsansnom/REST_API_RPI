#!/usr/bin/python

import cherrypy
from cherrypy import expose
import simplejson
import RPi.GPIO as gpio

class restRPI:
    
    def __init__(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
    
    def arrangerDict(self, dict):
        ret={}
        for key, value in dict:
            if key[0:1] == "u'" and value[0:1] == "u'":
                ret[key[2:-1]] = value[2:-1]
            else:
                ret[key[2:-1]] = value
        return ret
        
    @expose   
    def setGpio(self):
        try:
            strParams = simplejson.dumps(cherrypy.request.body.readline())
            params = self.arrangerDict(simplejson.loads(strParams))
            ret = {"OK" : True}
        except:
            ret = {"OK" : False}
            ret['Erreur'] = "Parametres invalides"
            return simplejson.dumps(ret)
        
        try:
            gpio.setmode(gpio.BOARD)
            gpio.setup(params['numGpio'],gpio.OUT)
            gpio.output(params['numGpio'], params['etat'])
        except:
           ret['OK'] = False
           ret['Erreur'] = "Echec lors du changement d'etat du GPIO"
        
        return simplejson.dumps(ret)
    
conf={
        'global':{
                  'server.socket_host' : '0.0.0.0',
                  'server.socket_port' : 8282
        }
}

cherrypy.config.update(conf)
cherrypy.quickstart(restRPI(),"/", conf)