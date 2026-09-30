"""Exact necessary quotient census at four blue pairs, arbitrary red density.
Author: six-books-2, role researcher. Coverage and exclusion proved in FOUR_BLUE.md.
The prior three-red lemma is a premise. No full matching signs are enumerated.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time

Q=11
PAIRS=list(combinations(range(Q),2))
ALL_FLAGS=(1<<(1<<Q))-1
ONE_FLAGS=[sum(1<<word for word in range(1<<Q) if word>>i&1) for i in range(Q)]
SUM_FLAGS={(i,j):(ALL_FLAGS & ~(ONE_FLAGS[i]|ONE_FLAGS[j]),ONE_FLAGS[i]^ONE_FLAGS[j],ONE_FLAGS[i]&ONE_FLAGS[j]) for i,j in PAIRS}


def inspect(red,blue):
    # Bitset formulas used only for a fast necessary quotient census.
    uniform=[r|b for r,b in zip(red,blue)]
    for i,j in PAIRS:
        if uniform[i]>>j&1:continue
        opposite=(red[i]&blue[j]).bit_count()+(blue[i]&red[j]).bit_count()
        fr=red[i].bit_count()+red[j].bit_count()-opposite
        fb=blue[i].bit_count()+blue[j].bit_count()-opposite
        free=9-uniform[i].bit_count()-uniform[j].bit_count()+(uniform[i]&uniform[j]).bit_count()
        if max(0,fb+free-6)>min(free,3-fr):return None
    budgets=[]
    for i,j in PAIRS:
        if not (uniform[i]>>j&1):continue
        color=int(not(red[i]>>j&1));outside=0
        for k in range(Q):
            if k in (i,j):continue
            a=2 if red[i]>>k&1 else 0 if blue[i]>>k&1 else 1
            b=2 if red[j]>>k&1 else 0 if blue[j]>>k&1 else 1
            outside+=a*b if color==0 else (2-a)*(2-b)
        budgets.append((i,j,color,outside))
    # A Python integer carries one bit for every one of the 2048 flags.
    feasible=ALL_FLAGS
    for i in range(Q):
        if 2*red[i].bit_count()>3:feasible &= ALL_FLAGS ^ ONE_FLAGS[i]
        if 2*blue[i].bit_count()>6:feasible &= ONE_FLAGS[i]
    for i,j,color,outside in budgets:
        allowed=0
        for total in range(3):
            pages=outside+2*(total if color==0 else 2-total)
            if pages<=(6 if color==0 else 12):allowed |= SUM_FLAGS[i,j][total]
        feasible &= allowed
    flags=[]
    while feasible:
        bit=feasible & -feasible;flags.append(bit.bit_length()-1);feasible-=bit
    return flags



BLUE_FORMS = [
    ("4k2", [(0,1),(2,3),(4,5),(6,7)]),
    ("p3_2k2", [(0,1),(1,2),(3,4),(5,6)]),
    ("2p3", [(0,1),(1,2),(3,4),(4,5)]),
    ("p4_k2", [(0,1),(1,2),(2,3),(4,5)]),
    ("star3_k2", [(0,1),(0,2),(0,3),(4,5)]),
    ("triangle_k2", [(0,1),(0,2),(1,2),(3,4)]),
    ("p5", [(0,1),(1,2),(2,3),(3,4)]),
    ("star4", [(0,1),(0,2),(0,3),(0,4)]),
    ("fork", [(0,1),(0,2),(0,3),(3,4)]),
    ("c4", [(0,1),(1,2),(2,3),(0,3)]),
    ("paw", [(0,1),(0,2),(1,2),(2,3)]),
]


def add(neighbors, edge):
    i,j=edge
    neighbors[i] |= 1<<j
    neighbors[j] |= 1<<i


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records',type=Path,required=True)
    args=parser.parse_args()
    start=time.monotonic();cases=[];records=[]
    for name,edges in BLUE_FORMS:
        blue=[0]*Q
        for edge in edges:add(blue,edge)
        candidates=[(i,j) for i,j in PAIRS if not (blue[i]>>j&1)
                    and (blue[i]|blue[j]).bit_count()>=3]
        counts={'blue_form':name,'blue_pairs':edges,'red_candidates':candidates,
                'all_red_subsets':0,'at_least_three_red_subsets':0,
                'matching_budget_pass':0,'necessary_red_survivors':0,
                'inside_flag_survivors':0}
        for word in range(1<<len(candidates)):
            counts['all_red_subsets']+=1
            if word.bit_count()<3:continue
            counts['at_least_three_red_subsets']+=1
            red=[0]*Q;red_pairs=[]
            for index,edge in enumerate(candidates):
                if word>>index&1:
                    add(red,edge);red_pairs.append(edge)
            flags=inspect(red,blue)
            if flags is None:continue
            counts['matching_budget_pass']+=1
            if flags:
                counts['necessary_red_survivors']+=1
                counts['inside_flag_survivors']+=len(flags)
                records.append({'blue_form':name,'blue_pairs':edges,
                                'red_pairs':red_pairs,'flags':flags})
        cases.append(counts)
    args.records.write_text(json.dumps(records,indent=2)+'\n')
    summary={'agent':'six-books-2','role':'researcher','complete':True,
             'blue_uniform_pairs':4,'red_uniform_pairs_minimum':3,
             'blue_forms':len(cases),'all_red_subsets':sum(c['all_red_subsets'] for c in cases),
             'at_least_three_red_subsets':sum(c['at_least_three_red_subsets'] for c in cases),
             'matching_budget_pass':sum(c['matching_budget_pass'] for c in cases),
             'necessary_red_survivors':len(records),
             'inside_flag_survivors':sum(len(r['flags']) for r in records),'cases':cases,
             'full_matching_sign_enumeration':False,'wall_seconds':time.monotonic()-start}
    print(json.dumps(summary))


if __name__=='__main__':main()
