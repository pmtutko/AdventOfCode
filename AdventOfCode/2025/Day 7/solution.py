#----------------------------------------------------------
""" AoC 2025 Day 7                                      """
#----------------------------------------------------------
from pathlib import Path
import logging
import re
from collections import deque


AOC_DAY_NUMBER = 7


def print_this(manifold):
    """ pretty prints the given manifold """
    for row in manifold:
        print(row)

def part_1(input_lines) -> int:
    """ AoC Part 1 Solution: test answer = 21, answer = 1524  """
    manifold = input_lines.copy()
    beam_index = -1
    for row, line in enumerate(manifold):
        if row == 0:
            # start the beam...
            beam_index = manifold[row].find('S')
        elif row == 1:
            # place the first beam
            manifold[row] = manifold[row][:beam_index] + '|' + manifold[row][beam_index + 1:]
        elif row % 2 == 0:
            # splitters only occur on EVEN numbered rows, so locate them ... 
            splitters = [match.start() for match in re.finditer('\\^', manifold[row])]
            # ... and set the new beams
            for split_index in splitters:
                manifold[row] = manifold[row][:split_index - 1] + '|' + manifold[row][split_index:]
                manifold[row] = manifold[row][:split_index + 1] + '|' + manifold[row][split_index + 2:]
            # don't forget to continue any unsplit beams from the previous row
            beams = [match.start() for match in re.finditer('\\|', manifold[row - 1])]
            for beam_index in beams:
                if manifold[row][beam_index] == '.':
                    manifold[row] = manifold[row][:beam_index] + '|' + manifold[row][beam_index + 1:]
        elif row % 2 != 0:
            # the odd rows just mark the beam travel from the previous row, so
            # carry down the beams from above
            beams = [match.start() for match in re.finditer('\\|', manifold[row - 1])]
            for beam_index in beams:
                manifold[row] = manifold[row][:beam_index] + '|' + manifold[row][beam_index + 1:]
    #print_this(manifold)
    # now count how many splitters have a beam as an input
    split_total = 0
    for row in range(2, len(manifold), 2):
        splitters = [match.start() for match in re.finditer('\\^', manifold[row])]
        for splitter_index in splitters:
            if manifold[row - 1][splitter_index] == '|':
                split_total += 1
    return split_total, manifold


class SplitterNode():
    """ tracks splitter node location in the graph """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.parent_keys = []
        self.indegree = 0
        self.ways = 0
        self.child_keys = []
        self.visited = False
        self.key = str(self.row) + '-' + str(self.col)

    def add_parent(self, parent_key):
        """ logs the link to the parent (input) node """
        self.parent_keys.append(parent_key)
        self.indegree += 1

    def add_child(self, child_key):
        """ logs a link to one of the child (output) nodes """
        self.child_keys.append(child_key)


def print_graph(the_graph):
    """ pretty print the state of the graph """
    for node_key, node in the_graph.items():
        print(f'Node {node_key}: with {len(node.parent_keys)} parents')
        for child_key in node.child_keys:
            print(f'\tChild {child_key}')

def count_paths(the_graph, first_node, last_node):
    """ adapted from https://www.geeksforgeeks.org/dsa/count-possible-paths-two-vertices/ """
    # Perform topological sort using Kahn's algorithm
    #  -- each node already has an indegree value (which is the number
    #     of inputs/parents)
    q = deque()
    for key in the_graph.keys():
        if the_graph[key].indegree == 0:
            q.append(key)

    topo_order = []
    while q:
        node_key = q.popleft()
        topo_order.append(node_key)

        for child_key in the_graph[node_key].child_keys:
            the_graph[child_key].indegree -= 1
            if the_graph[child_key].indegree == 0:
                q.append(child_key)

    # Traverse in topological order
    first_node.ways = 1
    for node_key in topo_order:
        for child_node_key in the_graph[node_key].child_keys:
            the_graph[child_node_key].ways += the_graph[node_key].ways

    return last_node.ways



def part_2(manifold) -> int:
    """ AoC Part 2 Solution: test answer = 40, answer = 32982105837605  """
    # use the manifold created in Part 1 to create a graph database
    # of all node connections
    #   node are mapped by row/column, with a uniquely generated ID
    #   nodes are stored in the dictionary with a generated key value
    #        key value = "row-col"
    #   when the entire manifold is mapped, all beams terminate in
    #        a "final" node (row number is > last row of manifold)
    graph = {}
    final_node = SplitterNode(len(manifold) + 1, 0)
    for row, line in enumerate(manifold):
        if row >= 2:
            splitters = [match.start() for match in re.finditer('\\^', line)]
            for splitter_index in splitters:
                newSplitter = SplitterNode(row, splitter_index)
                graph[newSplitter.key] = newSplitter
    graph[final_node.key] = final_node
    # now connect the nodes
    for node_key, node in graph.items():
        # follow the left split beam...
        for beam in [node.col - 1, node.col + 1]:
            child_key = ''
            for r in range(node.row + 2, len(manifold), 2):
                if manifold[r][beam] == '^':
                    child_key = str(r) + '-' + str(beam)
                    break
            if child_key == '':
                # no other splitter was found, so link to the final node
                child_key = final_node.key
            node.add_child(child_key)
            graph[child_key].add_parent(node_key)
    #print_graph(graph)
    print(f'the graph has {len(graph)} nodes')
    # finally use the graph with Depth First Search algorithm to
    # determine the total number of possible paths
    root_node = next(iter(graph.values()))
    #recursive_dfs(root_node, final_node, graph, total_paths)
    total_paths = count_paths(graph, root_node, final_node)
    return total_paths


if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt')
    print(f'reading from: {aoc_input}')
    lines = []
    with aoc_input.open('r', encoding="utf-8") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer1, manifold = part_1(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer1}')

    answer2 = part_2(manifold)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer2}')
