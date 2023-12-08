import more_itertools

cards = "AKQJT98765432"
rcards = ''.join(list(reversed(cards))) + "_ _ _ _ _ "

#5 -> 6
#4 -> 5
#32 -> 4
#3  -> 3
#22 -> 2
#2 -> 1
def comb(values):
    values= list(values)
    i = 0
    if 5 in values:
        return 6
    elif 4 in values:
        return 5
    if 3 in values and 2 in values:
        return 4
    if 3 in values:
        return 3
    count = 0
    for v in values:
        if v == 2:
            count+=1
    if count==2:
        return 2
    elif count==1:
        return 1
    return 0

def value(hand):
    r = 0
    for i,c in enumerate(hand):
        r = r * 100 + (14 - cards.index(c))
    values  = more_itertools.map_reduce(hand,lambda c: 14 - cards.index(c),lambda x:1, sum).values()
    return r+ pow(100,5)*comb(values)

def bigger(hand1,hand2):
    return value(hand1) > value(hand2)

def test_value():
    #                         X0102030405
    assert value("22222") ==  60202020202
    assert value("AAAAA") ==  61414141414
    assert value("AAAA2") ==  51414141402
    assert value("AAAAA") ==  61414141414
    assert value("23456") ==    203040506
    assert value("42233") ==  20402020303
    assert value("42533") ==  10402050303
    assert value("44333") ==  40404030303

def test_bigger():
    assert bigger("22222","A2222")
    assert bigger("AAAA2","A2222")
    assert bigger("33224","22334")
    assert bigger("33322","333A2")

def test_comb():
    assert comb([5]) == 6
    assert comb([4]) == 5
    assert comb([3,2]) == 4
    assert comb([3]) == 3
    assert comb([2,2]) == 2
    assert comb([2]) == 1

