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


'''support library for checking and other stuff'''

import string
import os.path
import urlparse

def checkIP(ip):
    '''ip check: must be 4 octets, each <256'''
    try:
        ip = ip.strip().split(".")
    except AttributeError:
        return False
    try:
        return len(ip) == 4 and all(octet.isdigit() and int(octet) < 256 for octet in ip)
    except ValueError:
        return False

def checkPOST(st):
    try:
        urlparse.parse_qs(st)
    except:
        return False
    return st

def checkPort(port):
    '''port must be 0<x<65536'''
    try:
        port = int(port)
    except ValueError:
        return False
    return port > 0 and port < 65536

def checkURL(url):
    '''everything can be a valid url!!'''
    return True

def checkVictim(p):
    '''sum of ip +url, right now will only do the ip'''
    if checkIP(p):
        return True
    else:
        if checkURL(p):
            return True
    return False


def checkPath(path):
    '''character allowed in path are a finite set + urlencoding'''
    #range A–Z, a–z, 0–9, -, ., _, ~, !, $, &, ', (, ), *, +, ,, ;, =, :, @, %+twohexdigits
    allowedChars=list(string.letters) + list(string.digits)+['/','-','.','_','~','!','$','&',"'",'(',')','*','+',',',';','=',':','@','%','?']
    if any(c not in allowedChars for c in path):
        return False
    for pos in [i for i, ltr in enumerate(path) if ltr == '%']:
        if path[pos+1] not in string.hexdigits or path[pos+2] not in string.hexdigits:
            return False
    return True

def checkMethod(method):
    '''get with 1, post with 2'''
    try:
        method=int(method)
    except ValueError:
        return False
    return method==1 or method == 2

def checkFilePath(path):
    '''check if file does exist'''
    try:
        with open(path):
            return True
    except IOError:
        return False
