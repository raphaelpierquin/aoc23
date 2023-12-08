import sys
import itertools
import more_itertools
import re
import math

times, distances = [],[]

def parseLine(line,n):
    global times, distances
    print(n,line)
    head, tail = map(str.strip,line.split(":"))
    print(head,tail)
    numbers = list(map(int,re.split(" +",tail)))
    if head == "Time":
        times = numbers
    else:
        distances = numbers
            
for l, line in enumerate(sys.stdin):
    parseLine(line.rstrip(),l)

def count_solutions(race):
    t,d = race 
    if t < 2 * math.sqrt(d):
        return 0
    a = math.sqrt(t*t-4*d)
    m = (t-a)/2
    if m == int(m):
        m = int(m)+1
    else:
        m = math.ceil(m) 
    M = (t+a)/2
    if M == int(M):
        M = int(M)-1
    else:
        M = math.floor(M)
    print(t,d,m,M)
    return M-m + 1

print(math.prod(map(count_solutions,zip(times,distances))))
