from collections import deque
import re

test_springs = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

def ints(input: str) -> list[int]:
  return [int(match) for match in re.findall(r"-?\d+", input)]

def gen_key(
  current_damaged_springs: int,
  unexplored: list[str],
  expected_damaged_springs: deque[int]
) -> str:
  damaged = ",".join(str(x) for x in expected_damaged_springs)
  return f"{current_damaged_springs}:{''.join(unexplored)}:{damaged}"


def possible_spring_arrangements(
  i: int,
  current_damaged_springs: int,
  springs: list[str],
  expected_damaged_springs: deque[int],
  memo: dict[str, int],
) -> int:
  memo_key = gen_key(current_damaged_springs, springs[i:], expected_damaged_springs)
  if memo_key in memo:
    return memo[memo_key]
  excess_springs = not expected_damaged_springs and current_damaged_springs > 0
  insufficient_springs = len(expected_damaged_springs) > 1 or (expected_damaged_springs and expected_damaged_springs[0] > current_damaged_springs)
  if excess_springs or (i == len(springs) and insufficient_springs):
    memo[memo_key] = 0
    return 0
  elif i == len(springs) and not insufficient_springs:
    memo[memo_key] = 1
    return 1
  elif springs[i] == ".":
    if expected_damaged_springs and current_damaged_springs == expected_damaged_springs[0]:
      fulfilled_damaged_springs = expected_damaged_springs.popleft()
      memo[memo_key] = possible_spring_arrangements(i+1, 0, springs, expected_damaged_springs, memo)
      expected_damaged_springs.appendleft(fulfilled_damaged_springs)
      return memo[memo_key]
    elif current_damaged_springs > 0 and current_damaged_springs < expected_damaged_springs[0]:
      memo[memo_key] = 0
      return 0
    memo[memo_key] = possible_spring_arrangements(i+1, 0, springs, expected_damaged_springs, memo)
    return memo[memo_key]
  elif springs[i] == "#":
    current_damaged_springs += 1
    if not expected_damaged_springs or current_damaged_springs > expected_damaged_springs[0]:
      memo[memo_key] = 0
      return 0
    memo[memo_key] = possible_spring_arrangements(i+1, current_damaged_springs, springs, expected_damaged_springs, memo)
    return memo[memo_key]
  
  springs[i] = "#"
  arr = possible_spring_arrangements(i, current_damaged_springs, springs, expected_damaged_springs, memo)
  springs[i] = "."
  arr += possible_spring_arrangements(i, current_damaged_springs, springs, expected_damaged_springs, memo)
  springs[i] = "?"
  memo[memo_key] = arr
  return arr
  

def part_one(lines: list[str]):
  arrangements = []
  for line in lines:
    parts = line.split()
    springs = list(parts[0])
    expected_damaged_springs = deque(ints(parts[1]))
    arrangements.append(possible_spring_arrangements(0, 0, springs, expected_damaged_springs, dict()))
  return sum(arrangements)

def part_two(lines: list[str]):
  arrangements = []
  for line in lines:
    parts = line.split()
    springs = list("?".join(parts[0] for _ in range(5)))
    expected_damaged_springs = deque()
    for _ in range(5):
      expected_damaged_springs.extend(ints(parts[1]))
    arrangements.append(possible_spring_arrangements(0, 0, springs, expected_damaged_springs, dict()))
  return sum(arrangements)
