import urllib
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
        try: #GET
            param = urlparse.parse_qs(params[1])
        except IndexError: #POST
            param=urlparse.parse_qs(options.payload)
        pars = {}
        for el in param:
            if len(param[el]) == 1:
                pars[el] = param[el][0]
            else:
                pars[el] = param[el][:]
        self.payload= pars
        print self.payload


    def buildUri(self, dictOfParams):
        tmpPay = urllib.urlencode(dictOfParams)
        if self.method==1:
            return (self.baseUrl+"?"+tmpPay,)
        else:
            return (self.baseUrl, tmpPay)

    def doConnection(self, tup):
        try:
            if self.method==1:
                con =  urllib2.urlopen(tup[0])
                print tup[0]
            else:
                print tup[0]
                print tup[1]
                con = urllib2.urlopen(tup[0], data=tup[1])
            cod = con.getcode()
            res = con.read()
        except urllib2.URLError:
            raise ConnectionError
        return cod,len(res)

