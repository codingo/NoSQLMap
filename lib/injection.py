import Logger
import injStrings
import copy

class InjectionManager:
    AvailableTests={
            1: "BaselineTestEnterRandomString",
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
        self.possibleVuln=[]
        self.sureVuln=[]

    def __performInjection(self, injParam)
        def testWorking(injLength, normLength):
            if injLength == normLength:
                Logger.error("Injection Failed")
                return False
            else:
                Logger.success("Injection succedeed")
                return True
        tmpDic = copy.deepcopy(self.dictOfParams)
        tmpDic[params]=injectString
        connParams = self.conn.buildUri(tmpDic)
        code, length = self.conn.doConnection(connParams)
        if code != 200: #if no good answer pass to successive test
            return False
        m="Got response length of %s" %(length)
        Logger.info(m)
        return testWorking(length, self.standardLength)



    def BaselineTestEnterRandomString(self):
        Logger.info("Testing BaselineTestEnterRandomString")
        for params in self.testingParams:
            for injectSize in xrange(5,31,7):
                for form in injStrings.formatAvailables:
                    injectString = injStrings.randInjString(injectSize, form)
                    m="Using  %s for injection testing" %(injectString)
                    Logger.info(m)
                    #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
                    #Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
                    if self.__performInjection(injectString):
                        sureVuln.append(connParams)

    def mongoPHPNotEqualAssociativeArray(self):
        Logger.info("Testing Mongo PHP not equals associative array injection")

        for params in self.testingParams:
            for injectSize in xrange(5,31,7):
                for form in injStrings.formatAvailables:
                    injectString = injStrings.createNeqString(injectSize, form)
                    m="using %s for injection testing" %(injectString)
                    Logger.info(m)
                    if self.__performInjection(injectString):
                        sureVuln.append(connParams)

    def mongoWhereInjection(self):
        Logger.info("Testing Mongo <2.4 $where all Javascript escape attack")
        basic = injStrings.createWhereStrString()
        for params in self.testingParams:
            try:
                while 1:
                    injectString = next(basic)
                    m="using %s for injection testing" %(injectString)
                    Logger.info(m)
                    if self.__performInjection(injectString):
                        sureVuln.append(connParams)
            except StopIteration:
                continue
        
