import argparse
import ast

def parse_list(argument):
    """Converts a string list representation into a Python list."""
    try:
        # Safely evaluate an expression node or a string containing a Python expression
        result = ast.literal_eval(argument)
        if not isinstance(result, list):
            raise ValueError
        return result
    except:
        raise argparse.ArgumentTypeError("The argument should be a list")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_height",type=int,default=8)
    parser.add_argument("--board_width",type=int,default=8)
    parser.add_argument("--score_clr_line",type=parse_list,default=[1,2,3,4])
    parser.add_argument("--window_size",type=int,default=2) # how many tetris blocks player can see
    parser.add_argument("--max_block_cnt",type=int,default=150) 
    parser.add_argument("--seed",type=int,default=42)
    parser.add_argument("--beam_size",type=int,default=5)
    parser.add_argument("--gene_cnt",type=int,default=16)
    parser.add_argument("--eleminate_cnt",type=int,default=8)
    parser.add_argument("--mutate_cnt",type=int,default=4)
    parser.add_argument("--mutate_prob",type=float,default=0.4)
    parser.add_argument("--cross_cnt",type=int,default=2)
    parser.add_argument("--epoch",type=int,default=100)
    parser.add_argument("--tempreture",type=float,default=1.0)
    parser.add_argument("--early_stop_score",type=int,default=65)
    res = parser.parse_args()
    if res.cross_cnt*2+res.mutate_cnt!=res.eleminate_cnt:
        raise ValueError
    return res

if __name__=="__main__":
    args = get_args()
    score_clr_line = args.score_clr_line
    print(type(score_clr_line))
    print(type(score_clr_line[0]),score_clr_line[0])
    print(score_clr_line)