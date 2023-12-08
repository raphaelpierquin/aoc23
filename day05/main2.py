import sys
import itertools
import more_itertools
import re
from module import translate

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
    #print(n,line)
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

def find_map_from(category):
    for m in nmaps:
        if m[0][0] == category:
            return m
    raise Exception("no map from " + category)

def nearest_seed(seed_range):
    category = "seed"
    mapped = [ seed_range ]
    while category != "location":
        m = find_map_from(category)
        category = m[0][1]
        mapped = translate(mapped,m[1])
    return(min(map(lambda r: r[0],mapped)))

def batched(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

#print(sum([r for n,r in batched(seeds,2)]))

seed_ranges = list(map(lambda r: (r[0],r[0]+r[1]), batched(seeds,2)))
# d s r -> s s+r d-s)

#print(maps )
nmaps = []
for mapping in maps:
    cats, zone = mapping
    nzone = list(map(lambda m: (m[1],m[1]+m[2], m[0]-m[1]), zone))
    nmaps.append((cats,nzone))

print(min(map(nearest_seed,seed_ranges)))

