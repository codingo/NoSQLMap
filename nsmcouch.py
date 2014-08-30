#!/usr/bin/python

import couchdb


def couchScan(target,port,pingIt):
    if pingIt == True:
        test = os.system("ping -c 1 -n -W 1 " + ip + ">/dev/null")

        if test == 0:	
            try:
                conn = couchdb.Server("http://" + str(target) + ":5984/")

                try:
                    dbVer = conn.version()
                    return [0,dbVer]
                
                except couchdb.http.Unauthorized:
                    return [1,None]

                except Exception, e:
                    print e
                    return [2,None]

            except Exception, e:
                print e
                return [3,None]

        else:
            return [4,None]

    else:
        try:
            conn = couchdb.Server("http://" + str(target) + ":5984/")
            print target #debug
            

            try:
                print str(conn) #debug
                dbVer = conn.version()
                return [0,dbVer]
            
            except couchdb.http.Unauthorized:
                return [1,None]

            except Exception, e:
                print e
                return [2,None]

        except Exception, e:
            print e
            return [3,None]