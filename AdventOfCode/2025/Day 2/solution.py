#----------------------------------------------------------
""" AoC 2025 Day 2                                      """
#----------------------------------------------------------
from pathlib import Path
import logging
import re

AOC_DAY_NUMBER = 2


def part_1(input_lines) -> int:
    """ AoC Part 1 Solution: test answer = 1227775554, answer = 21898734247  """
    invalid_id_sum = 0
    for line in input_lines:
        lbound, ubound = map(int, line.split('-'))
        #print(f'from {lbound} to {ubound}: {ubound - lbound} values to check')
        for value in range(lbound, ubound+1):
            vstr = str(value)
            # the check only works if there are two equal length strings
            if len(vstr) % 2 == 0:
                half_vlen = int(len(vstr)/2)
                if vstr[0:half_vlen] == vstr[half_vlen:]:
                    #print(f'  --- found {vstr}')
                    invalid_id_sum += value
    return invalid_id_sum

def part_2(input_lines) -> int:
    """ AoC Part 2 Solution: test answer = 4174379265, answer = 28915664389  """
    invalid_id_sum = 0
    for line in input_lines:
        lbound, ubound = map(int, line.split('-'))
        for value in range(lbound, ubound+1):
            vstr = str(value)
            match = re.search(r'(.+)\1+', vstr)
            if match:
                if match.group() == vstr:
                    #print(f'1 found {value}')
                    invalid_id_sum += value
                else:
                    match = re.search(r'(.+?)\1+', vstr)
                    if match:
                        if match.group() == vstr:
                            #print(f'2 found {value}')
                            invalid_id_sum += value
    return invalid_id_sum

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt')
    print(f'reading from: {aoc_input}')
    with aoc_input.open('r', encoding="utf-8") as f:
        lines = f.readlines()
    lines = lines[0].split(',')
    answer_1 = part_1(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer_1}')

    answer_2 = part_2(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer_2}')
