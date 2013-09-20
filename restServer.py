#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        except:
            ret = {"OK" : False}
            ret['Erreur'] = "Paramètres invalides"
            return json.dumps(ret)
        
        if  "numGpio" and "etat" in params :
            try:
                gpio.setmode(gpio.BOARD)
                gpio.setup(params['numGpio'],gpio.OUT)
                gpio.output(params['numGpio'], params['etat'])
                ret = {"OK" : True}
            except:
                ret = {"OK" : False}
                ret['Erreur'] = "Echec lors du changement d'état du GPIO"
        else :
            ret = {"OK" : False}
            ret['Erreur'] = "numGpio et etat sont obligatoires"
        
        return json.dumps(ret)
    
    @expose
    def connectDB(self):
        try:
            params = json.loads(cherrypy.request.body.readline())
        except:
            ret = {"OK" : False}
            ret['Erreur'] = "Paramètres invalides"
            return json.dumps(ret)
        
        if 'query' and 'username' and 'password' in params:
            if params['query'] == 'login':
                requete = """SELECT "password" FROM "Utilisateurs" WHERE "login"=\'' + params['username'] + '\'""";
            elif params['quert'] == 'ajouterMembre':
                requete = """INSERT INTO "Utilisateurs" ("login", "password") VALUES (\'' + params['username'] + '\', \'' + params['password'] + '\')""";

            try:
                sessionDB = psycopg2.connect(host = self.__host, port = self.__port, dbname = self.__dbname, user = self.__user, password = self.__password)
                curseur = sessionDB.cursor()
                curseur.execute(requete)
                cherrypy.log(','.join(map(str, curseur.fetchall())))
                ret = {'OK' : True}
            except:
                cherrypy.log("Erreur lors de la connexion a la DB")
                ret = {"OK" : False}
                ret['Erreur'] = "Erreur lors de la connexion a la DB"
        else:
            ret = {"OK" : False}
            ret['Erreur'] = "query, username et password sont obligatoires"
        
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