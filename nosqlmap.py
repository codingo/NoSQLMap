#!/usr/bin/python
#NoSQLMap Copyright 2016 Russell Butturini
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


import sys
import nsmcouch
import nsmmongo
import nsmscan
import nsmweb
import os
import signal
import ast

def main():
    signal.signal(signal.SIGINT, signal_handler)
    global optionSet
    #Set a list so we can track whether options are set or not to avoid resetting them in subsequent calls to the options menu.
    optionSet = [False]*9
    global yes_tag
    global no_tag
    yes_tag = ['y', 'Y']
    no_tag = ['n', 'N']
    global victim
    global webPort
    global uri
    global httpMethod
    global platform
    global https
    global myIP
    global myPort
    global verb
    global scanNeedCreds
    global dbPort
    #Use MongoDB as the default, since it's the least secure ( :-p at you 10Gen )
    platform = "MongoDB"
    dbPort = 27017
    myIP = "Not Set"
    myPort = "Not Set"
    mainMenu()

def mainMenu():
    global platform
    global victim
    global dbPort
    global myIP
    global webPort
    global uri
    global httpMethod
    global https
    global verb
    global requestHeaders
    global postData

    mmSelect = True
    while mmSelect:
        os.system('clear')
        print "===================================================="
        print " _   _       _____  _____ _     ___  ___            "
        print "| \ | |     /  ___||  _  | |    |  \/  |            "
        print "|  \| | ___ \ `--. | | | | |    | .  . | __ _ _ __  "
        print "| . ` |/ _ \ `--. \| | | | |    | |\/| |/ _` | '_ \ "
        print "| |\  | (_) /\__/ /\ \/' / |____| |  | | (_| | |_) |"
        print "\_| \_/\___/\____/  \_/\_\_____/\_|  |_/\__,_| .__/"
        print "===================================================="
        print "NoSQLMap-v0.7"
        print "nosqlmap@gmail.com"
        print "\n"
        print "1-Set options"
        print "2-NoSQL DB Access Attacks"
        print "3-NoSQL Web App attacks"
        print "4-Scan for Anonymous " + platform + " Access"
        print "5-Change Platform (Current: " + platform + ")"
        print "x-Exit"

        select = raw_input("Select an option: ")

        if select == "1":
            options()

        elif select == "2":
            if optionSet[0] == True and optionSet[4] == True:
                if platform == "MongoDB":
                    nsmmongo.netAttacks(victim, dbPort, myIP, myPort)

                elif platform == "CouchDB":
                    nsmcouch.netAttacks(victim, dbPort, myIP)

            #Check minimum required options
            else:
                raw_input("Target not set! Check options.  Press enter to continue...")


        elif select == "3":
            #Check minimum required options
            if (optionSet[0] == True) and (optionSet[2] == True):
                if httpMethod == "GET":
                    nsmweb.getApps(webPort,victim,uri,https,verb,requestHeaders)

                elif httpMethod == "POST":
                    nsmweb.postApps(victim,webPort,uri,https,verb,postData,requestHeaders)

            else:
                raw_input("Options not set! Check host and URI path.  Press enter to continue...")


        elif select == "4":
            scanResult = nsmscan.massScan(platform)

            if scanResult != None:
                optionSet[0] = True
                victim = scanResult[1]

        elif select == "5":
            platSel()

        elif select == "x":
            sys.exit()

        else:
            raw_input("Invalid selection.  Press enter to continue.")

def platSel():
    global platform
    global dbPort
    select = True
    print "\n"

    while select:
        print "1-MongoDB"
        print "2-CouchDB"
        pSel = raw_input("Select a platform: ")

        if pSel == "1":
            platform = "MongoDB"
            dbPort = 27017
            return

        elif pSel == "2":
            platform = "CouchDB"
            dbPort = 5984
            return
        else:
            raw_input("Invalid selection.  Press enter to continue.")

