import sys
import itertools
import functools
import operator
import more_itertools
import re
import math
import collection

instructions = []
choices = {}

def parseLine(line,n):
    global instructions, choices
    print(n,line)
    if "=" not in line :
        instructions = list(map(lambda x: x=="R",line))
    else:
        # AAA = (BBB, CCC)
        #for group in re.match("(.*) = \((.*), (.*)\)",line):
        m = re.findall("[^\(\) =,]+",line)
        choices[m[0]] = (m[1],m[2])
            
for l, line in enumerate(sys.stdin):
    parseLine(line.rstrip(),l)

nodes = list(filter(lambda l: l.endswith('A'),choices.keys()))
instructions_cycle = itertools.cycle(instructions)
cycle_length={}
for node in nodes:
    step = 0
    current = node
    while not current.endswith('Z'):
        current_choice = choices[current] 
        next_instruction = next(instructions_cycle)
        if next_instruction:
            choice_index = 1
        else:
            choice_index = 0
        current = current_choice[choice_index]
        step += 1
    cycle_length[node] = step

print(cycle_length)
print(functools.reduce(math.lcm,cycle_length.values()))
