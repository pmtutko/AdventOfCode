#----------------------------------------------------------
# AoC 2024 Day12
#----------------------------------------------------------
from pathlib import Path
import logging
from enum import Enum
import itertools


UNASSIGNED_ID = -1

class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

class Point:
    def __init__(self, value, row, col):
        self._value = value
        self._row = row
        self._col = col
        self._edges = [False, False, False, False]                                  # n, s, e, w
        self._sides = [UNASSIGNED_ID, UNASSIGNED_ID, UNASSIGNED_ID, UNASSIGNED_ID]  # n, s, e, w
        self._area_id = UNASSIGNED_ID

    def getCoordinate(self):
        return (self._row, self._col)
    
    @property
    def value(self):
        return self._value

    @property
    def areaID(self):
        return self._area_id
    
    @areaID.setter
    def areaID(self, area_id):
        self._area_id = area_id

    @property
    def beenMapped(self) -> bool:
        return self._area_id != UNASSIGNED_ID
    
    def setEdge(self, dir):
        self._edges[dir.value] = True

    def edgeCount(self) -> int:
        count = 0
        for e in Direction:
            if self._edges[e.value]:
                count += 1
        return count
    
    def hasSide(self, side_id) -> bool:
        return self._sides[side_id.value] != UNASSIGNED_ID

    def setSide(self, dir, side_id):
        if side_id not in self._sides:
            self._sides[dir.value] = side_id

    def getSide(self, dir) -> int:
        return self._sides[dir.value]
    
    def getSides(self):
        return self._sides
    
    def __str__(self):
        return f'({self._row:2d}, {self._col:2d}) - {self._value}: Area ID = {self._area_id}, edges = {self.edgeCount()} [{self._sides}]'


