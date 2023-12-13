import sys
import itertools
import more_itertools
import re
import math
from collections import Counter, deque, defaultdict
#import networkx as nx
#from matplotlib import pyplot as plt


def parseFile(filename):
    patterns = []
    with open(filename,"r") as f:
        lines = []
        for l, line in enumerate(f):
            line = line.rstrip()
            if line == "":
                patterns.append(lines)
                lines = []
            else:
                lines.append(line)
        patterns.append(lines)
    return patterns

def find_matching(lines):
    lines = list(lines)
    n = len(lines)

    candidates = []
    for i,pair in enumerate(itertools.pairwise(lines)):
        l1,l2= pair
        if l1 == l2:
            candidates.append(i+1)

    for c in candidates:
        if all([lines[c-1-i] == lines[c+i] for i in range(min(n-c,c))]):
            return c
    return 0

def test_find_matching():
    lines= [
            ".#.",
            "###",
            "###",
            "## ",
            "## ",
            "###",
           ]
    assert find_matching(lines) == 4

def transpose(lines):
    return ["".join([line[i] for line in lines]) for i in range(len(lines[0]))]

def test_transpose():
    assert transpose(['#..','#..']) == ['##','..','..']

def reflexions(lines):
    return 100 * find_matching(lines) + find_matching(transpose(lines))

def test_reflexions():
    lines = [
             "##..",
             "###.",
             "###.",
             ]
    assert reflexions(lines) == 201

def summarize(patterns):
    return sum(map(reflexions,patterns))

def test_part_1():
    patterns = parseFile("test.txt")
    assert summarize(patterns) == 405

if __name__ == "__main__":
    patterns = parseFile(sys.argv[1])
    print(summarize(patterns))
