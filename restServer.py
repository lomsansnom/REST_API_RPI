#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from cherrypy import expose
import json
import RPi.GPIO as gpio
import psycopg2
import psycopg2.extras
import transmissionrpc
import subprocess

class restRPI:
    
    __contentType = "application/json;charset=utf-8"
    __host = "192.168.1.45"
    __port = 5432
    __dbname = "lomsansnom"
    __user = "lomsansnom"
    __password = "postgres"
    
    __transmissionHost = "127.0.0.1"
    __transmissionPort = 9091
    __transmissionUser = "pi"
    __transmissionPassword = "catal48"

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
    def connectDB(self, post=True, params=None):
        try:
            if post:
                params = json.loads(cherrypy.request.body.readline())
        except Exception as e:
            ret = {"OK" : False}
            ret['Erreur'] = "Paramètres invalides"
            cherrypy.log(str(e))
            return json.dumps(ret)
        
        cherrypy.log("paramètres : " + str(params))
        
        if 'query' and 'username' and 'password' in params:
            if params['query'] == 'login':
                requete = """SELECT "password" FROM "Utilisateurs" WHERE "login" = %s;"""
                donnees = (params['username'],)
                output = True
            elif params['query'] == 'ajouterMembre':
                requete = """INSERT INTO "Utilisateurs" ("login", "password") VALUES (%s, %s);"""
                donnees = (params['username'], params['password'])
                output = False
            
            cherrypy.log("requete :" + requete)
            cherrypy.log("donnees :" + str(donnees))
            try:
                sessionDB = psycopg2.connect(host = self.__host, port = self.__port, dbname = self.__dbname, user = self.__user, password = self.__password)
                
                if not output:
                    sessionDB.autocommit = True
                    
                curseur = sessionDB.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                curseur.execute(requete, donnees)
                
                if output:
                    ret = {"OK" : True, "res" : curseur.fetchall()}
                else:
                    ret = {'OK' : True}
                
                
            except Exception as e:
                cherrypy.log("Erreur lors de la connexion a la DB")
                cherrypy.log(str(e))
                ret = {"OK" : False}
                ret['Erreur'] = "Erreur lors de la connexion a la DB"
        else:
            ret = {"OK" : False}
            ret['Erreur'] = "query, username et password sont obligatoires"
        
        if not post :
            return ret
        else:
            return json.dumps(ret)
    
    @expose
    def login(self):
        try:
            params = json.loads(cherrypy.request.body.readline())
        except Exception as e:
            retLogin = {"OK" : False}
            retLogin['Erreur'] = "Paramètres invalides"
            cherrypy.log(str(e))
            return json.dumps(retLogin)
        
        params['query'] = 'login'
        ret = self.connectDB(False, params)
        cherrypy.log(str(ret))
        
        if ret['OK']:
            if ret['res'][0]['password'] == params['password']:
                retLogin = {"OK" : True}
            else:
                retLogin = {"OK": False}
                retLogin["Erreur"] = "Mot de passe erroné"
        else:
            retLogin = {"OK": False}
            retLogin["Erreur"] = "Erreur lors de la demande des données à la DB" 
        
        return json.dumps(retLogin)
        
    @expose
    def getListeDD(self):    
        ret = {}
        boolDD = True
        i = 2
        cmd = "sudo fdisk -l | grep /dev/sda | sed -n " 
    
        while boolDD:
            cmd += str(i) + "p"
            i += 1
            ret[i-2] = subprocess.check_output(cmd)
            cmd = cmd[0:-2]
        
        return json.dumps(ret)
            
      
    @expose
    def downloadTorrent(self):
        transmissionClient = transmissionrpc.Client(self.__transmissionHost, self.__transmissionPort, self.__transmissionUser, self.__transmissionPassword)
        
        try:
            params = json.loads(cherrypy.request.body.readline())
        except Exception as e:
            ret = {"OK" : False}
            ret['Erreur'] = "Paramètres invalides"
            cherrypy.log(str(e))
            return json.dumps(ret)
        
        try:
            transmissionClient.add_torrent(params['torrent'], download_dir = params['repertoire'])
            ret = {"OK" : True}
        except Exception as e:
            ret = {"OK" : False}
            ret['Erreur'] = "Erreur lors de l'ajout du torrent"
            cherrypy.log(str(e))
            
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