import sys
import itertools
import more_itertools

colors = [ "red", "green", "blue" ]

def parse(line):
    partie = int(line.split(":")[0].split(" ")[1])
    manches = []
    for manche in line.split(":")[1].split(";"):
        values = [0,0,0]
        for tirage in list(map(lambda x: x.lstrip(),manche.split(","))):
            number = int(tirage.split(" ")[0])
            color = colors.index(tirage.split(" ")[1])
            values[color] = number
        manches.append(values)
    return (partie, manches)

def possible(partie, limites):
    numero, manches = partie
    def tirage_impossible(tirage):
        return any(map(lambda b: b[0] > b[1], zip(tirage,limites)))
    impossible = any(map(tirage_impossible, manches))
    if impossible:
        return 0
    return numero

lines = []

for line in sys.stdin:
    lines.append(parse(line.rstrip()))

print(sum(map(lambda x: possible(x,[12,13,14]),lines)))
