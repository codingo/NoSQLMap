import string

formatAvailables=[1,2,3,4]
def randInjString(size, formatStringString):
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
