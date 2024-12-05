#----------------------------------------------------------
# AoC 2024 Day 3
#----------------------------------------------------------
from pathlib import Path
import re


def part_1(input_lines) -> int:
    total = 0
    expression1 = R"(mul\(\d+,\d+\))"
    pattern = re.compile(expression1)
    expression2 = R"\d+,\d+"
    numbers = re.compile(expression2)
    for line in input_lines:
        ops = pattern.findall(line)
        #print(ops)
        for op in ops:
            a,b = map(int, numbers.findall(op)[0].split(','))
            total += a * b
            #print(f"a,b: {a}, {b}")
    return total

def part_2(input_lines) -> int:
    total = 0
    # finds "mul(xx,yy)" -or- "do()" -or- "don't"
    expression1 = R"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))"
    pattern = re.compile(expression1)
    expression2 = R"\d+,\d+"
    numbers = re.compile(expression2)

    mul_is_enabled = True
    for line in input_lines:
        op_iter = pattern.finditer(line)
        for op in op_iter:
            #print(f"operation at {op.start()}: {op.group()}")
            if op.group() == "don't()":
                mul_is_enabled = False
            elif op.group() == "do()":
                mul_is_enabled = True
            else:
                if mul_is_enabled:
                    a,b = map(int, numbers.findall(op.group())[0].split(','))
                    total += a * b
    return total


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
    