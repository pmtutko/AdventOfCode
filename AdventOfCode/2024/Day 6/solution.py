#----------------------------------------------------------
# AoC 2024 Day 6
#----------------------------------------------------------
from pathlib import Path
from itertools import cycle, islice, dropwhile
from enum import Enum
from copy import copy, deepcopy
import logging
import timeit

area_id = 100


class PositionType(Enum):
    START = '^'
    EMPTY = '.'
    BLOCKER = '#'
    TEMP_BLOCKER = 'O'
    VISITED = 'X'
    INVALID = 'Q'

class Direction(Enum):
    EAST = 'e'
    SOUTH = 's'
    WEST = 'w'
    NORTH = 'n'
    TURN_EAST = 'te'
    TURN_SOUTH = 'ts'
    TURN_WEST = 'tw'
    TURN_NORTH = 'tn'
    TURN_INVALID = 'xx'

    @classmethod
    def turn(self, dir):
        return_dir = Direction.TURN_INVALID
        if dir == Direction.EAST:
            return_dir = Direction.TURN_SOUTH
        elif dir == Direction.SOUTH:
            return_dir = Direction.TURN_WEST
        elif dir == Direction.WEST:
            return_dir = Direction.TURN_NORTH
        elif dir == Direction.NORTH:
            return_dir = Direction.TURN_EAST
        return return_dir

class AreaState(Enum):
    IN_AREA = 1
    OUT_OF_AREA = 2
    JOINED_EXISTING_PATH = 3

class DirectionCycle():
    def __init__(self, start_direction = Direction.NORTH):
        self._dirs = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        # rotate the directions until we're pointed the given direction
        logging.debug(f"start_direction: {start_direction}, current dir: {self._dirs[0]}")
        while start_direction != self._dirs[0]:
            self.next()
            #self._dirs = self._dirs[1:] + self._dirs[:1]

    def current(self) -> Direction:
        # the current direction is always the first element
        return self._dirs[0]
    
    def next(self):
        # rotate the list to keep the current direction first
        self._dirs = self._dirs[1:] + self._dirs[:1]

class Position:
    def __init__(self, r, c, pos_char):
        self._row = r
        self._col = c
        self._pos_char = ''
        self._pos_type = PositionType.INVALID
        if pos_char == PositionType.START.value:
            self._pos_type = PositionType.START
            self._pos_char = PositionType.START.value
        elif pos_char == PositionType.EMPTY.value:
            self._pos_type = PositionType.EMPTY
            self._pos_char = PositionType.EMPTY.value
        elif pos_char == PositionType.BLOCKER.value:
            self._pos_type = PositionType.BLOCKER
            self._pos_char = PositionType.BLOCKER.value
        self._visited = []

    @property
    def row(self) -> int:
        return self._row
    
    @property
    def col(self) -> int:
        return self._col

    @property
    def posType(self) -> PositionType:
        return self._pos_type

    def isStart(self) -> bool:
        return (self._pos_type == PositionType.START)
    
    def isEmpty(self) -> bool:
        return (self._pos_type == PositionType.EMPTY)
    
    def isBlocker(self) -> bool:
        return (self._pos_type in [PositionType.BLOCKER, PositionType.TEMP_BLOCKER])
        
    def setTempBlocker(self) -> bool:
        if self._pos_type == PositionType.START or self._pos_type == PositionType.BLOCKER:
            logging.debug(f'POSITION ERROR: cannot put a temporary blocker in the START or a BLOCKER position! ({self.row},{self.col})')
            return False
        elif self.wasVisited():
            logging.debug(f'POSITION ERROR: do not put a temporary blocker in a position that has been visited ({self.row},{self.col})')
            return False
        self._pos_type = PositionType.TEMP_BLOCKER
        self._pos_char = PositionType.TEMP_BLOCKER.value
        return True

    def char(self) -> str:
        # build a string of the directions visited (or not)
        if self._pos_type == PositionType.BLOCKER or self._pos_type == PositionType.TEMP_BLOCKER:
            return self._pos_type.value
        elif len(self._visited) == 0:
            return self._pos_char
        else:
            visit_text = ''
            for visit in self._visited:
                visit_text += visit.value + ','
            return visit_text[:-1]

    def visit(self, currrent_direction) -> bool:
        if self._pos_type == PositionType.BLOCKER or self._pos_type == PositionType.TEMP_BLOCKER:
            raise ValueError(f'POSITION ERROR: cannot visit a blocker position! ({self.row},{self.col})')
        # returns False if this is the first visit in the given direction
        # returns True if this is a re-visit
        if currrent_direction not in self._visited:
            self._visited.append(currrent_direction)
            return False
        else:
            return True

    def goingMyWay(self, current_direction) -> bool:
        # check the straight directions
        if (current_direction in self._visited):
            return True
        # check the turning directions
        if current_direction == Direction.NORTH and Direction.TURN_EAST in self._visited:
            return True
        if current_direction == Direction.EAST and Direction.TURN_SOUTH in self._visited:
            return True
        if current_direction == Direction.SOUTH and Direction.TURN_WEST in self._visited:
            return True
        if current_direction == Direction.WEST and Direction.TURN_NORTH in self._visited:
            return True
        return False
    
    def wasVisited(self) -> bool:
        return (len(self._visited) > 0)

    def __str__(self) -> str:
        return f"({self.row, self.col})"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
    