def options():
    global victim
    global webPort
    global uri
    global https
    global platform
    global httpMethod
    global postData
    global myIP
    global myPort
    global verb
    global mmSelect
    global dbPort
    global requestHeaders
    requestHeaders = {}
    optSelect = True

    #Set default value if needed
    if optionSet[0] == False:
        global victim
        victim = "Not Set"
    if optionSet[1] == False:
        global webPort
        webPort = 80
        optionSet[1] = True
    if optionSet[2] == False:
        global uri
        uri = "Not Set"
    if optionSet[3] == False:
        global httpMethod
        httpMethod = "GET"
    if optionSet[4] == False:
        global myIP
        myIP = "Not Set"
    if optionSet[5] == False:
        global myPort
        myPort = "Not Set"
    if optionSet[6] == False:
        verb = "OFF"
        optSelect = True
    if optionSet[8] == False:
        https = "OFF"
        optSelect = True

    while optSelect:
        print "\n\n"
        print "Options"
        print "1-Set target host/IP (Current: " + str(victim) + ")"
        print "2-Set web app port (Current: " + str(webPort) + ")"
        print "3-Set App Path (Current: " + str(uri) + ")"
        print "4-Toggle HTTPS (Current: " + str(https) + ")"
        print "5-Set " + platform + " Port (Current : " + str(dbPort) + ")"
        print "6-Set HTTP Request Method (GET/POST) (Current: " + httpMethod + ")"
        print "7-Set my local " +  platform + "/Shell IP (Current: " + str(myIP) + ")"
        print "8-Set shell listener port (Current: " + str(myPort) + ")"
        print "9-Toggle Verbose Mode: (Current: " + str(verb) + ")"
        print "0-Load options file"
        print "a-Load options from saved Burp request"
        print "b-Save options file"
        print "h-Set headers"
        print "x-Back to main menu"

        select = raw_input("Select an option: ")

        if select == "1":
            #Unset the boolean if it's set since we're setting it again.
            optionSet[0] = False
            ipLen = False

            while optionSet[0] == False:
                goodDigits = True
                notDNS = True
                victim = raw_input("Enter the host IP/DNS name: ")
                #make sure we got a valid IP
                octets = victim.split(".")

                if len(octets) != 4:
                    #Treat this as a DNS name
                    optionSet[0] = True
                    notDNS = False
                else:
                    #If len(octets) != 4 is executed the block of code below is also run, but it is not necessary
                    #If the format of the IP is good, check and make sure the octets are all within acceptable ranges.
                    for item in octets:
                        try:
                            if int(item) < 0 or int(item) > 255:
                                print "Bad octet in IP address."
                                goodDigits = False

                        except:
                            #Must be a DNS name (for now)

                            notDNS = False

                #If everything checks out set the IP and break the loop
                if goodDigits == True or notDNS == False:
                    print "\nTarget set to " + victim + "\n"
                    optionSet[0] = True

        elif select == "2":
            webPort = raw_input("Enter the HTTP port for web apps: ")
            print "\nHTTP port set to " + webPort + "\n"
            optionSet[1] = True

        elif select == "3":
            uri = raw_input("Enter URI Path (Press enter for no URI): ")
            print "\nURI Path set to " + uri + "\n"
            optionSet[2] = True

        elif select == "4":
            if https == "OFF":
                print "HTTPS enabled."
                https = "ON"
                optionSet[8] = True

            elif https == "ON":
                print "HTTPS disabled."
                https = "OFF"
                optionSet[8] = True


        elif select == "5":
            dbPort = int(raw_input("Enter target MongoDB port: "))
            print "\nTarget Mongo Port set to " + str(dbPort) + "\n"
            optionSet[7] = True

        elif select == "6":
            httpMethod = True
            while httpMethod == True:

                print "1-Send request as a GET"
                print "2-Send request as a POST"
                httpMethod = raw_input("Select an option: ")

                if httpMethod == "1":
                    httpMethod = "GET"
                    print "GET request set"
                    requestHeaders = {}
                    optionSet[3] = True

                elif httpMethod == "2":
                    print "POST request set"
                    optionSet[3] = True
                    postDataIn = raw_input("Enter POST data in a comma separated list (i.e. param name 1,value1,param name 2,value2)\n")
                    pdArray = postDataIn.split(",")
                    paramNames = pdArray[0::2]
                    paramValues = pdArray[1::2]
                    postData = dict(zip(paramNames,paramValues))
                    httpMethod = "POST"

                else:
                    print "Invalid selection"

        elif select == "7":
            #Unset the setting boolean since we're setting it again.
            optionSet[4] = False

            while optionSet[4] == False:
                goodLen = False
                goodDigits = True
                #Every time when user input Invalid IP, goodLen and goodDigits should be reset. If this is not done, there will be a bug
                #For example enter 10.0.0.1234 first and the goodLen will be set to True and goodDigits will be set to False
                #Second step enter 10.0.123, because goodLen has already been set to True, this invalid IP will be put in myIP variables
                myIP = raw_input("Enter the host IP for my " + platform +"/Shells: ")
                #make sure we got a valid IP
                octets = myIP.split(".")
                #If there aren't 4 octets, toss an error.
                if len(octets) != 4:
                    print "Invalid IP length."

                else:
                    goodLen = True

                if goodLen == True:
                #If the format of the IP is good, check and make sure the octets are all within acceptable ranges.
                    for item in octets:
                        if int(item) < 0 or int(item) > 255:
                            print "Bad octet in IP address."
                            goodDigits = False

