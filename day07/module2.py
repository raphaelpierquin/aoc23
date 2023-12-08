import more_itertools

cards = "AKQXT98765432J"
rcards = ''.join(list(reversed(cards))) + "_ _ _ _ _ "

#5 -> 6
#4 -> 5
#32 -> 4
#3  -> 3
#22 -> 2
#2 -> 1

def comb(jokers,values):
    i = 0
    if values == []:
        values = [jokers]
        jokers = 0
    if max(values) + jokers >= 5:
        return 6
    elif max(values) + jokers == 4:
        return 5
    if 3 in values and 2 in values :
        return 4
    count = 0
    for v in values:
        if v == 2:
            count+=1
    if count==2:
        return 2 + 2*jokers
    elif count==1:
        return 1 + 2*jokers
    if max(values) + jokers == 3 :
        return 3
    if jokers:
        return jokers
    if 1 in values and jokers ==1 :
        return 1
    return 0

def value(hand):
    r = 0
    for i,c in enumerate(hand):
        r = r * 100 + (14 - cards.index(c))
    h = more_itertools.map_reduce(hand,lambda c: 14 - cards.index(c),lambda x:1, sum)
    if 1 in h:
        jokers = h.pop(1)
    else:
        jokers = 0
    return r+ pow(100,5)*comb(jokers,list(h.values()))

def compare(hand1,hand2):
    return value(hand1) - value(hand2)

def bigger(hand1,hand2):
    return value(hand1) > value(hand2)

def test_value():
    #                         X0102030405
    assert value("22222") ==  60202020202
    assert value("JJJJJ") ==  60101010101
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
#5 -> 6
    assert comb(0,[5]) == 6
    assert comb(1,[4]) == 6
    assert comb(2,[3]) == 6
    assert comb(3,[2]) == 6
    assert comb(4,[1]) == 6
    assert comb(5,[]) == 6

#4 -> 5
    assert comb(0,[4]) == 5
    assert comb(1,[3]) == 5
    assert comb(2,[2]) == 5
    assert comb(3,[1]) == 5

#32 -> 4
    assert comb(0,[3,2]) == 4
    assert comb(1,[2,2]) == 4

#3  -> 3
    assert comb(0,[3]) == 3
    assert comb(1,[2]) == 3
    assert comb(2,[1]) == 3

#22 -> 2
    assert comb(0,[2,2]) == 2
    assert comb(1,[2,1]) == 3

#2 -> 1
    assert comb(0,[2]) == 1
    assert comb(1,[1]) == 1

#1
    assert comb(0,[1]) == 0


cards = "AKQXT98765432J"

def plain_compare(hand1,hand2):
    i1, i2 = more_itertools.first_true(zip(map(cards.index,hand1), map(cards.index,hand2)))
    if i1 < i2:
        return hand1
    else:
        return hand2

def test_plain_compare():
    assert plain_compare("AAAAA","KAAAA") == "AAAAA"

