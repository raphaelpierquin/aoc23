import sys
import itertools
import more_itertools
import re
import math
import collection
import networkx as nx
from matplotlib import pyplot as plt


pipes = { 
         "|": [(0,-1),(0,1)],
         "-": [(-1,0),(1,0)],
         "L": [(0,-1),(1,0)],
         "J": [(0,-1),(-1,0)],
         "7": [(-1,0),(0,1)],
         "F": [(1,0),(0,1)],
         ".": [],
         "S": [(1,0),(-1,0),(0,1),(0,-1)]
        }

starting = None
dim = None
G = None

def parseLine(line,n):
    print(n,line)
    global dim, starting
    if not dim:
        dim = len(line)
    y = n
    for x, letter in enumerate(line):
        for direction in pipes[letter]:
            dx, dy = direction
            G.add_edge((x,y),(x+dx/2,y+dy/2))
        if letter == "S":
            starting = (x,y)

def show_pipes(G):
    plt.figure(figsize=(dim*2,dim*2))
    pos = {(x,y):(y,x) for x,y in G.nodes()}
    nx.draw(G, pos=pos, 
            node_color='lightgreen', 
            with_labels=True,
            node_size=600)

def parseStdin():
    for l, line in enumerate(sys.stdin):
        parseLine(line.rstrip(),l)

def parseFile(filename):
    global starting, dim, G
    starting = None
    dim = None
    G = nx.Graph()
    with open(filename,"r") as f:
        for l, line in enumerate(f):
            parseLine(line.rstrip(),l)

def pipeLoop(s):
    currents = [s]
    visited = []
    dist = {}
    l= -1
    while len(currents)>0:
        l += 1
        nextc = []
        for c in currents:
            visited.append(c) 
            dist[c]= l
            for n in G.adj[c]:
                if n not in visited:
                    nextc.append(n)
        currents = nextc
    return visited

'''
   +-+
   |.|
   +-+

 +-+-+
 |...|
 +.x.+
 |...|
 +-+-+
'''

'''
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
'''

'''
#5 4 True False
#5 5 False False
x5 6 True False
'''

insides = []

def area(loop):
    result = 0
    for j in range(dim):
        sys.stdout.write("\n")
        #sys.stdout.write(str(j))
        inside = False
        pOnLoop = False
        vups, vdowns = [], []
        for i in range(dim):
            onloop = (i,j) in loop
            vup   = ((i,j-0.5),(i,j)) in G.edges and (i,j-1) in loop
            vdown = ((i,j+0.5),(i,j)) in G.edges and (i,j+1) in loop
            crossingLoop = vup and vdown
            corner = vup ^ vdown
            if onloop:
                sys.stdout.write("#")
            if not onloop and not inside:
                sys.stdout.write(".")
            if not onloop and inside:
                insides.append((i,j))
                result += 1
                sys.stdout.write("x")
            if crossingLoop:
                inside = not inside
            if corner:
                if len(vups)>0:
                    if vup ^ vups[-1]:
                        inside = not inside
                    vups, vdowns = [], []
                else:
                    vups.append(vup)
                    vdowns.append(vdown)
            pOnLoop = onloop
    return result

parseFile(sys.argv[1])

print("searching loop")
loop = pipeLoop(starting)

print("cleaning")
x,y = starting
for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    if len(G.adj[(x+dx/2,y+dy/2)])<2:
        G.remove_node((x+dx/2,y+dy/2))
toremove=[]
for n in G.nodes:
    if n not in loop:
        toremove.append(n)
for n in toremove:
    G.remove_node(n)

print("area is")
print(area(loop))


