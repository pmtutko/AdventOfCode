#----------------------------------------------------------
# AoC 2024 Day 13
#----------------------------------------------------------
from pathlib import Path
import logging
import re
import itertools

class ClawMachine:
    # generates an ID for each separate machine
    machine_id_gen = itertools.count()

    def __init__(self, input_lines, prize_offset=0):
        self._id = next(ClawMachine.machine_id_gen)
        parse_buttons = R"X\+(\d+), Y\+(\d+)"
        parse_prize = R"X\=(\d+), Y\=(\d+)"
        re_buttons = re.compile(parse_buttons)
        re_prize = re.compile(parse_prize)
        self._buttonA_x, self._buttonA_y = map(int, re_buttons.search(input_lines[0]).groups())
        self._buttonB_x, self._buttonB_y = map(int, re_buttons.search(input_lines[1]).groups())
        self._prize_x, self._prize_y = map(int, re_prize.search(input_lines[2]).groups())
        self._prize_x += prize_offset
        self._prize_y += prize_offset
        logging.debug(f'Machine {self._id}')
        logging.debug(f'\tButton A: {self._buttonA_x}, {self._buttonA_y}')
        logging.debug(f'\tButton B: {self._buttonB_x}, {self._buttonB_y}')
        logging.debug(f'\t   Prize: {self._prize_x}, {self._prize_y}')
        self._buttonA_presses = 0
        self._buttonB_presses = 0
        self.pathToPrize()
        
    def pathToPrize(self):
        '''
        Solve by simultaneous equations
          Given the machine:
            Button A: X+94, Y+34
            Button B: X+22, Y+67
            Prize: X=8400, Y=5400
          then 94a + 22b = 8400 and 34a + 67b = 5400
          so,
            34(94a + 22b) = 34(8400) and
            94(34a + 67b) = 94(5400) yields
            a = 80 and b = 40
        '''
        eq1 = [self._buttonA_x, self._buttonB_x, self._prize_x]
        eq2 = [self._buttonA_y, self._buttonB_y, self._prize_y]
        eq11 = [i * self._buttonA_y for i in eq1]
        eq21 = [i * self._buttonA_x for i in eq2]
        b = (eq11[2] - eq21[2])/(eq11[1] - eq21[1])
        a = (eq1[2] - (eq1[1] * b))/eq1[0]
        if (int(a) - a) == 0 and (int(b) - b) == 0:
            self._buttonA_presses = a
            self._buttonB_presses = b
            logging.debug(f'\tSolution: press A {a} times, and B {b} times')
        else:
            logging.debug(f'\t-- No valid solution found!')

    def tokenCost(self) -> int:
        return int((self._buttonA_presses * 3) + self._buttonB_presses)
        

def part_1(input_lines) -> int:
    # test answer = 480, answer = 36571
    machines = []
    for i in range(0, len(input_lines), 4):
        machines.append(ClawMachine(input_lines[i:i+4]))
    logging.debug(f'there are {len(machines)} machines')
    total_tokens = 0
    for m in machines:
        total_tokens += m.tokenCost()
    return total_tokens

def part_2(input_lines) -> int:
    # test answer = 875318608908, answer = 85527711500010
    machines = []
    for i in range(0, len(input_lines), 4):
        machines.append(ClawMachine(input_lines[i:i+4], prize_offset=10000000000000))
    logging.debug(f'there are {len(machines)} machines')
    total_tokens = 0
    for m in machines:
        total_tokens += m.tokenCost()
    return total_tokens

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
    