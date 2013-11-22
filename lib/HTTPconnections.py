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
        except ValueError: #POST
            param=urlparse.parse_qs(options.payload)
        self.payload= param


    def buildUri(self, dictOfParams):
        tmpPay = urllib.urlencode(dictOfParams)
        if self.method==1:
            return (self.baseUrl+"?"+tmpPay,)
        else:
            return (self.baseUrl, tmpPay)

    def doConnection(self, tup):
        try:
            if self.method==1:
                res = urllib2.urlopen(tup[0]).read()
            else:
                res = urllib2.urlopen(tup[0], data=tup[1]).read()
        except urllib2.URLError:
            raise ConnectionError
        return res.getcode(),len(res)

