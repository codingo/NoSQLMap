import Logger
import injStrings

class InjectionManager:
    AvailableTests={
            1: "BaselineTestEnterRandomString",
            #ADD OTHER TESTS AS SOON AS WE COPY THEM FROM THE MAIN
            }


    def BaselineTestEnterRandomString():
        Logger.info("Testing BaselineTestEnterRandomString")
        for injectSize in xrange(5,31,5):
            for form in injStrings.formatAvailables:
                injectString = injStrings.randInjString(injectSize, form)
                m="Using  %s for injection testing.\n"
                Logger.info(m)
                #Build a random string and insert; if the app handles input correctly, a random string and injected code should be treated the same.
                #Add error handling for Non-200 HTTP response codes if random strings freaks out the app.
                randomUri = buildUri(appURL,injectString)
                print "Checking random injected parameter HTTP response size using " + randomUri +"...\n"
                randLength = int(len(urllib.urlopen(randomUri).read()))
                print "Got response length of " + str(randLength) + "."
                
                randNormDelta = abs(normLength - randLength)
                
                if randNormDelta == 0:
                    print "No change in response size injecting a random parameter..\n"
                else:
                    print "HTTP response varied " + str(randNormDelta) + " bytes with random parameter value!\n"
