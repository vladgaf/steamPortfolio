from functools import reduce

def listToStr(list, sep = ', '):
    return reduce(lambda x, y: str(x) + sep + str(y), list)