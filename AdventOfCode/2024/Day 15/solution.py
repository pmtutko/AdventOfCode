#----------------------------------------------------------
# AoC 2024 Day 15
#----------------------------------------------------------
from pathlib import Path
import logging
import itertools
from enum import Enum
from copy import copy, deepcopy


class Direction(Enum):
    North = '^'
    East = '>'
    South = 'v'
    West = '<'


class PointType(Enum):
    Wall = '#'
    Empty = '.'
    Box = 'O'
    BoxLeft = '['
    BoxRight = ']'
    Robot = '@'


class Point:
    def __init__(self, x0, y0, this_point, type_two=False):
        # sets the initial location and kind of the object
        self._x = x0
        self._y = y0
        self._type = PointType(this_point)
        
    @property
    def type(self) -> PointType:
        return self._type
    
    @type.setter
    def type(self, new_type):
        self._type = new_type
    
    @property
    def dump(self) -> str:
        return self._type.value

    def getCoordinate(self):
        return (self._x, self._y)
    
    def getGPS(self) -> int:
        return (self._x * 100) + self._y


class Warehouse:
    def __init__(self, input_lines):
        self._map = []
        self._height = len(input_lines)
        self._width = len(input_lines[0])
        for r, line in enumerate(input_lines):
            this_row = []
            for c, point in enumerate(list(line)):
                this_point = Point(r, c, point)
                this_row.append(this_point)
                if this_point.type == PointType.Robot:
                    # capture the robot's initial position
                    self._robot_point = this_point
            self._map.append(this_row)

    def moveRobot(self, move):
        next_robot_point = self.getPoint(self._robot_point.getCoordinate(), move)
        if next_robot_point.type == PointType.Wall:
            # cannot move, so nothing to do
            pass
        elif next_robot_point.type == PointType.Empty:
            # nothing there, so move the robot into the spot
            self._robot_point.type = PointType.Empty
            next_robot_point.type = PointType.Robot
            self._robot_point = next_robot_point
        elif next_robot_point.type == PointType.Box:
            # can we push the box? are we pushing more than one box?
            # make a list of boxes to move 
            box_points = [next_robot_point]
            point_beyond_box = self.getPoint(next_robot_point.getCoordinate(), move)
            while point_beyond_box.type == PointType.Box:
                box_points.append(point_beyond_box)
                point_beyond_box = self.getPoint(point_beyond_box.getCoordinate(), move)
            if point_beyond_box.type == PointType.Empty:
                # we can move the boxes!
                point_beyond_box.type = PointType.Box
                # the first point in the list now holds the robot
                box_points[0].type = PointType.Robot
                self._robot_point.type = PointType.Empty
                self._robot_point = box_points[0]
            else:
                # it's a wall, nothing is moving in this direction
                pass

    def getPoint(self, coord, dir='') -> Point:
        # returns the point at the given location, or at the
        # location indicated by the direction
        r, c = coord
        if dir == '':
            return self._map[r][c]
        elif dir == Direction.North.value:
            return self._map[r-1][c]
        elif dir == Direction.South.value:
            return self._map[r+1][c]
        elif dir == Direction.West.value:
            return self._map[r][c-1]
        elif dir == Direction.East.value:
            return self._map[r][c+1]
        
    def boxGPSTotal(self) -> int:
        gpsTotal = 0
        for the_row in self._map:
            for pt in the_row:
                if pt.type == PointType.Box:
                    gpsTotal += pt.getGPS()
        return gpsTotal

    def dump(self) -> str:
        grid = ''
        for the_row in self._map:
            row_dump = ''
            for pt in the_row:
                row_dump += pt.dump
            grid += (row_dump + '\n')
        return grid

