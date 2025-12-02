"""MazeSolver holds the maze and the logic to solve it.
"""

import math
from node import Node, Direction


class MazeSolver:
    """ encapsulates the Maze and supporting operations to solve it"""

    def __init__(self, maze, start_pt, end_pt):
        # build a dictionary of the nodes
        self._unvisited_nodes = {}
        self._visited_nodes = {}
        self._start_pt = start_pt
        self._end_pt = end_pt
        for r, row in enumerate(maze):
            for c, pt in enumerate(row):
                if pt == 0:
                    # only keep the open spaces, not the walls
                    if (r,c) == start_pt:
                        self._start_node = Node(r,c)
                        self._start_node._score = 0
                        self._start_node._dir = Direction.EAST
                        self._unvisited_nodes[self._start_node.key] = self._start_node
                    else:
                        new_node = Node(r,c)
                        self._unvisited_nodes[new_node.key] = new_node
        self.find_adjacent_nodes()

    def find_adjacent_nodes(self):
        """Looks at all four possible positions to identify nodes and not walls."""
        # in the maze grid 1 == wall, 0 == open
        for node_key, this_node in self._unvisited_nodes.items():
            connected_nodes = [None, None, None, None, None] # index matches Direction value
            # the first index in the list is a dummy to force the direction indexes to match
            for i, key_offset in enumerate([(math.inf, math.inf), (-1,0), (0,1), (1,0), (0,-1)]):
                if key_offset != (math.inf, math.inf):
                    r, c = node_key
                    dr, dc = key_offset
                    if (r+dr,c+dc) in self._unvisited_nodes.keys():
                        connected_nodes[i] = self._unvisited_nodes[(r+dr,c+dc)]
            this_node.setAdjacent(connected_nodes)

    def visit_node(self, this_node, dir):
        this_node.visited = True
        this_node.dir = dir
        del self._unvisited_nodes[this_node.key]
        self._visited_nodes[this_node.key] = this_node

    def solve_by_dijkstra(self) -> int:
        # start at the beginning
        path_dir = Direction.EAST
        self._unvisited_nodes[self._start_node.key] = self._start_node
        while self._unvisited_nodes:
            current_node = self._unvisited_nodes.pop()
            if current_node.key in self._visited_nodes.keys():
                continue
            self.visit_node(current_node, path_dir)
            for neighbor_node in current_node.adjacent_nodes:
                cost_to_travel_to_neighbor, out_dir = neighbor_node.travel_cost(current_node.cost, in_dir)

        
