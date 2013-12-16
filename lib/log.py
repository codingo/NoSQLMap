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


class Logger :
    ''' Handles logging of debugging and error messages. '''

    DEBUG = 6
    INFO  = 5
    SUCCESS = 4
    WARN  = 3
    ERROR = 2
    FATAL = 1
    COLHEADER = '\033[95m' #PINK
    COLINFO = '\033[94m'   #BLUE
    COLDONE = '\033[92m'   #GREEN
    COLWARNING = '\033[93m' #YELLOW
    COLFAIL = '\033[91m'   #RED
    COLENDC = '\033[0m'    #ENDCOLOR
    _level = DEBUG

    def __init__(self) :
        Logger._level = Logger.DEBUG

    @classmethod
    def isLevel(cls, level) :
        return cls._level >= level

    @classmethod
    def success(cls, message) :
        if cls.isLevel(Logger.SUCCESS) :
            print Logger.COLDONE + "SUCCESS:  " + message + Logger.COLENDC

    @classmethod
    def debug(cls, message) :
        if cls.isLevel(Logger.DEBUG) :
            print Logger.COLHEADER + "DEBUG:  " + message + Logger.COLENDC

    @classmethod
    def info(cls, message) :
        if cls.isLevel(Logger.INFO) :
            print Logger.COLINFO+"INFO :  " + message + Logger.COLENDC

    @classmethod
    def warn(cls, message) :
        if cls.isLevel(Logger.WARN) :
            print Logger.COLWARNING + "WARN :  " + message + Logger.COLENDC

    @classmethod
    def error(cls, message) :
        if cls.isLevel(Logger.ERROR) :
            print Logger.COLFAIL + "ERROR:  " + message + Logger.COLENDC

    @classmethod
    def fatal(cls, message) :
        if cls.isLevel(Logger.FATAL) :
            print Logger.COLFAIL + "FATAL:  " + message + Logger.COLENDC

    @classmethod
    def default(cls, message):
        print message

    @classmethod
    def logRequest(cls, message):
        m = Logger.COLHEADER + message + Logger.COLENDC
        return raw_input(m)
