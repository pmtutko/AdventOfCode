#----------------------------------------------------------
# AoC 2024 Day 2
#----------------------------------------------------------
from pathlib import Path

MIN_DISTANCE = 1
MAX_DISTANCE = 3


def levelsAreSequential(levels):
    ascending = True
    if levels[0] < levels[1]:
        ascending = False
    for i in range(0, len(levels) - 1):
        if ascending:
            if levels[i] < levels[i+1]:
                # oops, these two aren't ascending
                return False
        else:
            if levels[i] > levels[i+1]:
                # oops, these two aren't descending
                return False
    return True

def levelDistancesAreSafe(levels):
    for i in range(0, len(levels) - 1):
        dist = abs(levels[i] - levels[i+1])
        if dist < MIN_DISTANCE or dist > MAX_DISTANCE:
            return False
    return True

def levelsAreSafe(levels):
    if levelsAreSequential(levels) and levelDistancesAreSafe(levels):
        return True
    return False

def part_1(input_lines) -> int:
    # answer = 510
    safe_total = 0
    for line in input_lines:
        levels = list(map(int, line.split()))
        if levelsAreSafe(levels):
            safe_total += 1
    return safe_total

def part_2(input_lines) -> int:
    # answer = 533
    safe_total = 0
    for line in input_lines:
        levels = list(map(int, line.split()))
        if levelsAreSafe(levels):
            safe_total += 1
        else:
            # sequentially remove each level to see if the 
            # level set becomes safe
            for i in range(0, len(levels)):
                reduced_levels = levels.copy()
                reduced_levels.pop(i)
                if levelsAreSafe(reduced_levels):
                    safe_total += 1
                    break
    return safe_total

if __name__ == "__main__":
    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt')
    print(f'reading from: {aoc_input}')
    with aoc_input.open('r') as f:
       #lines = " ".join(line.rstrip() for line in file)
       lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer_1 = part_1(lines)
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(lines)
    print(f'part 2 answer: {answer_2}')
