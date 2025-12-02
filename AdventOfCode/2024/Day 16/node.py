"""Defines Node and Direction classes.

Each node knows where it is and the other nodes that are adjacent. 
Given the direction of travel, each node can supply the cost to
travel that path.
"""

import math
from enum import Enum
from functools import cached_property
from dataclasses import dataclass

class Direction(Enum):
    """Establishes a common terminology and values for path direction."""
    UNDEFINED = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


def opposite(path_dir) -> Direction:
    """Helper function for the Direction class
    Returns the opposite direction from the one given.
    """
    if path_dir == Direction.UNDEFINED.value:
        return Direction.UNDEFINED.value
    if path_dir == Direction.NORTH.value:
        return Direction.SOUTH.value
    if path_dir == Direction.SOUTH.value:
        return Direction.NORTH.value
    if path_dir == Direction.EAST.value:
        return Direction.WEST.value
    if path_dir == Direction.WEST.value:
        return Direction.EAST.value
    return Direction.UNDEFINED.value

def rotate90(path_dir, cw=True):
    """Helper function for the Direction class.
    Returns the direction rotated from the given direction.
    """
    if path_dir == Direction.UNDEFINED.value:
        return Direction.UNDEFINED.value
    if path_dir == Direction.NORTH.value:
        if cw:
            return Direction.EAST.value
        return Direction.WEST.value
    if path_dir == Direction.SOUTH.value:
        if cw:
            return Direction.WEST.value
        return Direction.EAST.value
    if path_dir == Direction.EAST.value:
        if cw:
            return Direction.SOUTH.value
        return Direction.NORTH.value
    if path_dir == Direction.WEST.value:
        if cw:
            return Direction.NORTH.value
        return Direction.SOUTH.value
    return Direction.UNDEFINED.value

@dataclass
class NodeCost:
    """ the cost calculation is dependent upon the direction of travel
        both incoming and outgoing, i.e. there is an additional cost
        if the path turns
    """
    STRAIGHT_COST = 1
    TURN_COST = 1000
    incoming_dir: Direction
    outgoing_dir: Direction
    cost: int


class Node:
    """ Defines a node in a directed graph.
    Each node in the graph knows its own location and the location
    of its adjacent neighbors only
    """

    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.dir = Direction.UNDEFINED
        self.score = math.inf
        self.visited = False
        # index matches Direction value
        self.adjacent_nodes = [None, None, None, None, None]
        self.costs = []

    def calculate_edge_costs(self, incoming_path_dir, dest_node) -> int:
        """Given the incoming direction, calculates the cost of 
        turning or going straight.
        """
        if dest_node in self.adjacent_nodes:


    @cached_property
    def key(self):
        """Returns a tuple (r,c) to be used as the dictionary key."""
        return (self.row, self.col)
