#!/usr/bin/python

import cherrypy
from cherrypy import expose
import simplejson
import RPi.GPIO as gpio

class restRPI:
    
    def __init__(self):
        cherrypy.response.headers['Content-Type'] = "application/json;charset=utf-8"
    
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
            json = cherrypy.request.body.readline()
            cherrypy.log(json)
            cherrypy.log(json['numGpio'])
            strParams = simplejson.dumps(json)
            cherrypy.log(strParams)
            params = simplejson.loads(strParams)
            cherrypy.log(params)
            cherrypy.log(params['numGpio'])
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
                  'server.socket_port' : 8282,
                  'log.screen' : True
        },
        '/' : {
               'tools.encode.on':True,
               'tools.encode.encoding':'utf-8'
        }
}


cherrypy.config.update(conf)
cherrypy.quickstart(restRPI(),"/", conf)