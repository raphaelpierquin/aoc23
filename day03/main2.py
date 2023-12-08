import sys
import itertools
import more_itertools
import re

DIGITS = re.compile('\d+')
SYMBOLS = re.compile('[^\d\.]')

parts = []  # (l,c,e,number)
symbols = [] # (l,c,symbol)

def gear_ratio(s):
    l2,c2,symbol = s
    if symbol != "*":
        return 0
    count = 0
    numbers = []
    for l0,c0,c1,number in parts:
        if adjacent(l0,c0,c1,l2,c2):
            count+=1
            numbers.append(number)
    print(count)
    if count == 2:
        return numbers[0]*numbers[1]
    return 0

def adjacent_to_any_symbol(l0,c0,c1):
    for l2,c2,symbol in symbols:
        if adjacent(l0,c0,c1,l2,c2):
            return True
    return False

def adjacent(l0,c0,c1,l2,c2):
    return abs(l0-l2) <= 1 and (c2 >= c0-1 and c2 <= c1)

def parseLine(line,n):
    print(n,line)
    for m in DIGITS.finditer(line):
        parts.append((n,m.start(),m.end(),int(m.group())))
    for m in SYMBOLS.finditer(line):
        symbols.append((n,m.start(),m.group()))

for l, line in enumerate(sys.stdin):
    parseLine(line.rstrip(),l)

print(sum(map(gear_ratio,symbols)))
