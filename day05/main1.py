import sys
import itertools
import more_itertools
import re

seeds = []
maps = []
current_title = None
current_map = None

def parse_numbers(line):
    return [ int(w.strip()) for w in line.split(" ") ]

def parse_map_header(line):
    ws = line.split(" ")[0]
    ws = ws.split("-")
    return [ws[0], ws[2]]

def parse_header(line):
    return [ w.strip() for w in line.split(":") ]

def parseLine(line,n):
    global current_title, current_map, maps, seeds
    print(n,line)
    if ":" in line:
        words = parse_header(line)
        if words[0] == "seeds":
            seeds = parse_numbers(words[1])
        else:
            current_title = parse_map_header(words[0])
            current_map = []
        return
    if line == "":
       if current_title:
            maps.append((current_title,current_map)) 
       return
    current_map.append(parse_numbers(line))

for l, line in enumerate(sys.stdin):
    parseLine(line.rstrip(),l)

def translate(seed,m):
    for d,s,r in m[1]:
        if seed >= s and seed < s+r:
            seed = seed - s + d
            return seed
    return seed

def find_map_from(category):
    for m in maps:
        if m[0][0] == category:
            return m
    raise Exception("no map from " + category)

def location_of_seed(seed):
    category = "seed"
    mapped = seed
    while category != "location":
        m = find_map_from(category)
        category = m[0][1]
        mapped = translate(mapped,m)
    return mapped

print()
print(min(map(location_of_seed,seeds)))