class Warehouse2:
    def __init__(self, input_lines):
        self._map = []
        for r, line in enumerate(input_lines):
            this_row = []
            c = 0
            for point in list(line):
                if point == '.':
                    this_point = Point(r, c, PointType.Empty)
                    this_row.append(this_point)
                    c += 1
                    this_point = Point(r, c, PointType.Empty)
                elif point == '#':
                    this_point = Point(r, c, PointType.Wall)
                    this_row.append(this_point)
                    c += 1
                    this_point = Point(r, c, PointType.Wall)
                elif point == 'O':
                    this_point = Point(r, c, PointType.BoxLeft)
                    this_row.append(this_point)
                    c += 1
                    this_point = Point(r, c, PointType.BoxRight)
                elif point == '@':
                    this_point = Point(r, c, PointType.Robot)
                    self._robot_point = this_point
                    this_row.append(this_point)
                    c += 1
                    this_point = Point(r, c, PointType.Empty)
                c += 1
                this_row.append(this_point)
            self._map.append(this_row)

    def moveRobot(self, move):
        next_robot_point = self.getPoint(self._robot_point.getCoordinate(), pt_width=1, dir=move)
        if next_robot_point.type == PointType.Wall:
            # cannot move, so nothing to do
            pass
        elif next_robot_point.type == PointType.Empty:
            # nothing there, so move the robot into the spot
            self._robot_point.type = PointType.Empty
            next_robot_point.type = PointType.Robot
            self._robot_point = next_robot_point
        elif next_robot_point.type == PointType.BoxLeft or next_robot_point.type == PointType.BoxRight:
            # moving east/west is different than moving north/south
            if move == Direction.West.value or move == Direction.East.value:
                # can we push the box? are we pushing more than one box?
                # make a list of boxes to move 
                all_boxes_to_move = [next_robot_point]
                point_beyond_box = self.getPoint(next_robot_point.getCoordinate(), pt_width=1, dir=move)
                while point_beyond_box.type == PointType.BoxLeft or point_beyond_box.type == PointType.BoxRight:
                    all_boxes_to_move.append(point_beyond_box)
                    point_beyond_box = self.getPoint(point_beyond_box.getCoordinate(), pt_width=1, dir=move)
                if point_beyond_box.type == PointType.Empty:
                    # we can move the boxes!
                    move_opposite = Direction.West.value
                    if move == Direction.West.value:
                        move_opposite = Direction.East.value
                    while all_boxes_to_move:
                        point_to_move = all_boxes_to_move.pop()
                        point_beyond_box.type = point_to_move.type
                        point_beyond_box = self.getPoint(point_beyond_box.getCoordinate(), pt_width=1, dir=move_opposite)
                    # ... and the robot
                    point_beyond_box.type = PointType.Robot
                    self._robot_point = point_beyond_box
                    point_beyond_box = self.getPoint(point_beyond_box.getCoordinate(), pt_width=1, dir=move_opposite)
                    point_beyond_box.type = PointType.Empty
                else:
                    # it's a wall, nothing is moving in this direction
                    pass
            else:
                # move the box(es) above or below to the north or south
                # capture the box we're pushing
                all_boxes_to_move = []
                boxes_this_row = [next_robot_point]
                if next_robot_point.type == PointType.BoxLeft:
                    boxes_this_row.append(self.getPoint(next_robot_point.getCoordinate(), dir=Direction.East.value))
                elif next_robot_point.type == PointType.BoxRight:
                    boxes_this_row.append(self.getPoint(next_robot_point.getCoordinate(), dir=Direction.West.value))
                else:
                    print('ERROR: illegal point type')
                # the box list has a separate list of boxes for each row of boxes beyond the robot
                all_boxes_to_move.append(boxes_this_row)
                # how many rows of boxes are beyond the box we're pushing
                move_blocked = False
                robotCanMoveBoxes = False
                while not move_blocked and not robotCanMoveBoxes:
                    boxes_this_row = []
                    for box in all_boxes_to_move[-1]:
                        # check beyond the box, half a box at a time
                        half_box_beyond = self.getPoint(box.getCoordinate(), dir=move)
                        if half_box_beyond not in boxes_this_row:
                            if half_box_beyond.type == PointType.BoxLeft or half_box_beyond.type == PointType.BoxRight:
                                boxes_this_row.append(half_box_beyond)
                                # get the other half of the box
                                if half_box_beyond.type == PointType.BoxLeft:
                                    move_opposite = Direction.East.value
                                else:
                                    move_opposite = Direction.West.value
                                half_box_beyond = self.getPoint(half_box_beyond.getCoordinate(), dir=move_opposite)
                                boxes_this_row.append(half_box_beyond)
                            elif half_box_beyond.type == PointType.Empty:
                                # keep checking
                                pass
                            elif half_box_beyond.type == PointType.Wall:
                                # we hit a wall, so can't add this box and can't move at all
                                move_blocked = True
                                break
                    if not move_blocked:
                        if boxes_this_row:
                            all_boxes_to_move.append(boxes_this_row)
                        else:
                            robotCanMoveBoxes = True
                if robotCanMoveBoxes:
                    # work backwards to keep it clean
                    for row_of_boxes in reversed(all_boxes_to_move):
                        for half_box in row_of_boxes:
                            move_here = self.getPoint(half_box.getCoordinate(), dir=move)
                            move_here.type = half_box.type
                            half_box.type = PointType.Empty
                    move_here = self.getPoint(self._robot_point.getCoordinate(), dir=move)
                    move_here.type = PointType.Robot
                    self._robot_point.type = PointType.Empty
                    self._robot_point = move_here


    def getPoint(self, coord, pt_width=1, dir='') -> Point:
        # returns the point at the given location, or at the
        # location indicated by the direction
        r, c = coord
        if dir == '':
            return self._map[r][c]
        elif dir == Direction.North.value:
            return self._map[r-pt_width][c]
        elif dir == Direction.South.value:
            return self._map[r+pt_width][c]
        elif dir == Direction.West.value:
            return self._map[r][c-1]
        elif dir == Direction.East.value:
            return self._map[r][c+1]
        
    def boxGPSTotal(self) -> int:
        gpsTotal = 0
        for the_row in self._map:
            for pt in the_row:
                if pt.type == PointType.BoxLeft:
                    gpsTotal += pt.getGPS()
        return gpsTotal

    def dump(self) -> str:
        grid = ''
        for the_row in self._map:
            row_dump = ''
            for pt in the_row:
                row_dump += pt.dump
            grid += (row_dump + '\n')
        return grid


def part_1(input_lines) -> int:
    # test answer = 10092, answer = 1406392
    warehouse = Warehouse(input_lines[:input_lines.index('')])
    logging.debug('----- Initial State Part 1')
    logging.debug('\n' + warehouse.dump() + '\n')
    for line in input_lines[input_lines.index('')+1:]:
        for move in list(line):
            warehouse.moveRobot(move)
            logging.debug(f'----- After moving {move}')
            logging.debug('\n' + warehouse.dump() + '\n')
    return warehouse.boxGPSTotal()


def part_2(input_lines) -> int:
    # test answer = 9021, answer = xxxx
    warehouse2 = Warehouse2(input_lines[:input_lines.index('')])
    logging.debug('----- Initial State Part 2')
    logging.debug('\n' + warehouse2.dump() + '\n')
    move_number = 0
    for line in input_lines[input_lines.index('')+1:]:
        for move in list(line):
            warehouse2.moveRobot(move)
            move_number += 1
            logging.debug(f'----- After move number {move_number}: {move}')
            logging.debug('\n' + warehouse2.dump() + '\n')
    return warehouse2.boxGPSTotal()

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
    