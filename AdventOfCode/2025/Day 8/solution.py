#----------------------------------------------------------
""" AoC 2025 Day 0                                      """
#----------------------------------------------------------
from pathlib import Path
import logging

AOC_DAY_NUMBER = 0


def part_1(input_lines) -> int:
    """ AoC Part 1 Solution: test answer = xxx, answer = xxxx  """
    return 0

def part_2(input_lines) -> int:
    """ AoC Part 2 Solution: test answer = xxx, answer = xxxx  """
    return 0

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    #aoc_input = Path(__file__).with_name('input.txt')
    aoc_input = Path(__file__).with_name('input_test.txt')
    print(f'reading from: {aoc_input}')
    lines = []
    with aoc_input.open('r', encoding="utf-8") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer1 = part_1(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer1}')

    answer2 = part_2(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer2}')
