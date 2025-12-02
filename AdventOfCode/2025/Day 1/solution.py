#----------------------------------------------------------
# AoC 2025 Day 1
#----------------------------------------------------------
from pathlib import Path
import logging
from collections import deque

AOC_day_number = 1

MAX_DIAL_SIZE = 100
DIAL_START = 50
TARGET_NUMBER = 0


def part_1(input_lines) -> int:
    # test answer = 3, answer = 1007
    target_count = 0
    dial = deque(range(MAX_DIAL_SIZE))
    dial.rotate(-1 * DIAL_START)
    for line in input_lines:
        # assume we're turning LEFT, unless we're turning RIGHT
        print(f'Dial at {dial[0]}, turn {line}')
        direction = 1
        if line[0] == 'R':
            direction = -1
        clicks = int(line[1:])
        dial.rotate(direction * clicks)
        if dial[0] == TARGET_NUMBER:
            target_count += 1
    return target_count

def part_2(input_lines) -> int:
    # test answer = 6, answer = 5820
    target_count = 0
    dial = deque(range(MAX_DIAL_SIZE))
    dial.rotate(-1 * DIAL_START)
    for line in input_lines:
        # assume we're turning LEFT, unless we're turning RIGHT
        direction = 1
        if line[0] == 'R':
            direction = -1
        clicks = int(line[1:])
        # count how many times we'll fully rotate past 0
        passes_zero = (clicks // MAX_DIAL_SIZE)
        # now check if we'll pass 0 with less than a full rotation
        if dial[0] != 0:
            range_check = dial[0] + (-direction * (clicks % MAX_DIAL_SIZE))
            if (range_check <= 0) or (range_check >= MAX_DIAL_SIZE):
                passes_zero += 1
        print(f'Dial at {dial[0]}, turn {line} - passes zero {passes_zero}, range check {range_check}')
        dial.rotate(direction * clicks)
        target_count += passes_zero
    return target_count

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt') 
    print(f'reading from: {aoc_input}')
    with aoc_input.open('r') as f:
       #lines = " ".join(line.rstrip() for line in file)
       lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer_1 = part_1(lines)
    print(f'AOC Day {AOC_day_number} part 1 answer: {answer_1}')

    answer_2 = part_2(lines)
    print(f'AOC Day {AOC_day_number} part 2 answer: {answer_2}')
    