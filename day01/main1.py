import sys
import itertools
import more_itertools

def is_a_digit(x):
    return x in "0123456789"

def parse(line):
    first = int(more_itertools.first_true(line,pred=is_a_digit))
    last = int(more_itertools.first_true(reversed(line),pred=is_a_digit))
    return first*10+last

lines = []

for line in sys.stdin:
    lines.append(line.rstrip())

print(more_itertools.map_reduce(lines,lambda x:1,parse,sum))
