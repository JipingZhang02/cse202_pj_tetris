from typing import *
import numpy as np
from my_types import *

class Pattern:
    def __init__(self) -> None:
        pass

    def calculate_score(self,board:board_t,single_gene_val:float)->float:
        raise NotImplemented

    def __call__(self,board:np.ndarray,single_gene_val:float)->float:
        return self.calculate_score(board,single_gene_val)
    

def get_patterns()->List[Pattern]:
    pass

def rand_init()->List[gene_t]:
    pass

def pattern_match(board:board_t,patterns:List[Pattern],gene:gene_t)->float:
    res = 0.0
    for ptn,g in zip(patterns,gene):
        res += ptn.calculate_score(board,g)
    return res