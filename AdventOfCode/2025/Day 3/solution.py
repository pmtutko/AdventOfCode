#----------------------------------------------------------
""" AoC 2025 Day 3                                      """
#----------------------------------------------------------
from pathlib import Path
import logging

AOC_DAY_NUMBER = 3

# Source - https://stackoverflow.com/a/3990826
# Posted by martineau, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-03, License - CC BY-SA 3.0

def maxelements(seq):
    ''' Return list of position(s) of largest element '''
    max_indices = []
    if seq:
        max_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(seq) if val >= max_val):
            if val == max_val:
                max_indices.append(i)
            else:
                max_val = val
                max_indices = [i]
    return max_indices

def maxvalues(seq):
    ''' Return list of position(s) of largest values in the string '''
    max_indices = []
    if seq:
        max_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(list(seq)) if val >= max_val):
            if val == max_val:
                max_indices.append(i)
            else:
                max_val = val
                max_indices = [i]
    return max_indices

def minelements(seq):
    ''' Return list of position(s) of smallest element '''
    min_indices = []
    if seq:
        min_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(seq) if val <= min_val):
            if val == min_val:
                min_indices.append(i)
            else:
                min_val = val
                min_indices = [i]
    return min_indices

def values_by_index(sequence, value) -> list:
    ''' Return a list of all the indexes in the string at which the value appears '''
    return [i for i, val in enumerate(sequence) if int(val) == value]

def copy_first_joltage_seq(remaining_sequence, max_nums, jolts_seq) -> int:
    ''' Copy the value from the max_nums[0] index position to the jolts sequence 
        and return the resulting length of the jolts sequence '''
    while len(max_nums) > 0:
        jolts_seq.append(remaining_sequence[max_nums.pop(0)])
    return len(jolts_seq)


def part_1(input_lines) -> int:
    """ AoC Part 1 Solution: test answer = 357, answer = 17427  """
    total_joltage = 0
    seq_number = 1
    for line in input_lines:
        first_digit = 0
        second_digit = 0
        highest_joltage = 0
        # first, find the highest values in each sequence and their index
        nums = list(map(int, list(line)))
        max_nums = maxelements(nums)
        #print(f'testing sequence {seq_number}: {line}\n        max values ({nums[max_nums[0]]}) at {max_nums}')
        seq_number += 1
        # now, look at the list slice starting with each max number to find
        # the NEXT highest number
        if len(max_nums) == 1:
            # only ONE of the values in the sequence is the highest number...
            if max_nums[0] == (len(nums) - 1):
                # if the max value is the LAST number in the sequence, then it can
                # only be the second digit
                #print(f'   (1) check slice {nums[:-1]}')
                second_digit = nums[max_nums[0]]
                first_digit = max(nums[:-1])
            else:
                # check the slice of numbers from the highest value's index
                # to the end of the sequence and get the max value
                #print(f'   (2) check slice {nums[max_nums[0]+1:]}')
                first_digit = nums[max_nums[0]]
                second_digit = max(nums[max_nums[0]+1:])
            highest_joltage = (first_digit * 10) + second_digit
        else:
            # the maximum joltage is the highest value as a double digit (because it's repeated)
            highest_joltage = nums[max_nums[0]] * 10 + nums[max_nums[0]]
        #print(f'   --> highest joltage = {highest_joltage}')
        total_joltage += highest_joltage
    return total_joltage

def part_2(input_lines) -> int:
    """ AoC Part 2 Solution: test answer = 3121910778619, answer = 173161749617495  """
    total_joltage = 0
    seq_number = 1
    REQ_BATT_LEN = 12
    for line in input_lines:
        full_sequence = list(map(int, list(line)))
        print(f'testing sequence {seq_number}: {line}')
        seq_number += 1

        # first, find the highest value that occurs BEFORE the last REQ_BATT_LEN
        # valules of the sequence
        joltage_str = ''
        full_start_index = 0
        end_index = -(REQ_BATT_LEN - 1)
        this_sequence = full_sequence[full_start_index:end_index]
        while len(joltage_str) < REQ_BATT_LEN:
            max_nums = maxelements(this_sequence)
            joltage_str = joltage_str + str(this_sequence[max_nums[0]])
            end_index += 1
            full_start_index = full_start_index + max_nums[0] + 1
            if end_index < 0:
                this_sequence = full_sequence[full_start_index:end_index]
            else:
                this_sequence = full_sequence[full_start_index:]
            print(f'\tmax value at {max_nums[0]}, joltage = {joltage_str}')
        max_joltage = int(joltage_str)
        print(f'\tmax joltage {max_joltage}')
        total_joltage += max_joltage
    return total_joltage

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
    answer_1 = part_1(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer_1}')

    answer_2 = part_2(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer_2}')
