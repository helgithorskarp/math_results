"""Exact exploratory quotient budgets at exactly two red uniform pairs.
Author: six-books-2, role researcher. No matching signing is enumerated.
Coverage requires the separate written low-clique/attachment reduction.
"""
from itertools import combinations, product
from pathlib import Path
import argparse, json, time

Q=11
PAIRS=list(combinations(range(Q),2))
ALL_FLAGS=(1<<(1<<Q))-1
ONE_FLAGS=[sum(1<<word for word in range(1<<Q) if word>>i&1) for i in range(Q)]
SUM_FLAGS={(i,j):(ALL_FLAGS & ~(ONE_FLAGS[i]|ONE_FLAGS[j]),ONE_FLAGS[i]^ONE_FLAGS[j],ONE_FLAGS[i]&ONE_FLAGS[j]) for i,j in PAIRS}


def partitions(n, first):
    for triples in range(n//3+1):
        for doubles in range((n-3*triples)//2+1):
            singles=n-3*triples-2*doubles
            sizes=[1]*singles+[2]*doubles+[3]*triples
            blocks=[];start=first
            for size in sizes:
                blocks.append(tuple(range(start,start+size)));start+=size
            yield (singles,doubles,triples),blocks


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


def add(neighbors,edge):
    i,j=edge;neighbors[i]|=1<<j;neighbors[j]|=1<<i


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records',type=Path,required=True)
    parser.add_argument('--progress',action='store_true')
    args=parser.parse_args()
    start=time.monotonic();cases=[];survivors=[]
    for name,edges,active in [('adjacent',[(0,1),(0,2)],3),('disjoint',[(0,1),(2,3)],4)]:
        red=[0]*Q
        for edge in edges:add(red,edge)
        possible_active=[p for p in combinations(range(active),2) if p not in edges]
        active_options=[[(1,2)]] if active==3 else [list(subset) for n in range(5) for subset in combinations(possible_active,n)]
        for shape,blocks in partitions(Q-active,active):
            counts={'form':name,'low_cliques':shape,'raw_patterns':0,'red_F_pass':0,'matching_budget_pass':0,'color_survivors':0,'inside_flag_survivors':0}
            base=[0]*Q
            for block in blocks:
                for edge in combinations(block,2):add(base,edge)
            attachments=[()]+[subset for block in blocks if len(block)<=2 for size in range(1,len(block)+1) for subset in combinations(block,size)]
            for active_blue in active_options:
                active_base=base.copy()
                for edge in active_blue:add(active_base,edge)
                for attach in product(attachments,repeat=active):
                    counts['raw_patterns']+=1;blue=active_base.copy()
                    for i,subset in enumerate(attach):
                        for j in subset:add(blue,(i,j))
                    if any((blue[i]|blue[j]).bit_count()<3 for i,j in edges):continue
                    counts['red_F_pass']+=1
                    flags=inspect(red,blue)
                    if flags is None:continue
                    counts['matching_budget_pass']+=1
                    if flags:
                        counts['color_survivors']+=1;counts['inside_flag_survivors']+=len(flags)
                        mask=sum(1<<index for index,(i,j) in enumerate(PAIRS) if blue[i]>>j&1)
                        survivors.append({'form':name,'low_cliques':shape,'active_blue':active_blue,'attachments':attach,'blue_mask':mask,'flags':flags})
            cases.append(counts)
            if args.progress:print(json.dumps(counts),flush=True)
    args.records.write_text(json.dumps(survivors,indent=2)+'\n')
    summary={'agent':'six-books-2','role':'researcher','complete':True,'cases':cases,'raw_patterns':sum(c['raw_patterns'] for c in cases),'color_survivors':len(survivors),'inside_flag_survivors':sum(c['inside_flag_survivors'] for c in cases),'wall_seconds':time.monotonic()-start,'full_matching_sign_enumeration':False}
    print(json.dumps(summary))

if __name__=='__main__':main()
