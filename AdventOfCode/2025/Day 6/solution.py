#----------------------------------------------------------
""" AoC 2025 Day 6                                      """
#----------------------------------------------------------
from pathlib import Path
import logging

AOC_DAY_NUMBER = 6


def part_1(input_lines) -> int:
    """ AoC Part 1 Solution: test answer = 4277556, answer = 6503327062445  """
    in_lines = [x.strip() for x in input_lines]
    math_numbers = []
    for line in in_lines:
        math_line = []
        if line[0].isdigit():
            for val in line.split(' '):
                if val != '':
                    math_line.append(int(val))
        else:
            for i, val in enumerate(line):
                if val != ' ':
                    math_line.append(val)
        math_numbers.append(math_line)

    grand_total = 0
    math_operation = math_numbers[-1]
    for i in range(len(math_numbers[0])):
        column_total = 0
        if math_operation[i] == '*':
            column_total = 1
        for j in range(len(math_numbers) - 1):
            if math_operation[i] == '*':
                column_total *= math_numbers[j][i]
            else:
                column_total += math_numbers[j][i]
        #print(f'column {i} total = {column_total}')
        grand_total += column_total
    return grand_total

def part_2(input_lines) -> int:
    """ AoC Part 2 Solution: test answer = 3263827, answer = 9640641878593  """
    in_lines = [x.strip('\n') for x in input_lines]
    math_operations = input_lines[-1].split()
    grand_total = 0
    column_values = []
    for c in range(len(in_lines[0]) - 1, -1, -1):
        column_value = ''
        all_columns_blank = False
        for r in range(len(in_lines) - 1):
            column_value = column_value + in_lines[r][c]
        if column_value.strip().isdigit():
            column_values.append(int(column_value))
        else:
            all_columns_blank = True
        if all_columns_blank:
            math_operation = math_operations.pop()
            if math_operation == '*':
                column_total = 1
                for value in column_values:
                    column_total *= value
            else:
                column_total = 0
                for value in column_values:
                    column_total += value
            column_values = []
            grand_total += column_total
            #print(f'column total {column_total}')
    math_operation = math_operations.pop()
    if math_operation == '*':
        column_total = 1
        for value in column_values:
            column_total *= value
    else:
        column_total = 0
        for value in column_values:
            column_total += value
    grand_total += column_total
    #print(f'column total {column_total}')
    return grand_total

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt')
    print(f'reading from: {aoc_input}')
    lines = []
    with aoc_input.open('r', encoding="utf-8") as f:
        lines = f.readlines()

    answer1 = part_1(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer1}')

    answer2 = part_2(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer2}')
