#----------------------------------------------------------
# AoC 2024 Day 5
#----------------------------------------------------------
from pathlib import Path


def updatesAreValid(pages, rules) -> bool:
    # check each page against the rules to make sure that 
    # pages are not out of order
    for i in range(1, len(pages)):
        check_page = pages[i]
        for j in range(0, i):
            if check_page in rules:
                if pages[j] in rules[check_page]:
                    # found a page that should come after the given page
                    return False
    return True

def reorderPages(pages, rules):
    # check the pages against the rules to find which rule is broken
    # then reorder to fix it
    for i in range(1, len(pages)):
        check_page = pages[i]
        for j in range(0, i):
            if check_page in rules:
                if pages[j] in rules[check_page]:
                    # rule is broken, so fix it and check it
                    pages[i], pages[j] = pages[j], pages[i]
                    if updatesAreValid(pages, rules):
                        # we're done
                        return pages
                    else:
                        reorderPages(pages, rules)
                        break
    return pages

def part_1(input_lines) -> int:
    middle_total = 0
    rules = {}
    reading_rules = True
    for line in input_lines:
        # read rules until we get a blank line
        if len(line) == 0:
            reading_rules = False
            continue
        if reading_rules:
            page_key, page_after = map(int, line.split('|'))
            if page_key in rules:
                rules[page_key].append(page_after)
            else:
                rules[page_key] = [page_after]
        else:
            pages = list(map(int, line.split(',')))
            if updatesAreValid(pages, rules):
                middle = int((len(pages) - 1)/2)
                #print(f"line: {line} is valid! middle = {pages[middle]}")
                middle_total += pages[middle]
            else:
                #print(f"line: {line} is NOT valid!")
                continue
    return middle_total

def part_2(input_lines) -> int:
    middle_total = 0
    rules = {}
    reading_rules = True
    for line in input_lines:
        # read rules until we get a blank line
        if len(line) == 0:
            reading_rules = False
            continue
        if reading_rules:
            page_key, page_after = map(int, line.split('|'))
            if page_key in rules:
                rules[page_key].append(page_after)
            else:
                rules[page_key] = [page_after]
        else:
            pages = list(map(int, line.split(',')))
            if updatesAreValid(pages, rules):
                #print(f"line: {line} is valid, but we're not using it")
                continue
            else:
                fixed_pages = reorderPages(pages, rules)
                middle = int((len(fixed_pages) - 1)/2)
                #print(f"fixed line: {fixed_pages} - middle = {pages[middle]}")
                middle_total += pages[middle]
    return middle_total

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
    