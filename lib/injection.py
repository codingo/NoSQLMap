import Logger
import injStrings


class InjectionManager:
    AvailableTests={
            1: "BaselineTestEnterRandomString",
            2: "mongoPHPNotEqualAssociativeArray",
            #ADD OTHER TESTS AS SOON AS WE COPY THEM FROM THE MAIN
            }


    def BaselineTestEnterRandomString():
        Logger.info("Testing BaselineTestEnterRandomString")
        for injectSize in xrange(5,31,5):
            for form in injStrings.formatAvailables:
                injectString = injStrings.randInjString(injectSize, form)
                m="Using  %s for injection testing" %(injectString)
                Logger.info(m)
                #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
                #Add error handling for Non-200 HTTP response codes if random strings freaks out the app.


                #CANT WORK RIGHT NOW
                randomUri = buildUri(appURL,injectString)
                randLength = int(len(urllib.urlopen(randomUri).read()))
                print "Got response length of " + str(randLength) + "."
                
                randNormDelta = abs(normLength - randLength)
                
                if randNormDelta == 0:
                    print "No change in response size injecting a random parameter..\n"
                else:
                    print "HTTP response varied " + str(randNormDelta) + " bytes with random parameter value!\n"


    def mongoPHPNotEqualAssociativeArray():
        print "Testing Mongo PHP not equals associative array injection using " + neqUri +"..."
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
