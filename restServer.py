#!/usr/bin/python

import cherrypy
from cherrypy import expose
import json
import RPi.GPIO as gpio
import psycopg2

class restRPI:
    
    __contentType = "application/json;charset=utf-8"
    __host = "192.168.1.45"
    __port = 5432
    __dbname = "lomsansnom"
    __user = "lomsansnom"
    __password = "postgres"
    
    def __init__(self):
        cherrypy.response.headers['Content-Type'] = self.__contentType
        
    @expose   
    def setGpio(self):
        try:
            params = json.loads(cherrypy.request.body.readline())
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
        
        return json.dumps(ret)
    
    @expose
    def connectDB(self):
       # try:
            sessionDB = psycopg2.connect(host = self.__host, port = self.__port, dbname = self.__dbname, user = self.__user, password = self.__password)
            curseur = sessionDB.cursor()
            query = curseur("""SELECT * FROM "Utilisateurs" """)
            cherrypy.log(query.fetchall())
       # except:
         #   cherrypy.log("Erreur lors de la connexion a la DB")
        #    return False
        
    
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