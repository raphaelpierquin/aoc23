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

    matching = []
    for c in candidates:
        if all([lines[c-1-i] == lines[c+i] for i in range(min(n-c,c))]):
            matching.append(c)
    return matching

def test_find_matching():
    lines= [
            ".#.",
            "###",
            "###",
            "## ",
            "## ",
            "###",
           ]
    assert find_matching(lines) == [4]

def transpose(lines):
    return ["".join([line[i] for line in lines]) for i in range(len(lines[0]))]

def test_transpose():
    assert transpose(['#..','#..']) == ['##','..','..']

def reflexions(lines):
    return 100 * sum(matching_after_fix(lines)) + sum(matching_after_fix(transpose(lines)))

def test_reflexions():
    lines = [
             "#..####",
             "##.....",
             "###...#",
             "###....",
             "##.....",
             "#..####",
             ]
    assert reflexions(lines) == 305

def matching_after_fix(lines):
    matching_before = find_matching(lines)
    potential_smudges = {}
    n = len(lines)
    def f(x):
        i,p = x
        if p[0] != p[1]:
            return i
    for i,j in itertools.product(range(n),range(n)):
        diffs = list(filter(lambda x: x is not None, map(f, enumerate(zip(lines[i],lines[j])))))
        if len(diffs) == 1:
            potential_smudges[i,j] = diffs[0]
    assert(len(potential_smudges)%2 == 0)
    for coord, pos in potential_smudges.items():
        i,j = coord
        if i>j:
            continue
        newlines = list(lines)
        newlines[i] = lines[j]
        matching_after = find_matching(newlines)
        if matching_after !=[] and matching_after != matching_before:
            for e in matching_before:
                if e in matching_after:
                    matching_after.remove(e)
            return matching_after
    return []

def test_matching_after_fix2():
    lines = [ 
             "######",
             ".####.",
             "..##..",
             "#....#",
             "#.#..#",
             ]
    assert matching_after_fix(lines) == [4]

def test_matching_after_fix1():
    lines = [
             "#####.",
             "##....",
             "##...#",
             ]
    assert matching_after_fix(lines) == [2]

def test_matching_after_fix3():
    lines = [
            ".##...##.",
            "#..#.###.",
            "####.....",
            "#..######",
            ".##..#..#",
            ".##.#####",
            "....#####",
            ]
    assert matching_after_fix(transpose(lines)) == [7]

def summarize(patterns):
    return sum(map(reflexions,patterns))

def test_part_2():
    patterns = parseFile("test.txt")
    assert summarize(patterns) == 400

def test_broken():
    patterns = parseFile("test2.txt")
    assert summarize(patterns) != 0

def test_every_possible_smudge():
    pass

if __name__ == "__main__":
    patterns = parseFile(sys.argv[1])
    print(summarize(patterns))
