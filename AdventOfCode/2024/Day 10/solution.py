#----------------------------------------------------------
# AoC 2024 Day 10
#----------------------------------------------------------
from pathlib import Path
import logging
from copy import copy


def checkPossibleBranches(map, position) -> list:
    step_number, r, c = position
    step_number += 1
    branch_check = []
    # check NORTH of the given position
    if (r - 1) >= 0:
        if map[r-1][c] != '.' and map[r][c] != '.':
            if (map[r-1][c] - map[r][c]) == 1:
                # log a branch point
                branch_check.append((step_number, r-1, c))
    # check SOUTH of the given position
    if (r + 1) < len(map):
        if map[r+1][c] != '.' and map[r][c] != '.':
            if (map[r+1][c] - map[r][c]) == 1:
                # log a branch point
                branch_check.append((step_number, r+1, c))
    # check EAST of the given position
    if (c + 1) < len(map[0]):
        if map[r][c+1] != '.' and map[r][c] != '.':
            if (map[r][c+1] - map[r][c]) == 1:
                # log a branch point
                branch_check.append((step_number, r, c+1))
    # check WEST of the given position
    if (c - 1) >= 0:
        if map[r][c-1] != '.' and map[r][c] != '.':
            if (map[r][c-1] - map[r][c]) == 1:
                # log a branch point
                branch_check.append((step_number, r, c-1))
    return branch_check

def followPathToPeakOnce(input_path, step_number, map, these_paths):
    MAX_ALT = 9
    this_path = copy(input_path)
    branch_points = checkPossibleBranches(map, this_path[-1])
    for step in branch_points:
        # may have to delete the last step if there were previous branch points
        if this_path[-1] in branch_points:
            this_path.pop()
        this_path.append(step)
        step_number, r, c = step
        if map[r][c] == MAX_ALT:
            # the altitude is MAX and it's not a peak we've already reached, we're done
            new_peak = True
            for one_path in these_paths:
                last_step, peak_r, peak_c = one_path[-1]
                if r == peak_r and c == peak_c:
                    # we've been here before, so skip this path
                    new_peak = False
            if new_peak:
                # append a copy so that we can still work with the existing path
                # in this iteration
                these_paths.append(copy(this_path))
        else:
            followPathToPeakOnce(this_path, step_number, map, these_paths)


def part_1(input_lines) -> int:
    # test answer = 36, answer = 688
    map = []
    trailheads = []
    for r, line in enumerate(input_lines):
        #map_row = [int(e) for e in list(line)]
        map_row = []
        for e in list(line):
            if e == '.':
                map_row.append(e)
            else:
                map_row.append(int(e))
        map.append(map_row)
        for c, elevation in enumerate(map_row):
            if elevation == 0:
                trailheads.append((r,c))

    branch_points = []
    all_paths = []
    for trailhead in trailheads:
        paths_from_this_trailhead = []
        # path is a triple:  (step number, row, column)
        the_path = [(1, trailhead[0], trailhead[1])]
        followPathToPeakOnce(the_path, 0, map, paths_from_this_trailhead)
        logging.debug(f'from trailhead {trailhead}: found {len(paths_from_this_trailhead)} paths')
        for path in paths_from_this_trailhead:
            logging.debug(path)
        all_paths += paths_from_this_trailhead
    return len(all_paths)


def followPathToPeakScore(input_path, step_number, map, these_peaks):
    MAX_ALT = 9
    this_path = copy(input_path)
    branch_points = checkPossibleBranches(map, this_path[-1])
    for step in branch_points:
        # may have to delete the last step if there were previous branch points
        if this_path[-1] in branch_points:
            this_path.pop()
        this_path.append(step)
        step_number, r, c = step
        if map[r][c] == MAX_ALT:
            # the altitude is MAX and it's not a peak we've already reached, we're done
            if (r,c) in these_peaks.keys():
                these_peaks[(r,c)] += 1
            else:
                these_peaks[(r,c)] = 1
        else:
            followPathToPeakScore(this_path, step_number, map, these_peaks)

def part_2(input_lines) -> int:
    # test answer = 81, answer = xxxx
    map = []
    trailheads = []
    for r, line in enumerate(input_lines):
        #map_row = [int(e) for e in list(line)]
        map_row = []
        for e in list(line):
            if e == '.':
                map_row.append(e)
            else:
                map_row.append(int(e))
        map.append(map_row)
        for c, elevation in enumerate(map_row):
            if elevation == 0:
                trailheads.append((r,c))

    branch_points = []
    all_paths = []
    total_rating = 0
    for trailhead in trailheads:
        peaks_from_this_trailhead = {}
        # path is a triple:  (step number, row, column)
        the_path = [(1, trailhead[0], trailhead[1])]
        followPathToPeakScore(the_path, 0, map, peaks_from_this_trailhead)
        logging.debug(f'from trailhead {trailhead}: found {len(peaks_from_this_trailhead)} peaks')
        for peak in peaks_from_this_trailhead.keys():
            r, c = peak
            logging.debug(f'peak at ({r}, {c}) has a rating of {peaks_from_this_trailhead[peak]}')
            total_rating += peaks_from_this_trailhead[peak]
    return total_rating

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
    