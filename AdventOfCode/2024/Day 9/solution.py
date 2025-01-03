#----------------------------------------------------------
# AoC 2024 Day 9
#----------------------------------------------------------
from pathlib import Path
import logging
from enum import Enum

class BlockState(Enum):
    Empty = '.'
    Filled = 'X'

class Block:
    def __init__(self, default_file_id=-1, default_data=BlockState.Empty.value):
        self._file_id = default_file_id
        self._data = default_data

    def write(self, file_id, data=BlockState.Filled.value):
        self._file_id = file_id
        if self._file_id == -1:
            # we're actually erasing in this case
            self._data = BlockState.Empty.value
        else:
            self._data = data

    def read(self) -> str:
        #return str(self._data)
        if self._data == '.':
            return '.'
        return str(chr(ord('0') + self._file_id))
    
    def getFileID(self) -> int:
        return self._file_id
    
    def state(self) -> BlockState:
        if self._data == BlockState.Empty.value:
            return BlockState.Empty
        else:
            return BlockState.Filled
    
    def erase(self):
        self._data = BlockState.Empty.value
        self._file_id = -1

class Disk:
    def __init__(self):
        # the disk is organized into blocks, which are either empty or full
        self._blocks = {}
        # files are tracked by their filename (file_id) and a list of the blocks they occupy
        self._files = {}
        # free space is tracked by the starting block number and the number of blocks
        self._freespace = {}

    def writeBlocks(self, blockCount, file_id=-1, startBlock=-1):
        # simple function to write the given block data (with a filename or as empty) to the
        # disk at the given location. does not know about files, file tables, or empty space
        # if used during disk initialization, it will create the blocks and add them to the disk

        # if start block is -1, then write the blocks after the last used block on the disk
        if startBlock == -1:
            startBlock = len(self._blocks)

        # if file_id is -1, then we're writing empty space beginning at the startBlock
        # otherwise it's a file
        data = BlockState.Empty.value
        if file_id != -1:
            #data = BlockState.Filled.value
            data = file_id + 48

        for i in range(startBlock, startBlock+blockCount):
            # if the block doesn't exist at the given block index, create it
            if i >= len(self._blocks):
                self._blocks[i] = Block(file_id, default_data=data)

    def readBlocks(self, blockCount, startBlock) -> str:
        data = ''
        for i in range(startBlock, startBlock+blockCount):
            data += self._blocks[i]
        return data
    
    def firstEmptyBlocks(self, startBlock=-1, emptyCount=1) -> int:
        # finds the first empty block beginning at the given starting block number
        # and returns the block number
        start_at = startBlock
        if startBlock == -1:
            start_at = 0
        current_empty_count = 0
        empties = []
        for e in range(start_at, len(self._blocks)):
            if self._blocks[e].state() == BlockState.Empty:
                # we're looking for emptyCount number of blocks
                current_empty_count += 1
                if current_empty_count == emptyCount:
                    # check if the empties are consecutive
                    if emptyCount == 1:
                        return e
                    else:
                        for i in range(len(empties)-1):
                            if (empties[i+1] - empties[i]) != 1:
                                break
                        # if we get here, then we've found an empty block of the requested size
                        return empties[0]
                else:
                    # log the empty block 
                    empties.append(e)
            else:
                empties = []
                current_empty_count = 0
        # we didn't find a big enough empty block, so return -1
        return -1

        # this is really an error condition, else the disk is full!
        return -2

    def defragP1(self):
        # work backwards from the last non-empty block and move that
        # block to the first empty block and keep going.
        # so find the first empty block
        next_empty_block = self.firstEmptyBlocks()
        for f in reversed(list(self._blocks.keys())):
            if self._blocks[f].state() == BlockState.Filled:
                # move the data from the full block to the empty block
                self._blocks[next_empty_block].write(self._blocks[f].getFileID(), self._blocks[f].read())
                self._blocks[f].erase()
                next_empty_block = self.firstEmptyBlocks(startBlock=next_empty_block)
            if next_empty_block >= f:
                # this means we're completely defragged and done!
                break

    def defragP2(self):
        # work backwards from the last file and move that
        # file wholly to the first empty set of empty blocks that
        # can fit the whole file
        captured_entire_file = False
        file_blocks = []
        already_moved = []
        file_id = ''
        start_at = 0
        next_file = (-1, -1)   # next file_id, last block number
        for f in reversed(list(self._blocks.keys())):
            if self._blocks[f].state() == BlockState.Filled:
                if self._blocks[f].getFileID() not in already_moved:
                    # still the same file?
                    if (file_id == '' or file_id == self._blocks[f].getFileID()):
                        file_id = self._blocks[f].getFileID()
                        file_blocks.append(f)
                    else:
                        # save this non-empty block as the next file
                        next_file = (self._blocks[f].getFileID(), f)
                        captured_entire_file = True
            elif self._blocks[f].state() == BlockState.Empty and len(file_blocks) > 0:
                captured_entire_file = True
                next_file = (-1, -1)

            if captured_entire_file:
                if len(file_blocks) > 0 and file_id != '':
                    # we have a file, can we move it to an empty area with enough space?
                    empty_area = self.firstEmptyBlocks(start_at, emptyCount=len(file_blocks))
                    if (empty_area != -1) and (empty_area <= f):
                        for i in range(len(file_blocks)):
                            self._blocks[empty_area + i].write(file_id, self._blocks[file_blocks[i]].read())
                            self._blocks[file_blocks[i]].erase()
                        already_moved.append(file_id)
                    if next_file[0] != -1:
                        file_id = next_file[0]
                        file_blocks = [next_file[1]]
                    else:
                        file_id = ''
                        file_blocks = []
                    captured_entire_file = False
                    #self.print()
            print(f'processing from {f}\r', end='')
        print('\n')


    def checksum(self) -> int:
        the_checksum = 0
        for i, block in self._blocks.items():
            if block.state() == BlockState.Filled:
                this_blocks_checksum = i * block.getFileID()
                #logging.debug(f'block position {i} * file ID {block.getFileID()} = {this_blocks_checksum}')
                the_checksum += this_blocks_checksum
        return the_checksum

    def print(self, line_len=250):
        blocks_on_this_line_count = 0
        line_count = 0
        line = ''
        for id, block in self._blocks.items():
            if blocks_on_this_line_count == 0:
                line = f'{line_count:04}: '
            line += block.read()
            line_count += 1
            blocks_on_this_line_count += 1
            if blocks_on_this_line_count % line_len == 0:
                blocks_on_this_line_count = 0
                print(line)
        print(line)
            


