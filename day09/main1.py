import sys
import itertools
import more_itertools
import re
import math
import collection

seqs = []
def parseLine(line,n):
    print(n,line)
    return list(map(int,line.split(" ")))
            
for l, line in enumerate(sys.stdin):
    seqs.append(parseLine(line.rstrip(),l))

def prediction(seq):
    diffs = [j-i for i,j in itertools.pairwise(seq)]
    if all(map(lambda x: x==0,diffs)):
        return seq[-1]
    else:
        return seq[-1] + prediction(diffs)

def previous(seq):
    diffs = [j-i for i,j in itertools.pairwise(seq)]
    if all(map(lambda x: x==0,diffs)):
        return seq[0]
    else:
        return seq[0] - previous(diffs)

print("prediction",sum(map(prediction,seqs)))
print("previous",sum(map(previous,seqs)))
