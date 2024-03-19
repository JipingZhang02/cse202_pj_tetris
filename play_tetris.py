from typing import *
import numpy as np
from my_types import *
import tetris_rule
import patterns

from tqdm import tqdm

# def is_end(board:board_t,args)->bool:
#     return (board[-1]==1).any()


class LinkedNode:
    def __init__(self,val,prev) -> None:
        self.val = val
        self.prev = prev


def beam_search(board_with_score:board_t,window:List[block_id_t],beam_size:int,score_func,score_clr_line)->Optional[board_t]:
    beam:List[LinkedNode] = [LinkedNode(board_with_score,None)]
    for block_id in window:
        new_beam = list()
        for linked_node in beam:
            bd_s = linked_node.val
            for new_bd_s in tetris_rule.fall_down(bd_s,block_id,score_clr_line):
                new_beam.append(LinkedNode(new_bd_s,linked_node))
        if len(new_beam)==0:
            break
        new_beam.sort(key=lambda lnode:score_func(lnode.val),reverse=True)
        if len(new_beam)>beam_size:
            new_beam = new_beam[:beam_size]
        beam = new_beam
    best = beam[0]
    if best.prev is None:
        return None
    while not (best.prev.prev is None):
        best = best.prev
    return best.val
            


def play(seed:int,board_w:int,board_h:int,max_blk_cnt:int,window_size:int,beam_size:int,score_clr_line,score_func,should_print=False)->int:
    board = np.zeros((board_h,board_w),dtype=int),0
    blk_generator = tetris_rule.RandBlkSeqGenerator(seed,window_size)
    for _ in tqdm(range(max_blk_cnt),desc="playing..."):
        next_bd = beam_search(board,blk_generator.get_next_blocks(),beam_size,score_func=score_func,score_clr_line=score_clr_line)
        if next_bd is None:
            break
        if should_print:
            print(next_bd[0][::-1,:])
            print("score: "+str(next_bd[1]))
            print("\n\n")
        board = next_bd
    return board[1]

if __name__=="__main__":
    ptrns,gene=patterns.get_patterns(None),patterns.rand_init_gene(None)[0]
    score_func = lambda board:patterns.pattern_match(board,ptrns,gene)
    play(42,10,10,100,3,10,[1,2,3,4],score_func,True)