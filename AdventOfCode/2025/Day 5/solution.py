#----------------------------------------------------------
""" AoC 2025 Day 5                                      """
#----------------------------------------------------------
from pathlib import Path
import logging

AOC_DAY_NUMBER = 5


def part_1(id_ranges, ingredient_ids) -> int:
    """ AoC Part 1 Solution: test answer = 3, answer = 782  """
    fresh_ingredients = 0
    for ingredient_id in ingredient_ids:
        for id_range in id_ranges:
            if ingredient_id >= id_range[0] and ingredient_id <= id_range[1]:
                fresh_ingredients += 1
                break
    return fresh_ingredients

def part_2(id_ranges, ingredient_ids) -> int:
    """ AoC Part 2 Solution: test answer = 14, answer = xxxx  """
    # sort ascending by the first element
    id_ranges.sort()
    fresh_ranges = []
    for i, id_range in enumerate(id_ranges):
        # take each id range and shuffle it into place
        if len(fresh_ranges) == 0:
            fresh_ranges.append(id_range)
        else:
            range_not_modified = True
            range_not_skipped = True
            for fresh_range in fresh_ranges:
                if ((id_range[0] >= fresh_range[0]) and
                    (id_range[0] <= fresh_range[1])):
                    if id_range[1] > fresh_range[1]:
                        # in this case, the low end of the range is fine, but
                        # the higher end is extended to match the id range
                        fresh_range[1] = id_range[1]
                        range_not_modified = False
                    else:
                        # this range is completely inside the fresh range,
                        # so skip it
                        range_not_skipped = False
                    break
            if range_not_modified and range_not_skipped and id_range != fresh_ranges[-1]:
                # beware of duplicate ranges!! (they will appear
                # together because the ranges are sorted)
                fresh_ranges.append(id_range)

    #print(f'fresh: {fresh_ranges}')
    total_fresh_ingredients = 0
    for fresh_range in fresh_ranges:
        print(f'range {fresh_range} length {fresh_range[1] - fresh_range[0] + 1}')
        total_fresh_ingredients += (fresh_range[1] - fresh_range[0] + 1)
    return total_fresh_ingredients

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

    id_ranges = []
    ingredient_ids = []
    still_compiling_ranges = True
    for line in lines:
        if still_compiling_ranges:
            if len(line) == 0:
                still_compiling_ranges = False
            else:
                id_ranges.append([int(val) for val in line.split('-')])
        else:
            ingredient_ids.append(int(line))

    answer1 = part_1(id_ranges, ingredient_ids)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer1}')

    answer2 = part_2(id_ranges, ingredient_ids)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer2}')