class Area:
    def __init__(self, input_lines) -> None:
        # assign an ID to this area for debugging
        global area_id
        area_id += 1
        self.id = area_id
        # create the area as a 2D array of Positions
        self._this_area = []
        for r, line in enumerate(input_lines):
            this_row = []
            for c, p in enumerate(list(line)):
                if p == '^':
                    self.starting_row, self.starting_col = r, c
                this_row.append(Position(r, c, p))
            self._this_area.append(this_row)
        self.starting_pos = self.getPosition(self.starting_row, self.starting_col)
        self._vector = Vector(self, self.starting_pos, DirectionCycle(Direction.NORTH))

    def print(self) -> None:
        print("****************************************************")
        for r, row in enumerate(self._this_area):
            col_txt = ''
            for col in row:
                col_txt += col.char().rjust(2)
            print(f"{r:3d}: {col_txt}")

    def getStartingPosition(self) -> Position:
        return self._this_area[self.starting_row][self.starting_col]

    def visitedCount(self) -> int:
        count = 0
        for r in range(self.height):
            for c in range(self.width):
                if self._this_area[r][c].wasVisited():
                    count += 1
        return count

    def placeTempBlocker(self, pos) -> bool:
        return self._this_area[pos.row][pos.col].setTempBlocker()

    @property
    def width(self) -> int:
        return len(self._this_area[0])
    
    @property
    def height(self) -> int:
        return len(self._this_area)
 
    def getPosition(self, r, c) -> Position:
        return self._this_area[r][c]

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class Vector:
    # this holds the state of where we are and where we're going next
    def __init__(self, area, pos, initial_dir_cycle=DirectionCycle(Direction.NORTH)):
        self._this_area = area
        self._pos = pos
        self._next_pos = self._pos
        self._dir = initial_dir_cycle
        self._in_out_of_area = AreaState.IN_AREA
        self._next_calc_row = -1
        self._next_calc_col = -1
        self.determineNextStep()

    @property
    def row(self) -> int:
        return self._pos.row
    
    @property
    def col(self) -> int:
        return self._pos.col
    
    @property
    def dir(self) -> Direction:
        return self._dir.current()

    @property
    def inOrOut(self) -> AreaState:
        return self._in_out_of_area

    def determineNextStep(self, check_joining_path=False):
        # without considering blockers or edges, where is the next position?
        # -- does not advance the current row/col position
        # -- does not update the Position in the area
        next_row = -1
        next_col = -1
        if self._dir.current() == Direction.NORTH:
            next_row, next_col = self._pos.row - 1, self._pos.col
        elif self._dir.current() == Direction.EAST:
            next_row, next_col = self._pos.row, self._pos.col + 1
        elif self._dir.current() == Direction.SOUTH:
            next_row, next_col = self._pos.row + 1, self._pos.col
        elif self._dir.current() == Direction.WEST:
            next_row, next_col = self._pos.row, self._pos.col - 1

        # are we still going to be in the area?
        if ((next_row < 0) or (next_row == self._this_area.height) or 
            (next_col < 0) or (next_col == self._this_area.width)):
            # we're out of the area, so we're done!
            logging.debug(f"VECTOR: Path Complete: left the area to the {self._dir.current().name} ({self._pos.row},{self._pos.col})")
            # left the area, mark as visited
            self._pos.visit(self._dir.current())
            self._in_out_of_area = AreaState.OUT_OF_AREA

        else:
            self._next_pos = self._this_area.getPosition(next_row, next_col)
            # are we joining an existing path going our way?
            if check_joining_path and self._next_pos.goingMyWay(self._dir.current()):
                # we've joined an existing path
                logging.debug(f"VECTOR: Path joined going {self._dir.current().name} at ({self._pos.row},{self._pos.col})")
                self._in_out_of_area = AreaState.JOINED_EXISTING_PATH
        return

    def getPosition(self) -> Position:
        return self._pos

    def getNextPosition(self) -> Position:
        return self._next_pos

    def advance(self, check_joining_path=False):
        # proceed in the current direction and respond to blockers and turns and edges
        # -- (may) change the current position to the next location along the current direction
        # -- updates the vacated position with the direction we're headed
        # -- if the next position is a blocker, stay in place and log that we've turned
        we_have_turned = False
        if self._next_pos.isBlocker():
            # we're blocked, so turn in place at the current position
            already_visited = self._pos.visit(Direction.turn(self._dir.current()))
            if not already_visited:
                self._dir.next()
                we_have_turned = True
            else:
                self._in_out_of_area = AreaState.JOINED_EXISTING_PATH
                return
        else:
            # not blocked, haven't been here before, so just mark as visited
            self._pos.visit(self._dir.current())
        # what's our next step?
        self.determineNextStep()
        if self._in_out_of_area == AreaState.OUT_OF_AREA:
            # left the area, mark as visited
            already_visited = self._pos.visit(self._dir.current())
            if already_visited:
                return
        elif self._in_out_of_area == AreaState.JOINED_EXISTING_PATH:
            return
        # now take the step and set up for the next step (unless it goes out of the area)
        if not we_have_turned:
            self._pos = self._this_area.getPosition(self._next_pos.row, self._next_pos.col)
            self.determineNextStep(check_joining_path)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


