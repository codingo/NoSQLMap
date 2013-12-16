#!/usr/bin/python
# -*- coding: UTF-8 -*-

#NoSQLMap Copyright 2013 Russell Butturini
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

import urllib
import urllib2
import urlparse
from exceptions import ConnectionError

class ConnectionManager:
    """ 
    This class provides the interface for creating an HTTP connection. 
    """    
    def __init__(self, options):
        """
        initialize the connection object. Takes as input an option object (see options.py)
        and set paramethers, methods and base url according to the options given.
        """

        params = options.uri.split("?")
        self.baseUrl = "http://%s:%s%s" % (options.victim, options.webPort, params[0])
        self.method = options.httpMethod
        try: #GET
            param = urlparse.parse_qs(params[1])
        except IndexError: #POST
            param = urlparse.parse_qs(options.payload)
        pars = {}
        for el in param:
            if len(param[el]) == 1:
                pars[el] = param[el][0]
            else:
                pars[el] = param[el][:]
        self.payload = pars

    def buildUri(self, dictOfParams):
        """
        takes as input a dictionary in the form {"nameParameter": "valueParameter"} and build an URL according to the dictionary.
        Always use this method before creating a connection.
        Return a list.
        The first element is a URL.
        The second element (optional) is the payolad for a POST. This is returned only if method is a POST.
        """

        tmpPay = urllib.urlencode(dictOfParams)
        if self.method == 1:
            return [self.baseUrl + "?" + tmpPay]
        else:
            return [self.baseUrl, tmpPay]

    def doConnection(self, tup):
        """
        Takes as input an iterable, currently composed by 1 or 2 parameters.
        Do a request to the url specified as first parameter in the iterable (optionally using second as payload if method is a post).
        Returns HTTP status code and length of the response.
        Raise a ConnectionError if something goes wrong.
        """
        try:
            if self.method == 1:
                con = urllib2.urlopen(tup[0])
                print tup[0]
            else:
                print tup[0]
                print tup[1]
                con = urllib2.urlopen(tup[0], data=tup[1])
            cod = con.getcode()
            res = con.read()
        except urllib2.URLError:
            raise ConnectionError
        return cod, len(res)

    def checkVulnParam(self, param):
        """
        Take as input a string, a parameter, and check if it's present (as key) in the dictionary of parameters passed during the initialization
        Return True if present.
        """
        return param in self.payload
