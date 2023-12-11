import sys
import itertools
import more_itertools
import re
import math
import collections
import networkx as nx
from matplotlib import pyplot as plt

space = []
dim = None

def parseLine(line,n):
    global space,dim
    print(n,line)
    if not dim:
        dim = len(line)
    for i,c in enumerate(line):
        if c == "#":
            space.append((n,i))

def parseStdin():
    for l, line in enumerate(sys.stdin):
        parseLine(line.rstrip(),l)

def parseFile(filename):
    with open(filename,"r") as f:
        for l, line in enumerate(f):
            parseLine(line.rstrip(),l)

def expandLines(space):
    def column(g):
        l,c = g
        return c
    count = collections.Counter(map(column,space))
    expansion = []
    i=0
    for c in range(dim):
        if c not in count:
            i+=1        
        expansion.append(i)
    result = []
    for l,c in space:
        result.append((l,c+expansion[c]))
    return result

def expand(space):
    def transpose(g):
        l,c = g
        return c,l
    s = list(expandLines(space))
    s = list(map(transpose,s))
    s = list(expandLines(s))
    s = list(map(transpose,s))
    return s

def dist(g1,g2):
    l1,c1=g1
    l2,c2=g2
    return abs(l1-l2) + abs(c1-c2)
parseFile(sys.argv[1])
print(space)
space = expand(space)
print(space)
print(sum(dist(g1,g2) for g1 in space for g2 in space)/2)