def part_1(input_lines) -> int:
    # test answer = 41, data answer = 5239
    p1_area = Area(input_lines)
    #p1_area.print()
    # now march!
    start_here = p1_area.getStartingPosition()
    the_path = Vector(p1_area, start_here)
    while the_path.inOrOut == AreaState.IN_AREA:
        the_path.advance()
        #area.print()
    #area.print()
    return p1_area.visitedCount()

def part_2(input_lines) -> int:
    # test answer = 6, data answer = 1753
    p2_area = Area(input_lines)
    # now march!
    blockers = []
    steps = 0
    start_here = p2_area.getStartingPosition()
    the_main_path = Vector(p2_area, start_here, DirectionCycle(Direction.NORTH))
    while the_main_path.inOrOut == AreaState.IN_AREA:
        the_main_path.advance()
        # using a copy of the area, drop a temporary blocker and
        # see what happens
        temp_area = deepcopy(p2_area)
        the_temp_path = Vector(temp_area, 
                               temp_area.getPosition(the_main_path.row, the_main_path.col),
                               DirectionCycle(the_main_path.dir))
        temp_blocker_position = the_temp_path.getNextPosition()
        # place the blocker if the position is open
        while temp_area.placeTempBlocker(temp_blocker_position) == False:
            the_temp_path.advance()
            temp_blocker_position = the_temp_path.getNextPosition()
        # using the valid temp blocker, bop til you drop
        logging.debug(f"in temp area, starting at {the_temp_path.getPosition()}, blocker at {temp_blocker_position}")
        steps += 1
        temp_print = False
        temp_steps = 0
        while the_temp_path.inOrOut == AreaState.IN_AREA:
            the_temp_path.advance(check_joining_path=True)
            temp_steps += 1
            print(f" Step: {steps}, blockers found: {len(blockers)}, temp steps: {temp_steps}\r", end='')
            if the_temp_path.inOrOut == AreaState.JOINED_EXISTING_PATH:
                blocker_at = (temp_blocker_position.row,temp_blocker_position.col)
                if blocker_at not in blockers:
                    blockers.append(blocker_at)
                break
            if temp_print:
                 temp_area.print()
    #p2_area.print()
    logging.debug(f"blocking positions:\n{blockers}")
    return len(blockers)


if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt')
    logging.info(f'reading from: {aoc_input}')
    #print(f'reading from: {aoc_input}')
  
    with aoc_input.open('r') as f:
       #lines = " ".join(line.rstrip() for line in file)
       lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer_1 = part_1(lines)
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(lines)
    print(f'part 2 answer: {answer_2}')
