from typing import *
import random
import numpy as np
from my_types import *

all_blocks=["1","L","mirrorL","T","Z","mirrorZ","square"]
all_blocks_without_totation = [
    [[1,1,1,1]],
    [[1,0],
     [1,0],
     [1,1]],
    [[0,1],
     [0,1],
     [1,1]],
    [[1,1,1],
     [0,1,0]],
    [[1,1,0],
     [0,1,1]],
    [[0,1,1],
     [1,1,0]],
    [[1,1],
     [1,1]]      
]
n_block_types = len(all_blocks)

def rotate_matrix_90_clockwise(matrix):
    transpose_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    rotated_matrix = [row[::-1] for row in transpose_matrix]
    return rotated_matrix

all_blocks_with_rotation:List[List[block_t]] = list()
for block in all_blocks_without_totation:
    this_block_with_rot = list()
    this_block_with_rot.append(block)
    for _ in range(3):
        block = rotate_matrix_90_clockwise(block)
        already_exist = False
        for existing in this_block_with_rot:
            if existing==block:
                already_exist = True
                break
        if not already_exist:
            this_block_with_rot.append(block)
    all_blocks_with_rotation.append(this_block_with_rot)
del all_blocks_without_totation
        

def fall_down(board:board_t,block:int)->List[board_t]:
    pass

class RandBlkSeqGenerator():
    def __init__(self,seed:int,window_size:int) -> None:
        self.random_generator = random.Random(seed)
        self.blocks = list()
        for _ in range(max(10,window_size)):
            self.blocks.append(self.random_generator.randint(0,n_block_types-1))
        self.curr_block_i = -1
        self.window_size=window_size
    
    def get_next_blocks(self)->List[block_id_t]:
        self.curr_block_i+=1
        if self.curr_block_i+self.window_size>len(self.blocks):
            for _ in range(len(self.blocks)):
                self.blocks.append(self.random_generator.randint(0,n_block_types-1))
        return self.blocks[self.curr_block_i:self.curr_block_i+self.window_size]
    