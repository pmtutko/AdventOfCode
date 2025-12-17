#----------------------------------------------------------
""" AoC 2025 Day 4                                      """
#----------------------------------------------------------
from pathlib import Path
import logging

AOC_DAY_NUMBER = 4


def print_paper_map(paper_map):
    """ pretty printing of the map """
    print('===============   Paper Map ===================')
    for row in paper_map:
        print(''.join(row))


def paper_rolls_around_this_spot(paper_map, r, c) -> int:
    """ Counts the number of paper rolls that surround the given spot """
    paper_roll = []
    if r > 0:
        if c > 0:
            paper_roll.append(paper_map[r-1][c-1])
        paper_roll.append(paper_map[r-1][c  ])
        if c < len(paper_map[r]) - 1:
            paper_roll.append(paper_map[r-1][c+1])

    if c > 0:
        paper_roll.append(paper_map[r  ][c-1])
    if c < len(paper_map[r]) - 1:
        paper_roll.append(paper_map[r  ][c+1])

    if r < len(paper_map) - 1:
        if c > 0:
            paper_roll.append(paper_map[r+1][c-1])
        paper_roll.append(paper_map[r+1][c  ])
        if c < len(paper_map[r]) - 1:
            paper_roll.append(paper_map[r+1][c+1])

    return paper_roll.count('@') + paper_roll.count('x')

def count_moveable_rolls_and_update(paper_map) -> int:
    moveable_rolls = 0
    for r, row in enumerate(paper_map):
        for c, spot in enumerate(row):
            if paper_map[r][c] == '@' or paper_map[r][c] == 'x':
                rolls_around = paper_rolls_around_this_spot(paper_map, r, c)
                if rolls_around < 4:
                    paper_map[r][c] = 'x'
                    moveable_rolls += 1
    #print_paper_map(paper_map)
    return moveable_rolls

def part_1(paper_map) -> int:
    """ AoC Part 1 Solution: test answer = 13, answer = 1505  """
    return count_moveable_rolls_and_update(paper_map)

def part_2(paper_map) -> int:
    """ AoC Part 2 Solution: test answer = 43, answer = xxxx  """
    total_moveable_rolls = 0
    moveable_rolls = count_moveable_rolls_and_update(paper_map)
    while moveable_rolls > 0:
        total_moveable_rolls += moveable_rolls
        # replace all the 'x' marks with '.'
        for r, row in enumerate(paper_map):
            for c, spot in enumerate(row):
                if spot == 'x':
                    paper_map[r][c] = '.'
        #print(f'\tmoved {moveable_rolls} rolls')
        moveable_rolls = count_moveable_rolls_and_update(paper_map)
    return total_moveable_rolls

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt')
    print(f'reading from: {aoc_input}')
    lines = []
    with aoc_input.open('r', encoding="utf-8") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    # build up the map of the paper rolls
    paper_map = []
    for line in lines:
        paper_map.append(list(line))

    answer1 = part_1(paper_map)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer1}')

    answer2 = part_2(paper_map)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer2}')
