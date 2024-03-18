from typing import *
import copy
import numpy as np
from my_types import *
from my_types import board_t

class Pattern:
    def __init__(self) -> None:
        pass

    def calculate_score(self,board:board_t,single_gene_val:int)->int:
        raise NotImplemented

    def __call__(self,board:np.ndarray,single_gene_val:int)->int:
        return self.calculate_score(board,single_gene_val)
    

class ShapePattern(Pattern):
    def __init__(self,shape_ptrn:np.ndarray) -> None:
        if not isinstance(shape_ptrn,np.ndarray):
            shape_ptrn = np.array(shape_ptrn)
        self.shape_ptrn = shape_ptrn

    def calculate_score(self, board: board_t, single_gene_val: int) -> int:
        board = board[0]
        shape_w = len(self.shape_ptrn[0])
        shape_h = len(self.shape_ptrn)
        board_w = len(board[0])
        board_h = len(board)
        if shape_w>board_w or shape_h>board_h:
            return 0
        res = 0
        for y in range(board_h-shape_h+1):
            for x in range(board_w-shape_w+1):
                sub_board = board[y:y+shape_h,x:x+shape_w]
                if (self.shape_ptrn==sub_board).all():
                    res+=1
        return res*single_gene_val


class GetScorePattern(Pattern):
    def __init__(self) -> None:
        pass

    def calculate_score(self, board: board_t, single_gene_val: int) -> int:
        return board[1]*single_gene_val


patterns = list()
patterns.append(GetScorePattern())
patterns.append(ShapePattern([[0],
                              [1]]))
patterns.append(ShapePattern([[0],
                              [0],
                              [1]]))
patterns.append(ShapePattern([[0,0],
                              [1,1]]))
patterns.append(ShapePattern([[1,0,1],
                              [1,0,1]]))
patterns.append(ShapePattern([[1],
                              [0]]))
patterns.append(ShapePattern([[1,1],
                              [1,0]]))
patterns.append(ShapePattern([[1,1],
                              [0,1]]))
patterns.append(ShapePattern([[1,1],
                              [0,0]]))
patterns.append(ShapePattern([[1,1,1],
                              [0,0,0]]))

def get_patterns(args)->List[Pattern]:
    return patterns

def rand_init(args)->List[gene_t]:
    gene = [100,-50,-60,-70,-15,3,7,7,20,35]
    return [gene]

def pattern_match(board:board_t,patterns:List[Pattern],gene:gene_t)->int:
    res = 0
    for ptn,g in zip(patterns,gene):
        res += ptn.calculate_score(board,g)
    return res


if __name__=="__main__":
    shape_ptrn = ShapePattern(np.array([
        [0,0],
        [1,1]
    ]))
    board = np.array([
        [1,1,1,1],
        [1,1,0,0],
        [0,0,0,0]
    ])
    board = (board,10)
    print(pattern_match(board,get_patterns(None),rand_init(None)[0]))
    # print(shape_ptrn.calculate_score(board,1))
