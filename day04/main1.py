import sys
import itertools
import more_itertools
import re

DIGITS = re.compile('\d+')

cards = []

def value(card):
    winning, having = card
    count = len(list(filter(lambda x: x in winning, having)))
    if count == 0:
        return 0
    return pow(2,count-1)

def parseRaw(cards):
    numbers = []
    for m in DIGITS.finditer(cards):
        numbers.append(int(m.group()))
    return numbers

def parseLine(line,n):
    print(n,line)

    winning, having = map(parseRaw,line.split(":")[1].split("|"))
    return (winning,having)

for l, line in enumerate(sys.stdin):
    cards.append(parseLine(line.rstrip(),l))

print(sum(map(value,cards)))
