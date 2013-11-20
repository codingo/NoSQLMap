import urllib
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
            self.payload = params[1]
        except ValueError:
            self.payload=options.payload

    def buildUri(self):
        if self.method==1:
            return self.baseUrl+self.payload
        else:
            return self.baseUrl

    def testConnection(self):
        try:
            res = self.method(self.appUrl, self.payload)
            self.appUrl=res.url
        except requests.exceptions.ConnectionError:
            raise ConnectionError
        return res

    def checkLengthHTTPResponse(options):
        '''do connection and return its length'''
        pass
