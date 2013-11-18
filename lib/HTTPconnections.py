import requests
from exceptions import ConnectionError

def testConnection(options):
    funcs = {1: requests.get,
            2: requests.post}
    appUrl = "http://%s:%s%s"%(options.victim, options.webPort, options.uri)
    try:
        res = funcs[options.httpMethod](appUrl, data=options.payload)
    except requests.exceptions.ConnectionError:
        raise ConnectionError
    return res
