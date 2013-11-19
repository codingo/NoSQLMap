import requests
from exceptions import ConnectionError


class ConnectionManager:
    funcs = {1: requests.get,
    2: requests.post}
    
    def __init__(self, options):
        self.appUrl = "http://%s:%s%s"%(options.victim, options.webPort, options.uri)
        self.method = funcs[options.httpMethod]
        self.payload = options.payload

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
