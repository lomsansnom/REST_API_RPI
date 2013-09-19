#!/usr/bin/python

import cherrypy
from cherrypy import expose
import json
import RPi.GPIO as gpio

class restRPI:
    
    def __init__(self):
        cherrypy.response.headers['Content-Type'] = "application/json;charset=utf-8"
        
    @expose   
    def setGpio(self):
        #try:
        params = json.loads(json.dumps(cherrypy.request.body.readline()))
        cherrypy.log(str(type(params)))
        ret = {"OK" : True}
#        except:
 #           ret = {"OK" : False}
  #          ret['Erreur'] = "Parametres invalides"
   #         return simplejson.dumps(ret)
        
        try:
            gpio.setmode(gpio.BOARD)
            gpio.setup(params['numGpio'],gpio.OUT)
            gpio.output(params['numGpio'], params['etat'])
        except:
           ret['OK'] = False
           ret['Erreur'] = "Echec lors du changement d'etat du GPIO"
        
        return json.dumps(ret)
    
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