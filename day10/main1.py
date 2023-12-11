import sys
import itertools
import more_itertools
import re
import math
import collection
import networkx as nx
from matplotlib import pyplot as plt

dim = None
G = nx.Graph()

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

def parseLine(line,n):
    #print(n,line)
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

for l, line in enumerate(sys.stdin):
    parseLine(line.rstrip(),l)

def farthest(s):
    currents = [s]
    visited = []
    dist = {}
    l= -1
    while len(currents)>0:
        l += 1
        print(l,len(visited),len(currents))
        nextc = []
        for c in currents:
            visited.append(c) 
            dist[c]= l
            for n in G.adj[c]:
                if n not in visited:
                    nextc.append(n)
        currents = nextc
    return l/2

print(G.nodes)
for i,j in itertools.product(range(dim),range(dim)):
    if (i,j) not in G.nodes:
        continue
    adj = len(G.adj[(i,j)])
    if adj>2:
        print(i,j,adj)
print(farthest(starting))