class Area:
    # generates an ID for each separate area and side
    area_id_gen = itertools.count()
    side_id_gen = itertools.count()

    def __init__(self, starting_point):
        self._area = [starting_point]
        self._value = starting_point.value
        self._areaID = next(self.area_id_gen)
        self._start = starting_point
        self._start.areaID = self._areaID

    def startingPoint(self):
        return self._start

    def addPoint(self, new_point):
        new_point.id = self._areaID
        self._area.append(new_point)

    @property
    def id(self):
        return self._areaID
    
    @id.setter
    def id(self, new_id):
        self._areaID = new_id

    def perimeter(self) -> int:
        total = 0
        for pt in self._area:
            total += pt.edgeCount()
        return total
    
    def size(self) -> int:
        return len(self._area)
    
    def price(self) -> int:
        return (self.size() * self.perimeter())
    
    def bulkPrice(self) -> int:
        return (self.size() * self.sideCount())
    
    def findPoint(self, target_r, target_c) -> Point:
        for pt in self._area:
            r, c = pt.getCoordinate()
            if r == target_r and c == target_c:
                return pt
        return None
    
    def exploreSides(self):
        points = []
        for pt in self._area:
            points.append(pt.getCoordinate())
        sorted_points = sorted(points, key=lambda tup: (tup[0],tup[1]))
        # for each point in the area, determine which are adjacent
        for this_coordinate in sorted_points:
            r, c = this_coordinate
            this_point = self.findPoint(r, c)

            # look aheads for this point. pts may be None if they don't exist in this area
            north_pt = self.findPoint(r-1, c)
            south_pt = self.findPoint(r+1, c)
            east_pt = self.findPoint(r, c+1)
            west_pt = self.findPoint(r, c-1)

            # what's to the west?
            if not west_pt:
                # nothing to the west of this point, so it's a side. But it may be a
                # continuation of a side from the north only (because it's sorted)
                # for a common west side
                if north_pt:
                    if north_pt.getSide(Direction.West) != UNASSIGNED_ID:
                        # continue the same side
                        this_point.setSide(Direction.West, north_pt.getSide(Direction.West))
                    else:
                        # it's a new side
                        this_point.setSide(Direction.West, next(Area.side_id_gen))
                elif this_point.getSide(Direction.West) == UNASSIGNED_ID:
                    # it's a new side
                    this_point.setSide(Direction.West, next(Area.side_id_gen))
            else:
                # the point to the west is in the area, so leave the west edge unassigned
                this_point.setSide(Direction.West, UNASSIGNED_ID)


            # what's to the north?
            if not north_pt:
                # nothing to the north of this point, so it's a side. but which side?
                # check west only (because it's sorted) for a point with a top side
                if west_pt:
                    if west_pt.getSide(Direction.North) != UNASSIGNED_ID:
                        # continue the same side
                        this_point.setSide(Direction.North, west_pt.getSide(Direction.North))
                    else:
                        # it's a new side
                        this_point.setSide(Direction.North, next(Area.side_id_gen))
                else:
                    # it's a new side
                    this_point.setSide(Direction.North, next(Area.side_id_gen))
            else:
                # the point to the north is in the area, so we might share
                # the same left or right side
                if (north_pt.getSide(Direction.West) != UNASSIGNED_ID) and not west_pt:
                    # only continue the west side from point to the north if there's 
                    # not another point to the west on this row
                    this_point.setSide(Direction.West, north_pt.getSide(Direction.West))
                elif (north_pt.getSide(Direction.West) != UNASSIGNED_ID) and west_pt:
                    # the point to the north has a west side, but this point doesn't
                    this_point.setSide(Direction.West, UNASSIGNED_ID)
                else:
                    # the point above must be an interior point, but this point may
                    # have a side to the west
                    if not west_pt:
                        # nothing to the west, set a new side
                        this_point.setSide(Direction.West, next(Area.side_id_gen))
                if north_pt.getSide(Direction.East) != UNASSIGNED_ID and not east_pt:
                    # only continue the east side from point to the north if there's 
                    # not another point to the east on this row
                    this_point.setSide(Direction.East, north_pt.getSide(Direction.East))
                elif (north_pt.getSide(Direction.East) != UNASSIGNED_ID) and east_pt:
                    # the point to the north has a east side, but this point doesn't
                    this_point.setSide(Direction.East, UNASSIGNED_ID)
                else:
                    # the point above must be an interior point, so check the point
                    # to the east
                    if not east_pt:
                        # nothing to the east, set a new side
                        this_point.setSide(Direction.East, next(Area.side_id_gen))

            # what's to the south?
            if not south_pt:
                # nothing to the south of this point, so it's a side. but which side?
                # check west only (because it's sorted) for a point with a bottom side
                if west_pt:
                    if west_pt.getSide(Direction.South) != UNASSIGNED_ID:
                        # continue the same side
                        this_point.setSide(Direction.South, west_pt.getSide(Direction.South))
                    else:
                        # it's a new side
                        this_point.setSide(Direction.South, next(Area.side_id_gen))
                else:
                    # it's a new side
                    this_point.setSide(Direction.South, next(Area.side_id_gen))
            else:
                # the point to the south is in the area, so this point's bottom 
                # edge is unassigned
                 this_point.setSide(Direction.South, UNASSIGNED_ID)
            # what's to the east?
            if not east_pt:
                # nothing to the east of this point, so it's a side. 
                # --- we checked the point above for the same value, so if we're here,
                #     just assign a new side ID if it's unassigned
                if this_point.getSide(Direction.East) == UNASSIGNED_ID:
                    this_point.setSide(Direction.East, next(Area.side_id_gen))
        return
    
    def sideCount(self) -> int:
        # assumes that exploreSides has already been called
        unique_side_ids = []
        for pt in self._area:
            for side in pt.getSides():
                if side != UNASSIGNED_ID and side not in unique_side_ids:
                    unique_side_ids.append(side)
        return len(unique_side_ids)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        for p in self._area:
            yield p

    def __str__(self):
        return (f'Area {self._areaID} value {self._value}: size = {self.size()}, ' +
                f'perimeter = {self.perimeter()}, price = {self.price()}, ' +
                f'side count = {self.sideCount()}, bulk price = {self.bulkPrice()}')
    
    def dump(self):
        area_info = f'Area {self._areaID}:\n'
        for pt in self._area:
            area_info += f'\t{pt}\n'
        return area_info



