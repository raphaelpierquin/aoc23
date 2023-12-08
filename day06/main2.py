import sys
import itertools
import more_itertools
import re
import math

time, distance = 0,0

def parseLine(line,n):
    global time, distance
    print(n,line)
    head, tail = map(str.strip,line.split(":"))
    number = int(tail.replace(" ",""))
    if head == "Time":
        time = number
    else:
        distance = number
            
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
    return M-m + 1

print(time,distance,count_solutions((time,distance)))
