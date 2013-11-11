# -*- coding: UTF-8 -*-


class Logger :
    ''' Handles logging of debugging and error messages. '''

    DEBUG = 5
    INFO  = 4
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

    def __init__( self ) :
        Logger._level = Logger.DEBUG

    @classmethod
    def isLevel( cls, level ) :
        return cls._level >= level

    @classmethod
    def debug( cls, message ) :
        if cls.isLevel( Logger.DEBUG ) :
            print Logger.COLHEADER+"DEBUG:  " + message + Logger.COLENDC

    @classmethod
    def info( cls, message ) :
        if cls.isLevel( Logger.INFO ) :
            print Logger.COLINFO+"INFO :  " + message + Logger.COLENDC

    @classmethod
    def warn( cls, message ) :
        if cls.isLevel( Logger.WARN ) :
            print Logger.COLWARNING+"WARN :  " + message + Logger.COLENDC

    @classmethod
    def error( cls, message ) :
        if cls.isLevel( Logger.ERROR ) :
            print Logger.COLFAIL+"ERROR:  " + message + Logger.COLENDC

    @classmethod
    def fatal( cls, message ) :
        if cls.isLevel( Logger.FATAL ) :
            print Logger.COLFAIL+"FATAL:  " + message + Logger.COLENDC

    @classmethod
    def default(cls, message):
        print message

    @classmethod
    def logRequest(cls, message):
        m=Logger.COLHEADER + message + Logger.COLENDC
        return raw_input(m)

