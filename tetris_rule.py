from typing import *
import copy
import random
import numpy as np
from my_types import *

all_blocks=["1","mirrorL","L","T","mirrorZ","Z","square"]
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
        

def fall_down(board_with_score:board_t,block_id:int,scores_per_line:List[int]=[1,3,6,10])->List[board_t]:
    board,curr_score = board_with_score
    board_w = len(board[0])
    board_h = len(board)
    res = list()
    for block_rotated in all_blocks_with_rotation[block_id]:
        block_rotated = np.array(block_rotated)
        block_w = len(block_rotated[0])
        block_h = len(block_rotated)
        fake_board = np.concatenate((board,np.zeros((block_h,board_w),dtype=int)))
        for fall_col in range(board_w-block_w+1):
            fall_down_height = -block_h
            while fall_down_height<board_h-block_h:
                next_fall_h = fall_down_height+1
                if np.sum(fake_board[board_h-next_fall_h-block_h:board_h-next_fall_h,fall_col:fall_col+block_w]*block_rotated)==0:
                    fall_down_height = next_fall_h
                else:
                    break
            if fall_down_height>=0:
                new_bd = np.array(board.tolist())
                new_bd[board_h-fall_down_height-block_h:board_h-fall_down_height,fall_col:fall_col+block_w] += block_rotated
                eleminated_line_cnt = 0
                for y in range(board_h):
                    while (new_bd[y]==1).all():
                        new_bd = np.concatenate((new_bd[:y],new_bd[y+1:],np.zeros((1,board_w),dtype=int)))
                        eleminated_line_cnt+=1
                score_get_by_elminate = 0
                if eleminated_line_cnt>0:
                    score_get_by_elminate=scores_per_line[eleminated_line_cnt-1]
                res.append((new_bd,curr_score+score_get_by_elminate))
    return res




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
    

if __name__=="__main__":
    board = np.array([
        [1,1,1,1,0],
        [1,0,1,0,0],
    ])
    for b_n in fall_down((board,0),3):
        print(b_n[0][::-1,:],b_n[1],end="\n\n")