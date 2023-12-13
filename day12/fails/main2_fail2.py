import sys
import itertools
import more_itertools
import re
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

def consume(n,row):
    #print(n,row)
    i = 0
    pos = []
    consumed = 0
    maybe = 0
    while i<len(row):
        #print(i,consumed,maybe,row[i])
        if row[i] == "#" or (row[i] == "?" and consumed > 0):
            consumed += 1
        elif row[i] == "?":
            maybe += 1
        elif row[i] == ".":
            consumed,maybe = 0,0
        if consumed + maybe == n:
            if (i+1 < len(row) and row[i+1] != "#") or i+1 == len(row):
                pos.append(i+1)
                if maybe > 0:
                    offset =  i-consumed-maybe+2
                    pos.extend(map(lambda x: x+offset, consume(n,row[offset:])))
                    return pos
                else:
                    consumed,maybe = 0,0
                i+=1
            else: # next char is #
                if maybe > 0:
                    maybe -=1
                else:
                    return pos
        i+=1
    return list(set(pos))

def test_consume():
    assert consume(1,"") == []
    assert consume(1,".") == []
    assert consume(1,"#") == [1]
    assert consume(2,"#") == []
    assert consume(2,"##") == [2]
    assert consume(3,"###") == [3]
    assert consume(1,"##") == []
    assert consume(2,"#.##") == [4]
    assert consume(1,"?") == [1]
    assert consume(1,"#?") == [1]
    assert consume(1,"#.#") == [1,3]
    assert consume(1,"#?#") == [1,3]
    assert consume(1,"??") == [1,2]
    assert consume(1,"?.?") == [1,3]
    assert consume(1,"?.?.?") == [1,3,5]
    assert consume(1,"??.#") == [1,2,4]
    assert consume(1,"???#") == [1,2,4]
    assert consume(2,"???#") == [2,4]

def arrangements(row, records):
    #print("main",len(row),row,len(records),records)
    if len(records) == 0:
        if "#" in row:
            #print(0)
            return 0
        #print(1)
        return 1
    lcs = consume(records[0],row)
    #print("lcs",lcs)
    return sum(arrangements(row[lc+1:],records[1:]) for lc in lcs)


def test_arrangement1():
    assert arrangements("???##", [1,2]) == 2
    assert arrangements(".",[]) == 1
    assert arrangements("#",[1]) == 1
    assert arrangements("?",[1]) == 1
    assert arrangements("..",[]) == 1
    assert arrangements("##",[2]) == 1
    assert arrangements("?.?",[1]) == 2
    assert arrangements("???",[1,1]) == 1
    assert arrangements("???.###", [1,1,3]) == 1
    assert arrangements("??..??...?##.", [1,1,3]) == 4
    assert arrangements("?#?#?#?#?#?#?#?", [1,3,1,6]) == 1
    assert arrangements("????.#...#...", [4,1,1]) == 1
    assert arrangements(".??..??...?##.", [1,1,3]) == 4
    assert arrangements("?###????????", [3,2,1]) == 10
    assert arrangements("?###??????????###", [3,2,1,3]) == 16
    assert arrangements("?###??????????###????????", [3,2,1,3,2,1]) == 16*10
    assert arrangements("?###??????????###??????????###", [3,2,1,3,2,1,3]) == 16*16
    assert arrangements("?###??????????###??????????###????????", [3,2,1,3,2,1,3,2,1]) == 16*16*10
    assert arrangements("?###??????", [3,2,1]) == 3
    assert arrangements("?###????????###", [3,2,1,3]) == 6
    assert arrangements("?###????????###??????", [3,2,1,3,2,1]) == 3*6
    assert arrangements5("?###??????", [3,2,1]) == 6*6*6*6*3

def test_arrangement2():
    assert arrangements("???.?",[1,1]) == 4
    assert arrangements("?.???",[1,1]) == 4
    assert arrangements("?.???",[1,3]) == 1
    assert arrangements("?.???",[1,2]) == 2
    assert arrangements("?.???.?",[1,1,1]) == 5

def test_bug1():
    assert consume(2,"?.##") == [4]
    assert arrangements("?.##", [2]) == 1

def test_bug2():
    assert consume(3,"?#??#") ==  [3]
    assert consume(1,"??##") ==  [1]
    assert consume(1,"???##") ==  [1,2]
    assert arrangements("???##", [1,2]) == 2
    assert arrangements("##.???##", [2,1,2]) == 2

def test_bug3():
    assert consume(1, "???") == [1,2,3]
    assert consume(1, "???.###") == [1,2,3]
    assert arrangements("???.###", [1,1,3]) == 1
    assert arrangements5("?###????????", [3,2,1]) == 16*16*16*16*10 # 506250
    assert arrangements("?##????????##", [2,1,1,2]) == 11

def mult5(row, records):
    return ((row+"?")*4+row, records*5)

def test_mult5():
    assert(mult5(".#", [1])) == (".#?.#?.#?.#?.#", [1,1,1,1,1])
    assert(mult5( "???.###", [1,1,3])) == ("???.###????.###????.###????.###????.###", [1,1,3,1,1,3,1,1,3,1,1,3,1,1,3])

def arrangements5(row, records):
    return arrangements(*mult5(row,records))

def test_arrangements5_1():
    assert arrangements5("???.###", [1,1,3]) == 1
def test_arrangements5_2():
    assert arrangements5(".??..??...?##.", [1,1,3]) == 16384
def test_arrangements5_3():
    assert arrangements5("?#?#?#?#?#?#?#?", [1,3,1,6]) == 1
def test_arrangements5_4():
    assert arrangements5("????.#...#...", [4,1,1]) == 16
def test_arrangements5_5():
    assert arrangements5("????.######..#####.", [1,6,5]) == 2500
def test_arrangements5_6():
    assert arrangements5("?###????????", [3,2,1]) == 506250

if __name__ == "__main__":
    rows = parseFile(sys.argv[1])
    #for row,rec in rows:
    #    print(arrangements5(row,rec),row,rec)

    s=0
    i=0
    for row,rec in rows:
        i+=1
        print(i,row,rec)
        a = arrangements5(row,rec)
        print(i,a)
        s+=a
    print(s)
    #print(sum(map(lambda l: arrangements5(*l),rows)))
