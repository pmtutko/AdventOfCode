import logging
import copy
from queue import Queue
import networkx as nx

def visualizePath(maze, path) -> str:
    grid_map = f'\npath:\n'
    for r, row in enumerate(maze):
        line = ''
        for c, pt in enumerate(row):
            if (r,c) in path:
                line += '+'
            elif pt == 1:
                line += '#'
            elif pt == 0:
                line += '.'
        grid_map += (line + '\n')
    return grid_map

def nextPossibleSteps(maze, r, c, previous_steps) -> list:
    # in the maze grid 1 == wall, 0 == open
    next_steps = []
    for dr, dc in [(-1,0), (0,1), (1,0), (0,-1)]:
        if maze[r+dr][c+dc] == 0 and (r+dr,c+dc) not in previous_steps:
            next_steps.append((r+dr,c+dc))
    return next_steps

def findAllPaths(maze, r, c, end_pt, input_path, all_paths):
    # recursive function, DEFINITELY exceeds the recursion depth for larger mazes
    this_path = copy.copy(input_path)
    possible_steps = nextPossibleSteps(maze, r, c, this_path)
    if possible_steps:
        previous_step_evaluated = ()
        for step in possible_steps:
            if step not in this_path:
                if this_path[-1] == previous_step_evaluated:
                    this_path.pop()
                this_path.append(step)
                if step == end_pt:
                    # we're done with this path!
                    all_paths.append(this_path)
                else:
                    findAllPaths(maze, step[0], step[1], end_pt, this_path, all_paths)
            previous_step_evaluated = step
    else:
        all_paths.append(this_path)

def pathScore(path) -> int:
    # we start by facing EAST, so we may have to turn a number
    # of times (by 90 degrees) to face the direction of the path
    TURN_SCORE = 1000
    FORWARD_SCORE = 1
    score = 0
    step_turn = 0
    this_step = tuple(np.subtract(path[0], path[1]))
    if this_step == (1,0) or this_step == (-1,0):
        # we're going NORTH or SOUTH, so add ONE 90 deg turn to the score
        step_turn += 1
    elif this_step == (0,-1):
        # we're going WEST, so add TWO 90 deg turns to the score
        step_turn += 2
    else:
        # we're going EAST, so without turning add one forward step
        pass
    # add the rest of the steps
    for i in range(2, len(path)):
        last_step = this_step
        this_step = tuple(np.subtract(path[i-1], path[i]))
        step_difference = tuple(np.subtract(last_step, this_step))
        if step_difference != (0,0):
            step_turn += 1
    score = ((len(path) - 1) * FORWARD_SCORE) + (TURN_SCORE * step_turn)
    logging.debug(f'path {score=} - {len(path) - 1} steps, {step_turn} turns')
    return score

def findPathBFS(maze, start, end):
    # from https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
    # BFS algorithm to find the shortest path
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0]+dx, node[1]+dy)
            if (next_node == end):
                return path + [next_node]
            if (next_node[0] >= 0 and next_node[1] >= 0 and 
                next_node[0] < maze.shape[0] and next_node[1] < maze.shape[1] and 
                maze[next_node] == 0 and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))

def createGraph(maze, start_pt, end_pt) -> nx.Graph:
    rows, cols = len(maze), len(maze[0])
    wg = nx.grid_2d_graph(rows, cols)
    for r, row in enumerate(maze):
        for c, pt in enumerate(row):
            # we only want open spots, not walls
            # so remove the walls from the graph
            if pt == 1:
                wg.remove_node((r,c))
    return wg

def calcWeight(node1, node2, edge_attribs):
    #print(f'{node1=} {node2=} {edge_attribs=}')
    return 1


def part_1_weighted_graph(maze, start_pt, end_pt) -> int:
    maze_graph = createGraph(maze, start_pt, end_pt)
    # Visualize the graph
    '''
    pos = {(x, y): (y, -x) for x, y in maze_graph.nodes()}
    nx.draw(maze_graph, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=10, font_weight='bold')
    plt.show()
    '''
    path_generator = nx.all_simple_paths(maze_graph, start_pt, end_pt)
    paths = [p for p in path_generator]
    print(f'found {len(paths)} paths')
    scores = []
    for path in paths:
        scores.append(pathScore(path))
    return min(scores)

def part_1_bfs(maze, start_pt, end_pt) -> int:
    # test answer = 11048, answer = xxxx
    maze_array = np.array(maze)
    #plt.imshow(maze_array, cmap='binary')
    #plt.xticks([]), plt.yticks([])  # Hide the axes ticks
    #plt.show()
    path = findPathBFS(maze_array, start_pt, end_pt)
    return pathScore(path)

def part_1_recursion(maze, start_pt, end_pt) -> int:
    # test answer = 11048, answer = xxxx
    #maze_array = np.array(maze)
    #plt.imshow(maze_array, cmap='binary')
    #plt.xticks([]), plt.yticks([])  # Hide the axes ticks
    #plt.show()
    all_paths = []
    first_path = [(start_pt[0], start_pt[1])]
    findAllPaths(maze, start_pt[0], start_pt[1], end_pt, first_path, all_paths)
    valid_paths = []
    for path in all_paths:
        if path[-1] == end_pt:
            valid_paths.append(path)
    logging.debug(f'{len(valid_paths)} paths found')
    scores = []
    for path in valid_paths:
        scores.append(pathScore(path))
        logging.debug(visualizePath(maze, path))
        logging.debug(f'{pathScore(path)=}')
    return min(scores)
