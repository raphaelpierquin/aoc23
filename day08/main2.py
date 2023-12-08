import sys
import itertools
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

step = 0
currents = list(filter(lambda l: l.endswith('A'),choices.keys()))

instructions_cycle = itertools.cycle(instructions)

while any(map(lambda l: not l.endswith('Z'), currents)):
   current_choices = [choices[current] for current in currents]
   next_instruction = next(instructions_cycle)
   if next_instruction:
       choice_index = 1
   else:
       choice_index = 0
   currents = [current_choice[choice_index] for current_choice in current_choices]
   step += 1
print(step)
