import sys
import itertools
import more_itertools
import re
import math
import module

hands, bids = [],[]

def parseLine(line,n):
    global hands,bids
    print(n,line)
    hand,bid = line.split(" ")
    hands.append(hand)
    bids.append(int(bid))
            
for l, line in enumerate(sys.stdin):
    parseLine(line.rstrip(),l)

r = 0
for hand,order in list(zip((sorted(zip(hands,bids),key=lambda x: module.value(x[0]))),range(1,10000))):
    hand,bid = hand
    r = r + order * bid
print(list(zip(hands,map(module.value,hands))))
#print(list(zip((sorted(zip(hands,bids),key=lambda x: module.value(x[0]))),range(1,10000))))
print(r)
