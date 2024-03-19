from typing import *
import copy
import random
from my_types import *
import args as aaa
import patterns
import play_tetris
import numpy as np
from tqdm import tqdm
import json

import matplotlib.pyplot as plt
import matplotlib.patches as mptch


def cross(gene1:gene_t,gene2:gene_t)->Tuple[gene_t,gene_t]:
    res1,res2 = list(),list()
    for g1,g2 in zip(gene1,gene2):
        if random.randint(0,1)==0:
            res1.append(g1)
            res2.append(g2)
        else:
            res1.append(g2)
            res2.append(g1)
    return res1,res2


def mutate(gene:gene_t,prob:float)->gene_t:
    res = list()
    for g in gene:
        if random.random()>=prob:
            res.append(g)
            continue
        r = random.randint(-4,4)
        if r==-4:
            g = int(g*0.8)
        elif r==4:
            g = int(g*1.2)
        elif r==0:
            g = -g
        else:
            g+=(abs(r)//r)*(5*abs(r)+1)
        res.append(g)
    if res!=gene:
        return res
    else:
        return mutate(gene,prob)


def selection_and_mutate(genes:List[gene_t],eval_gene_func,args)->Tuple[List[gene_t],List[int],int,float]:
    GENE_CNT = args.gene_cnt
    ELEMINATE_CNT = args.eleminate_cnt
    MUTATE_CNT = args.mutate_cnt
    MUTATE_PROB = args.mutate_prob
    CROSS_CNT = args.cross_cnt
    TEMPERATURE = args.tempreture

    genes = copy.deepcopy(genes)
    scores = list()
    for i in range(len(genes)):
        scores.append(eval_gene_func(genes[i]))
    avg_score = sum(scores)/GENE_CNT
    max_score = max(scores)
    temperatured_scores = list(map(lambda x:x/TEMPERATURE,scores))
    min_temp_score = min(temperatured_scores)
    save_probs = list()
    for s in temperatured_scores:
        save_probs.append(2**(s-min_temp_score))
    res = list()
    while len(res)<GENE_CNT-ELEMINATE_CNT:
        saved_gene_i = random.choices(list(range(len(save_probs))),save_probs,k=1)[0]
        res.append(genes[saved_gene_i])
        del save_probs[saved_gene_i]
        del genes[saved_gene_i]

    random.shuffle(res)
    for i in range(CROSS_CNT):
        g1,g2 = cross(res[2*i],res[2*i+1])
        res.append(g1)
        res.append(g2)

    for i in range(MUTATE_CNT):
        j = random.randint(0,GENE_CNT-ELEMINATE_CNT-1)
        res.append(mutate(res[j],MUTATE_PROB))

    assert len(res)==GENE_CNT

    return res,scores,max_score,avg_score


def should_early_stop(max_s_trend,early_stop_score)->bool:
    if len(max_s_trend)<5:
        return False
    for i in range(-1,-4,-1):
        if max_s_trend[i]<early_stop_score:
            return False
    return True


def draw_trend_plot(max_s_trend,avg_s_trend,model_name):
    epochs = list(range(1,1+len(max_s_trend)))
    plt.plot(epochs,max_s_trend,color="blue")
    plt.plot(epochs,avg_s_trend,color="red")
    plt.title(model_name)
    plt.xlabel("epoch")
    plt.ylabel("loss")
    red_patch = mptch.Patch(color="red",label="avg score")
    blue_patch = mptch.Patch(color="blue",label="max score")
    plt.legend(handles=[red_patch,blue_patch])
    plt.savefig(f"./output/plot/{model_name}.pdf")


if __name__=="__main__":
    args = aaa.get_args()
    HEIGHT = args.board_height
    WIDTH = args.board_width
    SCORE_CLR_LINE = args.score_clr_line
    WINDOW_SIZE = args.window_size
    MAX_BLOCK_CNT = args.max_block_cnt
    SEED = args.seed
    BEAM_SIZE = args.beam_size
    GENE_CNT = args.gene_cnt
    ELEMINATE_CNT = args.eleminate_cnt
    MUTATE_CNT = args.mutate_cnt
    MUTATE_PROB = args.mutate_prob
    CROSS_CNT = args.cross_cnt
    TEMPERATURE = args.tempreture
    EPOCH = args.epoch
    EARLY_STOP_SCORE = args.early_stop_score

    random.seed(SEED)

    MODEL_NAME = f"tetris_G{GENE_CNT}_EL{ELEMINATE_CNT}_MUT{MUTATE_CNT}_PR{MUTATE_PROB}_CR{CROSS_CNT}_T{TEMPERATURE}"


    ptrns = patterns.get_patterns(args)
    genes = patterns.rand_init_gene(args)

    avg_score_trend = list()
    max_score_trend = list()
    epochs_list = list()

    for e in range(EPOCH):
        seed_this_round = random.randint(0,99999999)
        print(f"epoch:{e}\ngenes:")
        for gene in genes:
            print(gene)
        # cache = dict()
        def eval_gene(gene):
            # k = tuple(gene)
            # if k in cache:
            #     return cache[k]
            score_func = lambda board:patterns.pattern_match(board,ptrns,gene)
            score = play_tetris.play(seed_this_round,WIDTH,HEIGHT,MAX_BLOCK_CNT,WINDOW_SIZE,BEAM_SIZE,SCORE_CLR_LINE,score_func)
            print(f"gene {gene} get {score} points in playing game\n")
            # cache[k]=score
            return score
        genes_next,scores,max_s,avg_s = selection_and_mutate(genes,eval_gene,args)
        epochs_list.append(e)
        avg_score_trend.append(avg_s)
        max_score_trend.append(max_s)
        genes_prev = genes
        genes = genes_next
        print("\n\n")
        if should_early_stop(max_score_trend,EARLY_STOP_SCORE):
            break
    print(genes)
    draw_trend_plot(max_score_trend,avg_score_trend,MODEL_NAME)
    with open(f"./output/model/{MODEL_NAME}.txt","w+") as fout:
        for gene,s in zip(genes_prev,scores):
            fout.write(str(s)+"  "+str(gene)+"\n")
    with open(f"./output/log/{MODEL_NAME}.txt","w+") as fout:
        json.dump({'max_score':max_score_trend,'avg_score':avg_score_trend},fout,indent=4)