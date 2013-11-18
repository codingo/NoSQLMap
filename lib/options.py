# -*- coding: UTF-8 -*-

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
        self.victim="Not Set"
        self.webPort=80
        self.uri="Not Set"
        self.httpMethod= "Not Set"
        self.myIP="Not Set"
        self.myPort="Not Set"

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
                Logger.error("Invalid parameter: "+item)
                raise FileReadingException
            Logger.info(ack+item)
            return item
        select = True
        while select:
            m="\n\n"
            m+= "Options"+"\n"
            m+= "1-Set target host/IP (Current: " + str(self.victim) + ")"+"\n"
            m+= "2-Set web app port (Current: " + str(self.webPort) + ")"+"\n"
            m+= "3-Set App Path (Current: " + str(self.uri) + ")"+"\n"
            m+= "4-Set HTTP Request Method (1 for GET/ 2 for POST) "+"(Current: "+str(self.httpMethod)+")"+"\n"
            m+= "5-Set my local Mongo/Shell IP (Current: " + str(self.myIP) + ")"+"\n"
            m+= "6-Set shell listener port (Current: " + str(self.myPort) + ")"+"\n"
            m+= "7-Load options file"+"\n"
            m+= "8-Save options file"+"\n"
            m+= "9-Back to main menu"
            Logger.default(m)

            select = Logger.logRequest("Select an option: ")

            if select == "1":
                self.victim = setSingleInteractiveOption(support.checkVictim,const_definition.victimIntMessage, const_definition.victimAckMessage)

            elif select == "2":
                self.webPort = setSingleInteractiveOption(support.checkPort,const_definition.portIntMessage, const_definition.portAckMessage)

            elif select == "3":
                self.uri = setSingleInteractiveOption(support.checkPath,const_definition.uriIntMessage, const_definition.uriAckMessage)

            #NOT IMPLEMENTED YET FOR USE
            elif select == "4":
                    self.httpMethod = setSingleInteractiveOption(support.checkMethod, const_definition.methodIntMessage, const_definition.methodAckMessage)

            elif select == "5":
                    self.myIP = setSingleInteractiveOption(support.checkIP, const_definition.myIPIntMessage, const_definition.myIPAckMessage)

            elif select == "6":
                    self.myPort = setSingleInteractiveOption(support.checkPort, const_definition.myPortIntMessage, const_definition.myPortAckMessage)

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
                    self.webPort = setSingleFileOption(support.checkPort,optList[1], const_definition.portAckMessage)
                    self.uri = setSingleFileOption(support.checkPath,optList[2], const_definition.uriAckMessage)
                    self.httpMethod = setSingleFileOption(support.checkMethod,optList[3], const_definition.methodAckMessage)
                    self.myIP = setSingleFileOption(support.checkIP,optList[4], const_definition.myIPAckMessage)
                    self.myPort = setSingleFileOption(support.checkPort,optList[5], const_definition.myPortAckMessage)
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
