#----------------------------------------------------------
# AoC 2024 Day 0
#----------------------------------------------------------
from pathlib import Path
import logging
import threading
import time
from copy import copy



class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def evaluateStone1(stone):
    # applies the rules for the Plutonian Pebbles and returns a list of the 
    # resulting stones
    results = []
    if stone == '0':
        results.append('1')
    elif (len(stone) % 2) == 0:
        results.append(str(int(stone[:len(stone)//2])))
        results.append(str(int(stone[len(stone)//2:])))
    else:
        value = int(stone)
        results.append(f'{value*2024}')
    return results

class StoneInfo:
    def __init__(self, stone_id, blink_number):
        self.stone_id = stone_id
        self.results = []
        self._counts = {}
        self.updateBlink(blink_number, 1)
        # pre-calculate the results now
        if stone_id == '0':
            self.results.append('1')
        elif (len(stone_id) % 2) == 0:
            self.results.append(str(int(stone_id[:len(stone_id)//2])))
            self.results.append(str(int(stone_id[len(stone_id)//2:])))
        else:
            value = int(stone_id)
            self.results.append(f'{value*2024}')

    def updateBlink(self, blink_number, count):
        if blink_number in self._counts.keys():
            self._counts[blink_number] = self._counts[blink_number] + count
        else:
            self._counts[blink_number] = count

    def countThisBlink(self, blink_number):
        # assumes the blink was already counted at least once
        return self._counts[blink_number]
    
    def blinkedDuring(self, blink_number) -> bool:
        return blink_number in self._counts.keys()

    def __str__(self):
        return f'last blink updated {self.blink_number:2d}, count {self.total_this_blink} (results: {self.results}) for Stone {self.stone_id}'
    
class StoneDict:
    def __init__(self):
        self._stones = {}

    @property
    def length(self) -> int:
        return len(self._stones)
    
    def ids(self):
        return self._stones.keys()
    
    def addStone(self, stone_id, blink_number=0):
        # assumes the stone doesn't already exist
        self._stones[stone_id] = StoneInfo(stone_id, blink_number)

    def getStone(self, stone_id) -> StoneInfo:
        # assumes the stone exists
        return self._stones[stone_id]
    
    def addAndGetStone(self, stone_id) -> StoneInfo:
        if stone_id not in self._stones.keys():
            self.addStone(stone_id)
        return self._stones[stone_id]
    
    def inBlinkNumber(self, blink_number):
        # runs through the dictionary and returns a list of stones that
        # match the given blink number
        results = []
        for s in self._stones.keys():
            if self._stones[s].blinkedDuring(blink_number):
                results.append(self._stones[s])
        return results
    
    def __str__(self):
        result = ''
        for id in self._stones.keys():
            result += f'Last blink updated: {self._stones[id].blink_number:2d}, count = {self._stones[id].total_this_blink}, ID: {self._stones[id].stone_id}\n'
        return result


def part_1(input_lines, max_blinks) -> int:
    # test answer = 55312, answer (25) = 228668, answer (75) = 
    stones = input_lines[0].split(' ')
    start_time = time.perf_counter()
    for i in range(max_blinks):
        #logging.debug(f'blink {i}: {stones}')
        next_blink_stones = []
        for stone in stones:
            next_stones = evaluateStone1(stone)
            next_blink_stones += next_stones
        stones = next_blink_stones
    finish_time = time.perf_counter()
    print(f'Part 1 elapsed time for {max_blinks} blinks = {(finish_time - start_time):04f} secs')
    return len(stones)

def part_2(input_lines, max_blinks) -> int:
    # test answer = 55312, answer (25) = 228668, answer (75) = 270673834779359
    # dictionary value is:  (stone result list, count for this stone)
    stones = StoneDict();
    initial_stones = input_lines[0].split(' ')
    start_time = time.perf_counter()
    for initial_stone in initial_stones:
        stones.addStone(initial_stone)
    total_this_blink = 0
    for i in range(1, max_blinks+1):
        # reevaluate each entry in the dictionary for each blink
        #logging.debug(f'=== blink {i} - current dict keys: {stones.ids()}')
        for stone in stones.inBlinkNumber(i-1):
            # make sure the next set of stones is added to the current blink
            #logging.debug(f'processing blink {i} for {stone}')
            for next_stone in stone.results:
                stones.addAndGetStone(next_stone).updateBlink(i, stone.countThisBlink(i-1))
    finish_time = time.perf_counter()
    print(f'Part 2 elapsed time for {max_blinks} blinks = {(finish_time - start_time):04f} secs')
    # finally sum the totals of each stone in the dictionary
    #print(f'after {i:2d} blinks:')
    for stone in stones.inBlinkNumber(i):
        total_this_blink += stone.countThisBlink(i)
        #for j in range(stone.countThisBlink(i)):
        #    print(f'{stone.stone_id} ', end='')
    #print(f'\n--- total stones = {total_this_blink}\n')
    return total_this_blink

if __name__ == "__main__":
    # use logging so we can turn off debug printing
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

    aoc_input = Path(__file__).with_name('input.txt')
    #aoc_input = Path(__file__).with_name('input_test.txt') 
    print(f'reading from: {aoc_input}')
    with aoc_input.open('r') as f:
       #lines = " ".join(line.rstrip() for line in file)
       lines = f.readlines()
    lines = [x.strip() for x in lines]
    answer_1 = part_1(lines, 25)
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(lines, 75)
    print(f'part 2 answer: {answer_2}')
    