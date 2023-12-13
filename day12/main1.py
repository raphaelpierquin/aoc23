import sys
import itertools
import more_itertools
#import re
#import math
#import collections
#import networkx as nx
#from matplotlib import pyplot as plt

def parseLine(line,n):
    print(n,line)
    r1,r2 = line.split(" ")
    f2 = list(map(int,r2.split(",")))
    return r1,f2

def parseStdin():
    for l, line in enumerate(sys.stdin):
        parseLine(line.rstrip(),l)

def parseFile(filename):
    rows = []
    with open(filename,"r") as f:
        for l, line in enumerate(f):
            rows.append(parseLine(line.rstrip(),l))
    return rows

def combinations(row):
    combs = [ row ]
    for i in range(len(row)):
        if row[i] == "?":
            newcombs = [comb[:i] + "#" + comb[i+1:] for comb in combs]
            newcombs.extend([comb[:i] + "." + comb[i+1:] for comb in combs])
            combs = newcombs
    return list(sorted(combs))

def test_combination():
    assert combinations("#") == [ "#" ]
    assert combinations("?") == [ "#", "." ]
    assert combinations("?#") == [ "##", ".#" ]
    assert combinations("#?") == [ "##", "#." ]
    assert combinations("??") == [ "##", "#.", ".#", ".." ]

def recordsof(row):
    groups = list(more_itertools.split_when(row,lambda x,y:x!=y))
    records = []
    for group in groups:
        if group[0] == "#":
            records.append(len(group))
    return records

def test_recordsof():
    assert recordsof("###..#.##") == [3,1,2]

def arrangements(row,records):
    return len(list(filter(lambda r: r==records, map(recordsof,combinations(row)))))

def test_arrangement():
    assert arrangements("##",[2]) == 1
    assert arrangements("???.###", [1,1,3]) == 1
    assert arrangements(".??..??...?##.", [1,1,3]) == 4
    assert arrangements("?###????????", [3,2,1]) == 10


if __name__ == "__main__":
    rows = parseFile(sys.argv[1])
    print(sum(map(lambda l: arrangements(*l),rows)))
