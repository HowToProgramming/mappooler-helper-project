convertedtoken = 161852596426573538808593526471880393572430666572
def dectohex(num):
    h = ""
    while num != 0:
        r = num % 16
        if r <= 9:
            h = str(r) + h
        else:
            h = chr(87 + r) + h
        num //= 16
    return h
token = dectohex(convertedtoken)