class Map:
    def __init__(self, input_lines):
        self._map = []
        self._areas = []
        self._area_id = 1
        for r, line in enumerate(input_lines):
            point_row = []
            for c, p in enumerate(list(line)):
                point = Point(p, r, c)
                point_row.append(point)
            self._map.append(point_row)

    def explorePoint(self, this_point, the_area):
        # Assigns the given point to the area and checks the surrounding
        # points for:
        #    - do they have the same value?
        #    - have they already been mapped?
        #    - defines the edges of the given point
        # Returns a list of adjoining points that have the 
        # same value. May return an empty list if no adjacent
        # points have the same value (or have already been mapped).
        if this_point != the_area.startingPoint():
            this_point.areaID = the_area.id
            the_area.addPoint(this_point)
        r, c = this_point.getCoordinate()
        next_points = []
        # what's to the North?
        if r == 0:
            this_point.setEdge(Direction.North)
        else:
            north_point = self._map[r-1][c]
            if north_point.value == this_point.value and not north_point.beenMapped:
                next_points.append(north_point)
            elif north_point.value != this_point.value:
                this_point.setEdge(Direction.North)
        # what's to the South?
        if r == (len(self._map) - 1):
            this_point.setEdge(Direction.South)
        else:
            south_point = self._map[r+1][c]
            if south_point.value == this_point.value and not south_point.beenMapped:
                next_points.append(south_point)
            elif south_point.value != this_point.value:
                this_point.setEdge(Direction.South)
        # What's to the West?
        if c == 0:
            this_point.setEdge(Direction.West)
        else:
            west_point = self._map[r][c-1]
            if west_point.value == this_point.value and not west_point.beenMapped:
                next_points.append(west_point)
            elif west_point.value != this_point.value:
                this_point.setEdge(Direction.West)
        # What's to the East?
        if c == (len(self._map[0]) - 1):
            this_point.setEdge(Direction.East)
        else:
            east_point = self._map[r][c+1]
            if east_point.value == this_point.value and not east_point.beenMapped:
                next_points.append(east_point)
            elif east_point.value != this_point.value:
                this_point.setEdge(Direction.East)
        return next_points
    
    def exploreSides(self, this_area):
        # Accepts a defined area and explores each point to determine if it's
        # a part of one or more common sides. Each point carries a list of the
        # sides of which it's a member
        sides_in_use = []
        for p in this_area:
            r, c = p.getCoordinate()
            # what's to the North?
            if r == 0:
                if p.getSide(Direction.North) == UNASSIGNED_ID:
                    p.addSide(Direction.North, next(Area.side_id_gen))
            else:
                north_point = self._map[r-1][c]
                if north_point.value != p.value:
                    if p.getSide(Direction.North) == UNASSIGNED_ID:
                        # the point to the North is not in this area
                        p.addSide(Direction.North, next(Area.side_id_gen))
                    else:
                        ...
            # what's to the East?
            if c == (len(self._map[0]) - 1):
                if p.getSide(Direction.East) == UNASSIGNED_ID:
                    p.addSide(Direction.East, next(Area.side_id_gen))
            else:
                east_point = self._map[r][c+1]
                if east_point.value != p.value:
                    if p.getSide(Direction.East) == UNASSIGNED_ID:
                        p.addSide(Direction.East, next(Area.side_id_gen))
                else:
                    ...
            # what's to the South?
            if r == (len(self._map) - 1):
                if p.getSide(Direction.South) == UNASSIGNED_ID:
                    p.addSide(Direction.South, next(Area.side_id_gen))
            else:
                south_point = self._map[r+1][c]
                if south_point.value != p.value:
                    if p.getSide(Direction.South) == UNASSIGNED_ID:
                        p.addSide(Direction.South, next(Area.side_id_gen))
                else:
                    ...
            # what's to the West?
            if c == 0:
                if p.getSide(Direction.West) == UNASSIGNED_ID:
                    p.addSide(Direction.West, next(Area.side_id_gen))
            else:
                west_point = self._map[r][c-1]
                if west_point.value != p.value:
                    if p.getSide(Direction.West) == UNASSIGNED_ID:
                        p.addSide(Direction.West, next(Area.side_id_gen))
                else:
                    ...


    def fillThisArea(self, this_area):
        this_point = this_area.startingPoint()
        next_points = self.explorePoint(this_point, this_area)
        while len(next_points) > 0:
            next_point = next_points.pop()
            if not next_point.beenMapped:
                more_points = self.explorePoint(next_point, this_area)
                logging.debug(f'    added point {next_point}')
                next_points += more_points
                

    def defineAreas(self):
        for r, row in enumerate(self._map):
            for c, this_point in enumerate(row):
                if not this_point.beenMapped:
                    new_area = Area(this_point)
                    logging.debug(f'Mapping Area {new_area.id}: starting at {this_point}')
                    self.fillThisArea(new_area)
                    self._areas.append(new_area)
        logging.debug(f'there are {len(self._areas)} areas in the map')
        for a in self._areas:
            a.exploreSides()
            logging.debug(f'{a}')
            logging.debug(a.dump())

    def priceAreas(self, use_bulk_price=False) -> int:
        total_price = 0
        for a in self._areas:
            if use_bulk_price:
                total_price += a.bulkPrice()
            else:
                total_price += a.price()
        return total_price


def part_1(my_map) -> int:
    # test answer = 1930, answer = 1352976
    return my_map.priceAreas()

def part_2(my_map) -> int:
    # test answer = 1206, answer = 808796
    return my_map.priceAreas(use_bulk_price=True)

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

    my_map = Map(lines)
    my_map.defineAreas()

    answer_1 = part_1(my_map)
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(my_map)
    print(f'part 2 answer: {answer_2}')
    