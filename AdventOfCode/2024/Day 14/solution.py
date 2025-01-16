#----------------------------------------------------------
# AoC 2024 Day 14
#----------------------------------------------------------
from pathlib import Path
import logging
import re
import itertools
import math


class Robot:
    # generates an ID for each separate machine
    robot_id_gen = itertools.count()

    def __init__(self, x0, y0, vx, vy, mapH, mapW):
        self._id = next(Robot.robot_id_gen)
        self._x0 = x0
        self._y0 = y0
        self._vx = vx    # + moves right, - moves left
        self._vy = vy    # + moves down, - moves up
        self._mapH = mapH
        self._mapW = mapW
        self._x = self._x0
        self._y = self._y0
        #logging.debug(f'Robot {self._id}: initial ({self._x}, {self._y}), velocity ({self._vx}, {self._vy})')

    @property
    def id(self) -> int:
        return self._id
    
    def getCoordinate(self):
        return (self._x, self._y)

    def takeSteps(self, seconds):
        # top left map corner is 0, 0
        for i in range(seconds):
            self._x += self._vx
            if self._x >= self._mapW:
                # wraparound
                self._x = self._x - self._mapW
            if self._x < 0:
                # wraparound
                self._x = self._mapW + self._x  # because x is negative
            self._y += self._vy
            if self._y >= self._mapH:
                # wraparound
                self._y = self._y - self._mapH
            if self._y < 0:
                # wraparound
                self._y = self._mapH + self._y  # because y is negative
            #logging.debug(f'Robot {self._id} took {i+1} steps and stopped at ({self._x}, {self._y})')
    
    def getPosition(self):
        return (self._x, self._y)
    
    def getQuadrant(self) -> int:
        quad = 0
        if self._x < int(self._mapW/2) and self._y < int(self._mapH/2):
            quad = 1
        elif self._x > int(self._mapW/2) and self._y < int(self._mapH/2):
            quad = 2
        elif self._x < int(self._mapW/2) and self._y > int(self._mapH/2):
            quad = 3
        elif self._x > int(self._mapW/2) and self._y > int(self._mapH/2):
            quad = 4
        logging.debug(f'Robot {self._id} at ({self._x}, {self._y}) in quad {quad}')
        return quad
    

class MapSpace:
    def __init__(self, mapH, mapW):
        self._mapH = mapH
        self._mapW = mapW
        self._total_steps = 0
        self._robots = []

    def addRobot(self, new_robot):
        self._robots.append(new_robot)

    def takeStep(self, seconds=1):
        for robot in self._robots:
            robot.takeSteps(seconds)
        self._total_steps += seconds
        
    def quadrantCounts(self):
        quad_totals = [0,0,0,0]
        for r in self._robots:
            quad = r.getQuadrant() - 1
            if quad >= 0:
                quad_totals[quad] = quad_totals[quad] + 1
        logging.debug(f'quad totals = {quad_totals}')
        return quad_totals
    
    def easterEggNotFound(self) -> bool:
        robot_points = []
        for r in self._robots:
            robot_points.append(r.getCoordinate())
        # if none of the points sits on top of another, see what the grid looks like
        no_doubles = True
        while no_doubles and len(robot_points) > 0:
            pt = robot_points.pop()
            if pt in robot_points:
                no_doubles = False
        if no_doubles:
            print(self.dumpGrid())
            return False
        else:
            return True
        '''
        grid = self.dumpGrid()
        grid_rows = grid.split('\n')
        count_list = []
        for r in range(len(grid_rows)):
            # find the first row with the top of the tree
            if grid_rows[r].count('X') == 1:
                # from here, check that each successive row has more trees
                previous_row = 1
                tree_row_count = 1
                for t in range(r+1, len(grid_rows)):
                    if grid_rows[t].count('X') - previous_row != 1:
                        break
                    else:
                        previous_row = grid_rows.count('X')
                        tree_row_count += 1
                        if tree_row_count > 10:
                            break
            elif grid_rows[r].count('X') > 1:
                # if we get here, then the grid won't be a tree
                break
        return True
        '''
    
    def currentStepCount(self) -> int:
        return self._total_steps
    
    def dumpGrid(self) -> str:
        # get a list of the robot points
        grid = ''
        robot_points = []
        for r in self._robots:
            robot_points.append(r.getCoordinate())
        for i in range(self._mapW):
            grid_row = ''
            for j in range(self._mapH):
                if (i,j) in robot_points:
                    grid_row += 'X'
                else:
                    grid_row += '.'
            grid += (grid_row + '\n')
        return grid

        

def part_1(input_lines) -> int:
    # test answer = 12, answer = 236628054
    mapspace = MapSpace(mapH=103, mapW=101)
    parse_robot = R"p\=(-?\d+),(-?\d+) v\=(-?\d+),(-?\d+)"
    re_robot = re.compile(parse_robot)
    for line in input_lines:
        x0, y0, vx, vy = map(int, re_robot.search(line).groups())
        mapspace.addRobot(Robot(x0, y0, vx, vy, mapH=103, mapW=101))
    mapspace.takeStep(100)
    quad_totals = mapspace.quadrantCounts()
    safety_factor = math.prod(quad_totals)
    return safety_factor

def part_2(input_lines) -> int:
    # test answer = yyy, answer = xxxx
    mapspace = MapSpace(mapH=103, mapW=101)
    parse_robot = R"p\=(-?\d+),(-?\d+) v\=(-?\d+),(-?\d+)"
    re_robot = re.compile(parse_robot)
    for line in input_lines:
        x0, y0, vx, vy = map(int, re_robot.search(line).groups())
        mapspace.addRobot(Robot(x0, y0, vx, vy, mapH=103, mapW=101))
    while mapspace.easterEggNotFound():
        mapspace.takeStep()
    return mapspace.currentStepCount()

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

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
    