#----------------------------------------------------------
# AoC 2024 Day 7
#----------------------------------------------------------
from pathlib import Path
import logging
from bitarray import bitarray


def convertToBase(number, base, width=1):
    # baed on: https://stackoverflow.com/a/34559825/4717755
    if number == 0:
        return '0' * width
    nums = []
    while number:
        number, rem = divmod(number, base)
        nums.append(str(rem))
    answer_without_padding = ''.join(reversed(nums))
    padded_answer = answer_without_padding.zfill(width)
    return padded_answer


def calculateNumbers(target, numbers, base=2) -> bool:
    '''
    returns if the total calculated by applying the given operations
      total_ops is the number of potential operations, which is
      one less than the list of numbers.
    '''
    number_of_operation_places = len(numbers) - 1
    total_ops = base**number_of_operation_places
    for ops in range(total_ops):
        # convert to a list of the current operations
        # '0' represents addition
        # '1' represents multiplication
        # '2' represents concatenation
        these_ops = convertToBase(ops, base, number_of_operation_places)
        test_total = numbers[0]
        i = 1
        for op in list(these_ops):
            if op == '0':
                test_total += numbers[i]
            elif op == '1':
                test_total *= numbers[i]
            elif op == '2':
                test_total = int(str(test_total) + str(numbers[i]))
            i += 1
        if test_total == target:
            # the operations matched the target valule, so return True
            return True
    return False

def part_1(input_lines) -> int:
    # test answer = 3749, answer = 6083020304036
    sum_of_matched_totals = 0
    for line in input_lines:
        target_total = int(line.split(':')[0])
        numbers = list(map(int, line.split(':')[1].split()))
        if calculateNumbers(target_total, numbers, base=2):
            logging.debug(f"line: {line} matches!")
            sum_of_matched_totals += target_total
    return sum_of_matched_totals

def part_2(input_lines) -> int:
    # test answer = 11387, answer = xxxx
    sum_of_matched_totals = 0
    for line in input_lines:
        target_total = int(line.split(':')[0])
        numbers = list(map(int, line.split(':')[1].split()))
        if calculateNumbers(target_total, numbers, base=3):
            logging.debug(f"line: {line} matches!")
            sum_of_matched_totals += target_total
    return sum_of_matched_totals

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
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(lines)
    print(f'part 2 answer: {answer_2}')
    