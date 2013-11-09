import json
import log
#change print into log.logging
#set level of notifications
#logging take as parameter the level of notification

class Options:
    '''options that will be used throughout the program, defaults:
        - strings = ""
        - number = -1
    '''
    def __init__(self):
        self.victim=""
        self.webPort=-1
        self.uri=""
        self.httpMethod=-1
        self.myIP=""
        self.myPort=-1

    def setSingleOption(self, item, message, ack):
        '''set a single option'''
        item = log.log_request(message)
        log.logging(ack+item)

    def setOptions(self):
        select = True
        while select:
            print "\n\n"
            print "Options"
            print "1-Set target host/IP (Current: " + str(self.victim) + ")"
            print "2-Set web app port (Current: " + str(self.webPort) + ")"
            print "3-Set App Path (Current: " + str(self.uri) + ")"
            print "4-Set HTTP Request Method (GET/POST)"
            print "5-Set my local Mongo/Shell IP (Current: " + str(self.myIP) + ")"
            print "6-Set shell listener port (Current: " + str(self.myPort) + ")"
            print "7-Load options file"
            print "8-Save options file"
            print "9-Back to main menu"

            select = raw_input("Select an option: ")

            if select == "1":
                self.setSingleOption(self.victim, "Enter the host IP/DNS name: ", "Target set to ")

            elif select == "2":
                self.setSingleOption(self.webPort, "Enter the HTTP port for web apps: ", "HTTP port set to ")

            elif select == "3":
                self.setSingleOption(self.webPort, "Enter URI Path (Press enter for no URI): ", "URI Path set to ")

            #NOT IMPLEMENTED YET FOR USE
            elif select == "4":
                httpMethod = True
                while httpMethod:
                    print "1-Send request as a GET"
                    print "2-Send request as a POST"
                    httpMethod = raw_input("Select an option: ")

                    if httpMethod == "1":
                        print "GET request set"
                        self.httpMethod = 1

                    elif httpMethod == "2":
                        print "POST request set"
                        self.httpMethod = 2

                    else:
                        print "Invalid selection"

            elif select == "5":
                myIP = raw_input("Enter host IP for my Mongo/Shells: ")
                print "Shell IP set to " + myIP + "\n"

            elif select == "6":
                myPort = raw_input("Enter TCP listener for shells: ")
                print "Shell TCP listener set to " + myPort + "\n"

            elif select == "7":
                loadPath = raw_input("enter file name to load: ")
                try:
                    #changing to json format
                    fo = open(loadPath,"r" )
                    csvOpt = fo.read()
                    fo.close()
                    optList = csvOpt.split(",")
                    victim = optList[0]
                    webPort = optList[1]
                    uri = optList[2]
                    httpMethod = optList[3]
                    myIp = optList[4]
                    myPort = optList[5]

                except IOError, e:
                    print "Couldn't load options file! "+e

            elif select == "9":
                return
