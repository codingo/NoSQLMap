#!/usr/bin/python
# NoSQLMap Copyright 2012-2017 NoSQLMap Development team
# See the file 'doc/COPYING' for copying permission


from exception import NoSQLMapException
import ipcalc
import nsmmongo
import nsmcouch

def args():
    return []

def massScan(platform, args = None):
    yes_tag = ['y', 'Y']
    no_tag = ['n', 'N']
    optCheck = True
    loadCheck = False
    ping = False
    success = []
    versions = []
    creds = []
    commError = []
    ipList = []
    resultSet = []

    print "\n"
    print platform + " Default Access Scanner"
    print "=============================="
    print "1-Scan a subnet for default " + platform + " access"
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
            except NoSQLMapException:
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
                except NoSQLMapException:
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

        if platform == "MongoDB":
            result = nsmmongo.mongoScan(target.rstrip(),27017,ping)

        elif platform == "CouchDB":
            result = nsmcouch.couchScan(target.rstrip(),5984,ping)

        if result[0] == 0:
            print "Successful default access on " + target.rstrip() + "(" + platform + " Version: " + result[1] + ")."
            success.append(target.rstrip())
            versions.append(result[1])

        elif result[0] == 1:
            print platform + " running but credentials required on " + target.rstrip() + "."
            creds.append(target.rstrip()) # Future use

        elif result[0] == 2:
            print "Successful " + platform + " connection to " + target.rstrip() + " but error executing command."
            commError.append(target.rstrip()) # Future use

        elif result[0] == 3:
            print "Couldn't connect to " + target.rstrip() + "."

        elif result[0] == 4:
            print target.rstrip() + " didn't respond to ping."


    print "\n\n"
    select = True
    while select:
        saveEm = raw_input("Save scan results to CSV? (y/n):")

        if saveEm in yes_tag:
            savePath = raw_input("Enter file name to save: ")
            outCounter = 0
            try:
                fo = open(savePath, "wb")
                fo.write("IP Address," + platform + " Version\n")

                for server in success:
                    fo.write(server + "," + versions[outCounter] + "\n" )
                    outCounter += 1

                fo.close()
                print "Scan results saved!"
                select = False

            except NoSQLMapException:
                print "Couldn't save scan results."

        elif saveEm in no_tag:
            select = False

        else:
            select = True

    print "Discovered " + platform + " Servers with No Auth:"
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
            return None

        elif select.isdigit() == True and int(select) <= outCounter:
            victim = success[int(select) - 1]
            resultSet[0] = True
            resultSet[1] = victim
            raw_input("New target set! Press enter to return to the main menu.")
            return resultSet

        else:
            raw_input("Invalid selection.")
