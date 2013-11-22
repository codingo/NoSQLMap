import Logger
import injStrings
import copy

class InjectionManager:
    AvailableTests={
            1: "BaselineTestEnterRandomString",
            2: "mongoPHPNotEqualAssociativeArray",
            #ADD OTHER TESTS AS SOON AS WE COPY THEM FROM THE MAIN
            }


    def __init__(self, connection, standard_length):
        self.conn = connection
        self.dictOfParams = connection.payload
        self.standardLength = standard_length
        self.possibleVuln=[]
        self.sureVuln=[]

    def BaselineTestEnterRandomString(self):
        Logger.info("Testing BaselineTestEnterRandomString")
        for params in self.dictOfParams:
            for injectSize in xrange(5,31,7):
                for form in injStrings.formatAvailables:
                    tmpDic = copy.deepcopy(self.dictOfParams)
                    injectString = injStrings.randInjString(injectSize, form)
                    m="Using  %s for injection testing" %(injectString)
                    Logger.info(m)
                    #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
                    #Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
                    
                    tmpDic[params]=injectString
                    connParams = self.conn.buildUri(tmpDic)
                    code, length = self.conn.doConnection(connParams)
                    if code != 200: #if no good answer pass to successive test
                        continue
                    m="Got response length of %s" %(length)
                    Logger.info(m)

                    randNormDelta = abs(normLength - randLength)
                    
                    if randNormDelta == 0:
                        Logger.warn("No change in response size injecting a random parameter..")
                    else:
                        m="HTTP response varied %s bytes with random parameter value!" %(randNormDelta)
                        Logger.success(m)
                        sureVuln.append(connParams)


    def mongoPHPNotEqualAssociativeArray(self):
        Logger.info("Testing Mongo PHP not equals associative array injection")
        
            injectString = injStrings.createNeqString()

            m="using %s for injection testing" %(injectString)
        Logger.info(m)

        injLen = int(len(urllib.urlopen(neqUri).read()))
        print "Got response length of " + str(injLen) + "."

        randInjDelta = abs(injLen - randLength)

        if (randInjDelta >= 100) and (injLen != 0) :
            print "Not equals injection response varied " + str(randInjDelta) + " bytes from random parameter value! Injection works!"
            vulnAddrs.append(neqUri)

        elif (randInjDelta > 0) and (randInjDelta < 100) and (injLen != 0) :
            print "Response variance was only " + str(randInjDelta) + " bytes. Injection might have worked but difference is too small to be certain. "
            possAddrs.append(neqUri)

        elif (randInjDelta == 0):
            print "Random string response size and not equals injection were the same. Injection did not work."
        else:
            print "Injected response was smaller than random response.  Injection may have worked but requires verification."
            possAddrs.append(neqUri)
