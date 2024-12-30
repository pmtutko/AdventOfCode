#----------------------------------------------------------
# AoC 2024 Day 8
#----------------------------------------------------------
from pathlib import Path
import logging
from itertools import combinations
import numpy as np
from scipy.spatial import distance


class Point:
    def __init__(self, new_freq):
        self._freq = new_freq
        self._antinode_count = 0

    def isEmpty(self) -> bool:
        return self._freq == '.'

    def hasAntenna(self) -> bool:
        return (self._freq != '.' and self._freq != '#')

    def addAntiNode(self):
        self._antinode_count += 1
        self._freq = '#'

    @property
    def freq(self):
        return self._freq

    @property
    def antinodeCount(self) -> int:
        return self._antinode_count


class Area:
    def __init__(self, input_lines):
        self._this_area = []
        for line in input_lines:
            this_row = list(Point(p) for p in list(line))
            self._this_area.append(this_row)
        self._width = len(self._this_area[0])
        self._height = len(self._this_area)

    def locateAntennas(self):
        self._antennas = {}
        for row, line in enumerate(self._this_area):
            for col, point in enumerate(line):
                if not point.isEmpty():
                    if point.freq not in self._antennas:
                        self._antennas[point.freq] = [(row,col)]
                    else:
                        self._antennas[point.freq].append((row,col))
        logging.debug(f'antennas: {self._antennas.items()}')

    def calcAntinodeLocations(self, freq, this_point, rise, run, which_side, limit_antinodes):
        node_x = this_point[0]
        node_y = this_point[1]
        still_in_area = True
        while still_in_area:
            if which_side == 1:
                node_x -= run
                node_y -= rise
            else:
                node_x += run
                node_y += rise
            if ((node_x >= 0 and node_x < self._width) and
                (node_y >= 0 and node_y < self._height)):
                self._this_area[node_x][node_y].addAntiNode()
                logging.debug(f'freq {freq} pair {this_point}: antinode at ({node_x}, {node_y})')
            else:
                still_in_area = False
            if limit_antinodes:
                still_in_area = False

    def placeAntinodes(self, limit_anitnodes=True):
        for freq in self._antennas:
            pairs = list(combinations(self._antennas[freq], 2))
            logging.debug(f'freq {freq}: {pairs}')
            for pair in pairs:
                pointA, pointB = pair
                rise = pointB[1] - pointA[1]
                run = pointB[0] - pointA[0]
                # place anitnode on this side
                self.calcAntinodeLocations(freq, pointA, rise, run, 1, limit_anitnodes)
                self.calcAntinodeLocations(freq, pointB, rise, run, 2, limit_anitnodes)
    
    def countAntinodes(self) -> int:
        total_count = 0
        for row in self._this_area:
            for point in row:
                if point.antinodeCount > 0:
                    total_count += 1
        return total_count
    
    def countNonEmpty(self) -> int:
        total_count = 0
        for row in self._this_area:
            for point in row:
                if not point.isEmpty():
                    total_count += 1
        return total_count
    
    def print(self):
        for row, line in enumerate(self._this_area):
            printed_row = f'Row {row}: '
            for col, point in enumerate(line):
                printed_row += point.freq
            logging.debug(printed_row)

def part_1(input_lines) -> int:
    # test answer = 14, answer = 367
    this_area = Area(input_lines)
    this_area.locateAntennas()
    this_area.placeAntinodes()
    return this_area.countAntinodes()

def part_2(input_lines) -> int:
    # test answer = 34, answer = 1285
    this_area = Area(input_lines)
    this_area.locateAntennas()
    this_area.placeAntinodes(limit_anitnodes=False)
    this_area.print()
    return this_area.countNonEmpty()

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
    