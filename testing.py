def testing(method, inpu, ass):
    res = method(inpu)
    print "Testing " + method.__name__ + " with input " + str(inpu) + " Result: " + str(res)
    assert ass == res

def testUnit():
    import support
    testing(support.checkIP,"1.1.1.1", True)
    testing(support.checkIP,"-1.1.1.1", False)
    testing(support.checkIP,"1.1.1", False)
    testing(support.checkIP,"1.a.1.1", False)
    testing(support.checkIP,"", False)
    testing(support.checkPort,"a", False)
    testing(support.checkPort,"-12", False)
    testing(support.checkPort,"", False)
    testing(support.checkPort,"80", True)
    testing(support.checkPath,"", True)
    testing(support.checkPath,"/assf%66", True)
    testing(support.checkPath,"/asdgfh%pp", False)
    testing(support.checkPath,"/^ ", False)
    testing(support.checkMethod,"1", True)
    testing(support.checkMethod,"-1", False)
    testing(support.checkMethod,"a", False)
    testing(support.checkMethod,"", False)
