import urllib2
import urlparse
from exceptions import ConnectionError
"""update: library should use urllib and urlparse
urllib allows for getting a url using urlopen(url, data=payload) data used only for post must be a string
we can obtain a dictionary from a string using urlparse.pase_qs CAREFUL words only on query string, remove everything before ? in GET before calling it
the string can get back from a dictionary using urllib.urlencode
"""

class ConnectionManager:
    
    def __init__(self, options):
        params = options.uri.split("?")
        self.baseUrl = "http://%s:%s%s"%(options.victim, options.webPort, params[0])
        self.method = options.httpMethod
        try:
            #it's a get
            param=urlparse.parse_qs(params[1])
        except ValueError:
            #it's a post
            param=urlparse.parse_qs(options.payload)
        self.payload=param

    def buildUri(self, injection):
        '''create a tuple with 1/2 elems, if 1 then it's a get if 2 it's a post. accept an injection param as a dictionary'''
        inj=urllib2.urlencode(injection)
        if self.method==1:
            return (self.baseUrl+"?"+inj,)
        else:
            return (self.baseUrl,inj)

    def testConnection(self):
        tup=self.buildUri(self.payload) 
        try:
            if self.method==1: #GET
                res=urllib2.urlopen(tup[0]).read()
            else: #POST
                res = urllib2.urlopen(tup[0],data=tup[1]).read()
        except urllib2.URLError:
            raise ConnectionError
        return res

    def checkLengthHTTPResponse(options):
        '''do connection and return its length'''
        pass
