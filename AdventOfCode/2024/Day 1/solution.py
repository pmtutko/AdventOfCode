#----------------------------------------------------------
# AoC 2024 Day 1
#----------------------------------------------------------
from pathlib import Path

def part_1(input_lines) -> int:
    location_a = []
    location_b = []
    for line in input_lines:
        a, b = map(int, line.split(maxsplit=1))
        location_a.append(a)
        location_b.append(b)
    location_a = sorted(location_a)
    location_b = sorted(location_b)
    total_distance = 0
    for a, b in zip(location_a, location_b):
        total_distance += abs(a - b)
    return total_distance

def part_2(input_lines) -> int:
    location_a = []
    location_b = {}
    for line in input_lines:
        a, b = map(int, line.split(maxsplit=1))
        location_a.append(a)
        if b in location_b:
            location_b[b] += 1
        else:
            location_b[b] = 1
    similarity_score = 0
    for location in location_a:
        if location in location_b:
            similarity_score += location * location_b[location]
    return similarity_score

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
    