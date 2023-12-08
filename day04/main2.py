import sys
import itertools
import more_itertools
import re

DIGITS = re.compile('\d+')

cards = []

def matching(card):
    winning, having = card
    return len(list(filter(lambda x: x in winning, having)))

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

won = [1] * len(cards)

for n, card in enumerate(cards):
    m = matching(card)
    for i in range(m):
        won[n+1+i] += won[n]
print(sum(won))
