#----------------------------------------------------------
# AoC 2024 Day 4
#----------------------------------------------------------
from pathlib import Path
import re


def totalXmas(line) -> int:
    total_xmas = len([m.start() for m in re.finditer('XMAS', line)])
    total_samx = len([m.start() for m in re.finditer('SAMX', line)])
    return total_xmas + total_samx

def rotateInput90(input_lines):
    # convert each line to a list so we get a 2D array of lists
    twoD_array = []
    for line in input_lines:
        twoD_array.append(list(line))
    # now rotate it
    rotated_array = zip(*twoD_array[::-1])
    # and collapse it back to strings
    rotated_lines = []
    for list_row in rotated_array:
        rotated_lines.append(''.join(list_row))
    #print(f"rotated 90: {rotated_lines}")
    return rotated_lines

def rotateInput45(input_lines):
    twoD_array = []
    for line in input_lines:
        twoD_array.append(list(line))
    
    # from: https://www.geeksforgeeks.org/python3-program-for-rotate-matrix-by-45-degrees/
    n = len(input_lines)
    m = len(input_lines[0])
    rotated_array = []
    # Counter Variable
    ctr = 0
    while(ctr < 2 * n-1):
        new_line = []
        new_line.append(list(" "*abs(n-ctr-1)))
        lst = []

        # Iterate [0, m]
        for i in range(m):

                # Iterate [0, n]
            for j in range(n):

                # Diagonal Elements
                # Condition
                if i + j == ctr:

                    # Appending the
                    # Diagonal Elements
                    lst.append(twoD_array[i][j])

        # Printing reversed Diagonal
        # Elements
        lst.reverse()
        rotated_array.append(lst)
        ctr += 1

    # and collapse it back to strings
    rotated_lines = []
    for list_row in rotated_array:
        rotated_lines.append(''.join(list_row))
    #print(f"rotated 45: {rotated_lines}")
    return rotated_lines

def part_1(input_lines) -> int:
    count_horizontal = 0
    for line in input_lines:
        count_horizontal += totalXmas(line)
    # rotate the 2D array by 90 degrees so we can count the vertical
    count_vertical = 0
    rotated_lines = rotateInput90(input_lines)
    for line in rotated_lines:
        count_vertical += totalXmas(line)
    # rotate the original 2D array by 45 degrees so we can count 
    # the diagonal in one direction
    count_diagonal = 0
    rotated_lines = rotateInput45(input_lines)
    for line in rotated_lines:
        count_diagonal += totalXmas(line)
    # finally rotate the original by 90 then by 45 to count
    # the other diagonal
    rotated_lines = rotateInput90(input_lines)
    rotated_lines = rotateInput45(rotated_lines)
    for line in rotated_lines:
        count_diagonal += totalXmas(line)
    return count_horizontal + count_vertical + count_diagonal

def isXmas(input_lines, row, a_pos) -> int:
    if a_pos == 0 or a_pos == (len(input_lines[row]) - 1):
        return 0
    #print(f"line: {input_lines[row]}, row: {row}, a_pos: {a_pos}")
    diag1 = input_lines[row-1][a_pos-1] + input_lines[row][a_pos] + input_lines[row+1][a_pos+1]
    diag2 = input_lines[row+1][a_pos-1] + input_lines[row][a_pos] + input_lines[row-1][a_pos+1]
    if (diag1 == "MAS" or diag1 == "SAM") and (diag2 == "MAS" or diag2 == "SAM"):
        #print(f"diag1: {diag1}, diag2: {diag2} --> X-MAS!")
        return 1
    else:
        #print(f"diag1: {diag1}, diag2: {diag2} --> nope")
        return 0

def part_2(input_lines) -> int:
    xmas_count = 0
    for i in range(1, len(input_lines) - 1):
        a_pos = input_lines[i].find('A')
        while a_pos >= 0:
            xmas_count += isXmas(input_lines, i, a_pos)
            a_pos = input_lines[i].find('A', a_pos + 1)
    return xmas_count

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
    