#----------------------------------------------------------
# AoC 2024 Day 0
#----------------------------------------------------------
from pathlib import Path
import logging


def part_1(input_lines) -> int:
    # test answer = xxx, answer = xxxx
    ...

def part_2(input_lines) -> int:
    # test answer = yyy, answer = xxxx
    ...

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    #aoc_input = Path(__file__).with_name('input.txt')
    aoc_input = Path(__file__).with_name('input_test.txt') 
    print(f'reading from: {aoc_input}')
    with aoc_input.open('r') as f:
       #lines = " ".join(line.rstrip() for line in file)
       lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer_1 = part_1(lines)
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(lines)
    print(f'part 2 answer: {answer_2}')
    