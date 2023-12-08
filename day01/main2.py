import sys
import itertools
import more_itertools

digits = [ "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
stigid = list(map(lambda x: "".join(reversed(x)), digits))

def is_a_digit(x):
    return x in "0123456789"

def digit_at(line,i,digits):
    if is_a_digit(line[i]):
        return int(line[i])
    digit = more_itertools.first_true(digits,pred = lambda x: line[i:].startswith(x))
    if digit:
        return digits.index(digit)+1
    return False

def parse(line):
    print(line)
    first = more_itertools.first_true(range(len(line)),
                                      pred=lambda x: digit_at(line,
                                                              x,
                                                              digits))
    first = digit_at(line,first,digits)
    reversed_line = "".join(reversed(line))
    last = more_itertools.first_true(range(len(line)),
                                      pred=lambda x: digit_at(reversed_line,
                                                              x,
                                                              stigid))
    last = digit_at(reversed_line,last,stigid)
    return first*10+last

lines = []

for line in sys.stdin:
    lines.append(line.rstrip())

print(more_itertools.map_reduce(lines,lambda x:1,parse,sum))
