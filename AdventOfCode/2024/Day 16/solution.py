""" Advent of Code 2024 Day 16 """

from pathlib import Path
import logging
from solver import MazeSolver


def create_maze(input_lines):
    """ Converts the puzzle input into a 2D array of 1s and 0s. """
    maze = []
    start_here = (-1,-1)
    end_here   = (-1,-1)
    for r, line in enumerate(input_lines):
        maze_row = []
        for c, point in enumerate(list(line)):
            if point == '#':
                maze_row.append(1)
            elif point == '.':
                maze_row.append(0)
            elif point == 'S':
                maze_row.append(0)
                start_here = (r, c)
            elif point == 'E':
                maze_row.append(0)
                end_here = (r, c)
        maze.append(maze_row)
    return start_here, end_here, maze

def part_1(maze, start_pt, end_pt) -> int:
    """ test answer = yyy, answer = xxxx """
    solver = MazeSolver(maze, start_pt, end_pt)
    solver.solveDijkstra()

def part_2(maze, start_pt, end_pt) -> int:
    """ test answer = yyy, answer = xxxx """
    ...

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    #aoc_input = Path(__file__).with_name('input.txt')
    aoc_input = Path(__file__).with_name('input_test.txt') 
    print(f'reading from: {aoc_input}')
    with aoc_input.open('r') as f:
        #lines = " ".join(line.rstrip() for line in file)
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    start_pt, end_pt, input_maze = create_maze(lines)

    answer_1 = part_1(input_maze, start_pt, end_pt)
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(input_maze, start_pt, end_pt)
    print(f'part 2 answer: {answer_2}')
