from log import Logger
import injStrings
import copy

class InjectionManager:
    AvailableTests={
            1: "baselineTestEnterRandomString",
            2: "mongoPHPNotEqualAssociativeArray",
            3: "mongoWhereInjection",
            #ADD OTHER TESTS AS SOON AS WE COPY THEM FROM THE MAIN
            }
    randInjDelta = 100

    def __init__(self, connection, standard_length,vulnParam=""):
        self.conn = connection
        self.dictOfParams = connection.payload
        if vulnParam:
            self.testingParams=[vulnParam]
        else:
            self.testingParams = connection.payload
        self.standardLength = standard_length
        self.injStringCreator=injStrings.InjectionStringCreator()
        self.possibleVuln=[]
        self.sureVuln=[]
        self.successfulAttacks = {} 
    def removeEqual(tup, injParam):
        l=[]
        for el in tup:
            ele = el
            pos=el.find(injParam)
            stLen=len(injParam)
            if pos != -1 and el[pos+stLen]=="=":
                ele = el[:pos+stLen]+el[pos+stLen+1:]
            l.append(ele)
        return l

    def __addSuccessful(self, suc, funcName):
        if suc:
            self.successfulAttacks[funcName]=True
        else:
            self.successfulAttacks[funcName]=False

    def __performInjection(self, injParam="", injectString="", removeEqual=False, dummyInjection=False):
        def testWorking(injLength, normLength):
            if injLength==0:
                Logger.error("Injection Failed")
                return False
            if injLength > normLength:
                Logger.success("Injection succedeed")
                return True
            else:
                Logger.error("Injection Failed")
                return False
        def removeEqual(tup, injParam):
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
        return testWorking(length, self.standardLength),connParams

    def baselineTestEnterRandomString(self):

        funcName="baselineTestEnterRandomString"
        Logger.info("Testing BaselineTestEnterRandomString")

        for params in self.testingParams:
            for injectString in self.injStringCreator.createIdString():
                m="Using  %s for injection testing" %(injectString)
                Logger.info(m)
                #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
                #Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
                res,connParams=self.__performInjection(params, injectString)
                if res:
                    self.sureVuln.append(connParams)
                    suc=True

        self.__addSuccessful(suc,funcName)

    def mongoPHPNotEqualAssociativeArray(self):

        funcName="mongoPHPNotEqualAssociativeArray"
        Logger.info("Testing Mongo PHP not equals associative array injection")

        for params in self.testingParams:
            for injectString in self.injStringCreator.createNeqString():
                m="using %s for injection testing" %(injectString)
                Logger.info(m)
                res,connParams=self.__performInjection(params, injectString, True)
                if res:
                    self.sureVuln.append(connParams)
                    suc=True
        
        self.__addSuccessful(suc,funcName)

    def mongoWhereInjection(self):

        funcName="mongoWhereInjection"
        Logger.info("Testing Mongo <2.4 $where all Javascript escape attack")
        for params in self.testingParams:
            for injectString in self.injStringCreator.createWhereStrString():
                m="using %s for injection testing" %(injectString)
                Logger.info(m)
                res,connParams=self.__performInjection(params, injectString)
                if res:
                    self.sureVuln.append(connParams)

    def mongoThisNotEqualEscape(self):

        funcName="MongoThisNotEqualEscape"
        Logger.info("Testing Mongo PHP not equals associative array injection")

        for params in self.testingParams:
            for injectString in self.injStringCreator.createBlindNeqString():
                m="using %s for injection testing" %(injectString)
                Logger.info(m)
                res,connParams=self.__performInjection(params, injectString)
                if res:
                    self.sureVuln.append(connParams)

        self.__addSuccessful(suc,funcName)

    def mongoTimeBasedInjection(self):
        #VERY NAIVE IMPLEMENTATION, IMPROVE WITH MORE TESTING

        funcName="mongoTimeBasedInjection"
        Logger.info("Testing time based injection")
        start=time.time()
        res,connParams = self.__performInjection(dummyInjection=True)
        end = time.time()
        for params in self.testingParams:
            for injectString in self.injStringCreator.createTimeString():
                startTest = time.time()
                res,connParams=self.__performInjection(params, injectString)
                endTest = time.time()
        #TIME TESTING PERFORMED LOCALLY TODO: CREATE AN ABSTRACT FACTORY FOR TET WORKING 
                strTimeDelta = (int(round((end - start), 3)) - timeBase)
                if strTimeDelta > 25:
                    m="HTTP load time variance was %s seconds! Injection succeeded" %(strTimeDelta)
                    Logger.success(m)
                    suc=True
                    self.sureVuln.append(connParams)

        self.__addSuccessful(suc,funcName)