#						else:
#							goodDigits = True
                        #Default value of goodDigits should be set to True
                        #for example 12.12345.12.12


                #If everything checks out set the IP and break the loop
                if goodLen == True and goodDigits == True:
                    print "\nShell/DB listener set to " + myIP + "\n"
                    optionSet[4] = True

        elif select == "8":
            myPort = raw_input("Enter TCP listener for shells: ")
            print "Shell TCP listener set to " + myPort + "\n"
            optionSet[5] = True

        elif select == "9":
            if verb == "OFF":
                print "Verbose output enabled."
                verb = "ON"
                optionSet[6] = True

            elif verb == "ON":
                print "Verbose output disabled."
                verb = "OFF"
                optionSet[6] = True

        elif select == "0":
            loadPath = raw_input("Enter file name to load: ")
            try:
                fo = open(loadPath,"r" )
                csvOpt = fo.readlines()
                fo.close()
                optList = csvOpt[0].split(",")
                victim = optList[0]
                webPort = optList[1]
                uri = optList[2]
                httpMethod = optList[3]
                myIP = optList[4]
                myPort = optList[5]
                verb = optList[6]
                https = optList[7]

                if httpMethod == "POST":
                    postData = ast.literal_eval(csvOpt[1])

                #Set option checking array based on what was loaded
                x = 0
                for item in optList:
                    if item != "Not Set":
                        optionSet[x] = True
                    x += 1
            except:
                print "Couldn't load options file!"

        elif select == "a":
            loadPath = raw_input("Enter path to Burp request file: ")

            try:
                fo = open(loadPath,"r")
                reqData = fo.readlines()

            except:
                raw_input("error reading file.  Press enter to continue...")
                return

            methodPath = reqData[0].split(" ")

            if methodPath[0] == "GET":
                httpMethod = "GET"

            elif methodPath[0] == "POST":
                paramNames = []
                paramValues = []
                httpMethod = "POST"
                postData = reqData[len(reqData)-1]
                #split the POST parameters up into individual items
                paramsNvalues = postData.split("&")

                for item in paramsNvalues:
                    tempList = item.split("=")
                    paramNames.append(tempList[0])
                    paramValues.append(tempList[1])

                postData = dict(zip(paramNames,paramValues))

            else:
                print "unsupported method in request header."

            # load the HTTP headers
            for line in reqData[1:]:
                print(line)
                if not line.strip(): break
                header = line.split(": ");
                requestHeaders[header[0]] = header[1].strip()

            victim = reqData[1].split( " ")[1].replace("\r\n","")
            optionSet[0] = True
            uri = methodPath[1].replace("\r\n","")
            optionSet[2] = True

        elif select == "b":
            savePath = raw_input("Enter file name to save: ")
            try:
                fo = open(savePath, "wb")
                fo.write(str(victim) + "," + str(webPort) + "," + str(uri) + "," + str(httpMethod) + "," + str(myIP) + "," + str(myPort) + "," + verb + "," + https)

                if httpMethod == "POST":
                    fo.write(",\n"+ str(postData))
                fo.write(",\n" + str(requestHeaders) )
                fo.close()
                print "Options file saved!"
            except:
                print "Couldn't save options file."

        elif select == "h":
            reqHeadersIn = raw_input("Enter HTTP Request Header data in a comma separated list (i.e. header name 1,value1,header name 2,value2)\n")
            reqHeadersArray = reqHeadersIn.split(",")
            headerNames = reqHeadersArray[0::2]
            headerValues = reqHeadersArray[1::2]
            requestHeaders = dict(zip(headerNames, headerValues))

        elif select == "x":
            return


def signal_handler(signal, frame):
    print "\n"
    print "CTRL+C detected.  Exiting."
    sys.exit()

if __name__ == '__main__':
    main()
