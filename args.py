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
    parser.add_argument("--board_height",type=int,default=20)
    parser.add_argument("--board_width",type=int,default=10)
    parser.add_argument("--score_clr_line",type=parse_list,default=[1,2,3,4])
    parser.add_argument("--window_size",type=int,default=3)
    parser.add_argument("--seed",type=int,default=42)
    parser.add_argument("--beam_size",type=int,default=10)
    parser.add_argument("--epoch",type=int,default=1000)
    return parser.parse_args()

if __name__=="__main__":
    args = get_args()
    score_clr_line = args.score_clr_line
    print(type(score_clr_line))
    print(type(score_clr_line[0]),score_clr_line[0])
    print(score_clr_line)