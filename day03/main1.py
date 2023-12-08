import sys
import itertools
import more_itertools
import re

DIGITS = re.compile('\d+')
SYMBOLS = re.compile('[^\d\.]')

parts = []  # (l,c,e,number)
symbols = [] # (l,c,symbol)

def adjacent_to_any_symbol(l0,c0,c1):
    for l2,c2,symbol in symbols:
        if adjacent(l0,c0,c1,l2,c2):
            return True
    return False

def adjacent(l0,c0,c1,l2,c2):
    return abs(l0-l2) <= 1 and (c2 >= c0-1 and c2 <= c1)

def parseLine(line,n):
    print(n,line.split('.'))
    for m in DIGITS.finditer(line):
        parts.append((n,m.start(),m.end(),int(m.group())))
    for m in SYMBOLS.finditer(line):
        symbols.append((n,m.start(),m.group()))

for l, line in enumerate(sys.stdin):
    parseLine(line.rstrip(),l)

result = 0
for l0,c0,c1,number in parts:
    if adjacent_to_any_symbol(l0,c0,c1):
        result += number

print(result)