def part_1(disk_map) -> int:
    # test answer = 1928, answer = 6356833654075
    this_disk = Disk()
    file_id = 0
    for i in range(len(disk_map)):
        number_of_blocks = int(disk_map[i])
        if i % 2 == 0:
            # from the data stream, even numbered indexes are the number of blocks in a file
            this_disk.writeBlocks(number_of_blocks, file_id)
            file_id += 1
        else:
            # from the data stream, odd numbered indexes are the number of empty blocks
            this_disk.writeBlocks(number_of_blocks)
    #this_disk.print()
    this_disk.defragP1()
    #this_disk.print()
    return this_disk.checksum()


def part_2(disk_map) -> int:
    # test answer = 2858, answer = 6389911791746
    this_disk = Disk()
    file_id = 0
    for i in range(len(disk_map)):
        number_of_blocks = int(disk_map[i])
        if i % 2 == 0:
            # from the data stream, even numbered indexes are the number of blocks in a file
            this_disk.writeBlocks(number_of_blocks, file_id)
            file_id += 1
        else:
            # from the data stream, odd numbered indexes are the number of empty blocks
            this_disk.writeBlocks(number_of_blocks)
    #this_disk.print()
    this_disk.defragP2()
    #this_disk.print()
    return this_disk.checksum()

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
    answer_1 = part_1(lines[0])
    print(f'part 1 answer: {answer_1}')

    answer_2 = part_2(lines[0])
    print(f'part 2 answer: {answer_2}')
    