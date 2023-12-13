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

def consumex(n,row):
   n1,s1,e1,p1 = 0,0,0,"" # [#?]+
   n2,s2,e2,p2 = 0,0,0,"" # #+
   n3,s3,e3,p3 = 0,0,0,"" # ^?+ (from 1)
   n4,s4,e4,p4 = 0,0,0,"" # ?+ (from end of 1)
   n5,s5,e5,p5 = 0,0,0,"" # #([?#]*#)?

   m1 = re.search("[#?]+",row)
   if m1:
       p1 = m1.group()
       n1 = len(m1.group())
       s1 = m1.start()
       e1 = m1.end()
       m2 = re.search("#+",m1.group())
       if m2:
           p2 = m2.group()
           n2 = len(m2.group())
           s2 = m2.start()
           e2 = m2.end()
       m3 = re.search("^\\?+",m1.group())
       if m3:
           p3 = m3.group()
           n3 = len(m3.group())
           s3 = m3.start()
           e3 = m3.end()
       if m2:
           m4 = re.search("\\?+",m1.group()[m2.end():])
           if m4:
               p4 = m4.group()
               n4 = len(m4.group())
               s4 = m4.start()
               e4 = m4.end()
       m5 = re.search("#([?#]*#)?",m1.group())
       if m5:
           p5 = m5.group()
           n5 = len(m5.group())
           s5 = m5.start()
           e5 = m5.end()

   if n1 < n and n2 >= 0:
       if e1 < len(row):
           return list(map(lambda x: x+e1+1, consumex(n,row[e1+1:])))
       else:
           return []
   if n3 >= n+1 and n2>0:
       return list(range(s1+n,s1+n3))
   if n2 == n:
       i = s1+e2
       return [i]
   if n1 == n and n2> 0:
       i = e1
       return [i]
   if n2>0:
       print("bonjour")
       left = min(n-n2,n3)
       right = max(0, n - (n2 + left))
       first = s1+s2-left+n

       right = min(n-n2,n1-n2-n3)
       left = max(0, n - (n2 + right))
       last = s1+s2+n2+right+1

       return list(range(first,last))
   else:
       first = s1 + n
       last  = e1 + 1
       if last == first:
           res = [ last ]
       else:
           res =  list(range(first,last))
       res.extend(map(lambda x: x+e1+1, consumex(n,row[e1+1:])))
       return res
   assert False
  
def test_consumex_1():
    assert consumex(1,"") == []
    assert consumex(1,"...") == []
    assert consumex(1,".##.") == []
    assert consumex(1,"#") == [1]
    assert consumex(1,"#.") == [1]
    assert consumex(1,".#.") == [2]

def test_consumex_1u():
    assert consumex(1,"?") == [1]
    assert consumex(1,"?.") == [1]
    assert consumex(1,".?") == [2]
    assert consumex(1,".?.") == [2]

def test_consumex_2u():
    assert consumex(1,"?.?") == [1,3]
    assert consumex(1,"?.?.?") == [1,3,5]
    assert consumex(1,".??.") == [2,3]
    assert consumex(1,".??.") == [2,3]

def test_consumex_3u():
    assert consumex(1,"???.") == [1,2,3]
    assert consumex(1,"???") == [1,2,3]

def test_consumex_1_and_us():
    assert consumex(1,".?#.") == [3]
    assert consumex(1,".#?.") == [2]
    assert consumex(1,".?#?.") == [3]

def test_consumex_2_and_us():
    assert consumex(2,".?#.") == [3]
    assert consumex(2,".?#?.") == [3,4]

def test_consumex_3_and_us():
    assert consumex(3,"?#?") == [3]
    assert consumex(3,".?#?") == [4]
    assert consumex(3,".#?#.") == [4]
    assert consumex(3,".?##?.") == [4,5]
    assert consumex(3,".#?#") == [4]
    assert consumex(3,".##?.") == [4]
    assert consumex(3,".?##.") == [4]

def arrangements(row, records):
    #print("main",len(row),row,len(records),records)
    if len(records) == 0:
        if "#" in row:
            #print(0)
            return 0
        #print(1)
        return 1
    lcs = consumex(records[0],row)
    #print("consumex", records[0], lcs)
    return sum(arrangements(row[lc+1:],records[1:]) for lc in lcs)

def test_arrangement():
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

def test_arrangement2():
    assert arrangements("???.?",[1,1]) == 4
    assert arrangements("?.???",[1,1]) == 4
    assert arrangements("?.???",[1,3]) == 1
    assert arrangements("?.???",[1,2]) == 2
    assert arrangements("?.???.?",[1,1,1]) == 5

def test_bug1():
    assert consumex(2,"?.##") == [4]
    assert arrangements("?.##", [2]) == 1

def test_bug2():
    assert consumex(3,"?#??#") ==  [3]
    assert consumex(1,"???#") ==  [1,2]
    assert consumex(1,"??##") ==  [1]
    assert consumex(1,"???##") ==  [1,2]
    assert arrangements("???##", [1,2]) == 2
    assert arrangements("##.???##", [2,1,2]) == 2

def mult5(row, records):
    return ((row+"?")*4+row, records*5)

def test_mult5():
    assert(mult5(".#", [1])) == (".#?.#?.#?.#?.#", [1,1,1,1,1])

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
    for row,rec in rows:
        print(arrangements5(row,rec),row,rec)

    print(sum(map(lambda l: arrangements5(*l),rows)))
