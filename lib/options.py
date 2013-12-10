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


import json
from log import Logger
import support
from exceptions import FileReadingException
import const_definition

#insert loading from json file

class Options:
    '''options that will be used throughout the program
    '''
    def __init__(self):
        #change it, maybe put "" and -1 as default then when printing if -1 or void print "Not Set"
        self.victim=""
        self.webPort=-1
        self.uri=""
        self.httpMethod= -1
        self.myIP=""
        self.myPort=-1
        self.mongoUn=""
        self.mongoPw=""
        self.mongoPort=27017
        self.mongoWebPort=28017
        self.payload={} #will be used in POST
        #MONGOwebport changes are not implemented, we first have to look at what is useful to
        
    def setOptionsRemoteMongo(self):
        m="Enter port, return for default port (27017)"
        tmpPort = Logger.logRequest(m)
        if tmpPort: self.mongoPort = tmpPort
        m= "Does the database server need credentials? "
        srvNeedCreds=Logger.logRequest(m)
        if not srvNeedCreds or srvNeedCreds == "y" or srvNeedCreds == "Y":
            #ask for username and password
            self.mongoUn = Logger.logRequest("Enter server username: ")
            self.mongoPw = Logger.logRequest("Enter server password: ")
            ack="Username set to %s password to %s" %(self.mongoUn, self.mongoPw)
            Logger.info(ack)
        elif srvNeedCreds == "n" or srvNeedCreds == "N":
            return
        else:
            Logger.error("Invalid choice: y/Y for entering credentials, n/N for no credentials")

    def setInteractiveOptions(self):
        def setSingleInteractiveOption(checker, message, ack):
            '''set a single option'''
            passed=False
            while not passed:
                test = Logger.logRequest(message)
                if checker(test):
                    passed=True
                else:
                    Logger.error("Invalid Parameter")
            Logger.info(ack+test)
            return test
        def setSingleFileOption(checker, item, ack):
            '''Check an option, raise a FileReadingException if option does not comply with instructions'''
            item=item.strip()
            if not checker(item):
                what = ack.split("set")[0].strip()
                Logger.error("Invalid parameter: "+item+"for element "+what)
                raise FileReadingException
            Logger.info(ack+item)
            return item
        select = True
        while select:
            m="\n\n"
            m+= "Options"+"\n"
            vicm = self.victim if self.victim else "Not Set"
            m+= "1-Set target host/IP (Current: %s)\n" %(vicm)
            webPortm = self.webPort if self.webPort!=-1 else "Not Set"
            m+= "2-Set web app port (Current: %s)\n" %(webPortm)
            urim = self.uri if self.uri else "Not Set"
            m+= "3-Set App Path (Current: %s)\n" %(urim)
            methodm = self.httpMethod if self.httpMethod!=-1 else "Not Set"
            m+= "4-Set HTTP Request Method (1 for GET/ 2 for POST) (Current: %s)\n" %(methodm)
            myIpm = self.myIP if self.myIP else "Not Set"
            m+= "5-Set my local Mongo/Shell IP (Current: %s)\n" %(myIpm)
            myPortm = self.myPort if self.myPort!= -1 else "Not Set"
            m+= "6-Set shell listener port (Current: %s)\n" %(myPortm)
            m+= "7-Load options file"+"\n"
            m+= "8-Save options file"+"\n"
            m+= "9-Back to main menu"
            Logger.default(m)

            select = Logger.logRequest("Select an option: ")

            if select == "1":
                self.victim = setSingleInteractiveOption(support.checkVictim,const_definition.victimIntMessage, const_definition.victimAckMessage)

            elif select == "2":
                self.webPort = int(setSingleInteractiveOption(support.checkPort,const_definition.portIntMessage, const_definition.portAckMessage))

            elif select == "3":
                self.uri = setSingleInteractiveOption(support.checkPath,const_definition.uriIntMessage, const_definition.uriAckMessage)

            #NOT IMPLEMENTED YET FOR USE
            elif select == "4":
                    self.httpMethod = int(setSingleInteractiveOption(support.checkMethod, const_definition.methodIntMessage, const_definition.methodAckMessage))
                    if self.httpMethod == 2:
                        self.payload = setSingleInteractiveOption(support.checkPOST, const_definition.contentPOSTIntMessage, const_definition.contentPOSTAckMessage)


            elif select == "5":
                    self.myIP = setSingleInteractiveOption(support.checkIP, const_definition.myIPIntMessage, const_definition.myIPAckMessage)

            elif select == "6":
                    self.myPort = int(setSingleInteractiveOption(support.checkPort, const_definition.myPortIntMessage, const_definition.myPortAckMessage))

            elif select == "7":
                loadPath = setSingleInteractiveOption(support.checkFilePath, const_definition.optionFileIntMessage, const_definition.optionFileAckMessage)
                try:
                    fo = open(loadPath,"r" )
                    csvOpt = fo.read()
                    fo.close()
                    optList = csvOpt.split(",")
                    if len(optList) != 6:
                        raise FileReadingException
                    self.victim = setSingleFileOption(support.checkVictim,optList[0], const_definition.victimAckMessage)
                    self.webPort = int(setSingleFileOption(support.checkPort,optList[1], const_definition.portAckMessage))
                    self.uri = setSingleFileOption(support.checkPath,optList[2], const_definition.uriAckMessage)
                    self.httpMethod = int(setSingleFileOption(support.checkMethod,optList[3], const_definition.methodAckMessage))
                    self.myIP = setSingleFileOption(support.checkIP,optList[4], const_definition.myIPAckMessage)
                    self.myPort = int(setSingleFileOption(support.checkPort,optList[5], const_definition.myPortAckMessage))
                except IOError:
                    Logger.error("Couldn't load options file")
                except FileReadingException:
                    Logger.error("Error while parsing the file, check it")

            elif select == "8":
                gotit=False
                while not gotit:
                    savePath = raw_input("Enter file name to save: ")
                    try:
                        with open(savePath):
                            ans=raw_input("File already exists, overwrite? ")
                            if ans=="y" or ans == "Y":
                                gotit=True
                    except IOError:
                        gotit=True
                try:
                    fo = open(savePath, "wb")
                    fo.write(str(self.victim) + "," + str(self.webPort) + "," + str(self.uri) + "," + str(self.httpMethod) + "," + str(self.myIP) + "," + str(self.myPort))
                    fo.close()
                    print "Options file saved!"
                except IOError:
                    print "Couldn't save options file."
            elif select == "9":
                return

    def minRequirementsForNetAttack(self):
        '''check if victim is set, only req for net attack'''
        if len(self.victim)>0:
            return True
        else:
            return False
    def minRequirementsForWebApps(self):
        '''check if victim is set, only req for web app (uri can also be null in case of a post)'''
        if len(self.victim)>0:
            return True
        else:
            return False
