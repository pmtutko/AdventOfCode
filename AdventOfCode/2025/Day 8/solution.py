#----------------------------------------------------------
""" AoC 2025 Day 8                                      """
#----------------------------------------------------------
from pathlib import Path
import logging
import itertools
import math


AOC_DAY_NUMBER = 8

point_id = itertools.count()

class Point:
    """ defines a unique three-dimensional point in space """
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.id = next(point_id)
        self.key = str(self.id)


def compute_distance(point_a, point_b) -> float:
    """ calculates the linear distance in three-dimensional
        space between two points """
    return math.sqrt((point_b.x - point_a.x)**2 + 
                     (point_b.y - point_a.y)**2 + 
                     (point_b.z - point_a.z)**2)

def compute_all_distances(input_lines):
    """ a common function to create a dictionary of Point objects and 
        create another dictionary of distances from each Point to all
        other Points """
    # first log all the 3D points...
    points = {}
    for line in input_lines:
        x, y, z = list(map(int, line.split(',')))
        new_point = Point(x, y, z)
        points[new_point.key] = new_point
    # now calculate distances from each point to all others
    point_distances = {}
    for point in points.values():
        for other_point in points.values():
            if other_point.id == point.id:
                pass
            else:
                # distance keys are always "lower ID - higher ID"
                if point.id < other_point.id:
                    distance_key = point.key + '-' + other_point.key
                else:
                    distance_key = other_point.key + '-' + point.key
                point_distances[distance_key] = [compute_distance(other_point, point), 
                                                 point, other_point]
    print(f'---> there are {len(point_distances)} bi-directional paths between all points')
    point_distances = dict(sorted(point_distances.items(), key=lambda item: item[1][0]))
    return points, point_distances

def part_1(input_lines) -> int:
    """ AoC Part 1 Solution: test answer = 40, answer = 83520  """
    points, distances = compute_all_distances(input_lines)
    # now figure out the circuits
    circuits = []
    MAX_CLOSEST = 10  # 1000 for the actual input, 10 for test
    close_distance_count = 0
    for distance_key in distances.keys():
        p1, p2 = distance_key.split('-')
        if len(circuits) == 0:
            # this is the first point pair that makes a circuit
            circuits.append([p1, p2])
        else:
            join_to_circuit = []
            existing_circuit = False
            for n, circuit in enumerate(circuits):
                # each circuit is a list of point keys
                #   make a note of which point should be added to which
                #   circuit, or two circuits may be joined, or a new
                #   circuit created
                if (p1 in circuit) and (p2 not in circuit):
                    join_to_circuit.append([n, p2])
                elif (p1 not in circuit) and (p2 in circuit):
                    join_to_circuit.append([n, p1])
                elif (p1 in circuit) and (p2 in circuit):
                    # the points already exist in the same circuit, nothing to add/modify
                    existing_circuit = True
                    break
            if len(join_to_circuit) == 0 and not existing_circuit:
                # make a new circuit
                circuits.append([p1, p2])
            elif len(join_to_circuit) == 1:
                # add a point to an existing circuit
                circuit_number, point_key = join_to_circuit[0]
                circuits[circuit_number].append(point_key)
            elif len(join_to_circuit) == 2:
                # the points belong to two different circuits, so they
                # must be joioned
                ckt_a = join_to_circuit[0][0]
                ckt_b = join_to_circuit[1][0]
                circuits[ckt_a] = list(set(circuits[ckt_a] + circuits[ckt_b]))
                circuits.pop(ckt_b)
            else:
                pass
        close_distance_count += 1
        if close_distance_count == MAX_CLOSEST:
            break
    #print(circuits)
    # measure the lengths of all the circuits
    lengths = []
    for circuit in circuits:
        lengths.append(len(circuit))
    lengths.sort(reverse=True)
    circuit_length_result = 1
    for i in range(3):
        circuit_length_result *= lengths[i]
    return circuit_length_result, distances, points

def part_2(distances, number_of_points) -> int:
    """ AoC Part 2 Solution: test answer = 25272, answer = 1131823407  """
    # now figure out the circuits
    circuits = []
    for distance_key, distance in distances.items():
        #print(f'{distance[0]}: {distance_key}')
        p1, p2 = distance_key.split('-')
        if len(circuits) == 0:
            # this is the first point pair that makes a circuit
            circuits.append([p1, p2])
        else:
            join_to_circuit = []
            existing_circuit = False
            for n, circuit in enumerate(circuits):
                # each circuit is a list of point keys
                #   make a note of which point should be added to which
                #   circuit, or two circuits may be joined, or a new
                #   circuit created
                if (p1 in circuit) and (p2 not in circuit):
                    join_to_circuit.append([n, p2])
                elif (p1 not in circuit) and (p2 in circuit):
                    join_to_circuit.append([n, p1])
                elif (p1 in circuit) and (p2 in circuit):
                    # the points already exist in the same circuit, nothing to add/modify
                    existing_circuit = True
                    break
            if len(join_to_circuit) == 0 and not existing_circuit:
                # make a new circuit
                circuits.append([p1, p2])
            elif len(join_to_circuit) == 1:
                # add a point to an existing circuit
                circuit_number, point_key = join_to_circuit[0]
                circuits[circuit_number].append(point_key)
            elif len(join_to_circuit) == 2:
                # the points belong to two different circuits, so they
                # must be joioned
                ckt_a = join_to_circuit[0][0]
                ckt_b = join_to_circuit[1][0]
                circuits[ckt_a] = list(set(circuits[ckt_a] + circuits[ckt_b]))
                circuits.pop(ckt_b)
            else:
                pass
        if len(circuits[0]) == len(points):
            # all of the points are in a single circuit, so we're done
            coordinate_result = points[p1].x * points[p2].x
            break
    return coordinate_result

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    next(point_id)

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt')
    print(f'reading from: {aoc_input}')
    lines = []
    with aoc_input.open('r', encoding="utf-8") as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer1, distances_list, points = part_1(lines)
    print(f'AOC Day {AOC_DAY_NUMBER} part 1 answer: {answer1}')

    answer2 = part_2(distances_list, points)
    print(f'AOC Day {AOC_DAY_NUMBER} part 2 answer: {answer2}')
