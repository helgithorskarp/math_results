#!/usr/bin/env python3
"""Exact pair/triple interaction formula for sparse signed edge counts."""
import argparse
import json
from pathlib import Path
from generate import patterns

def need(condition,message):
    if not condition:raise ValueError(message)

def edge_count(q,kind,lam):
    need(q>=11 and kind in ('same','mixed') and 1<lam<q,'Bad density parameters')
    zero=(0,)*7;m0=len(patterns(zero));need(m0==8,'Constant local count')
    need(all(len(patterns(tuple(int(i==j) for i in range(7))))==14 for j in range(7)),'Single count')
    pair_sums={}
    for second in (1,2):
        total=0
        for left in range(7):
            for right in range(left+1,7):
                row=[0]*7;row[left]=1;row[right]=second
                total+=len(patterns(tuple(row)))-20
        pair_sums[second]=total
    need(pair_sums=={1:-106,2:-60},'Pair interaction counts')
    base=4*q*(q-1)+63*(q-1)+(3*pair_sums[1] if kind=='same' else pair_sums[1]+2*pair_sums[2])
    correction=0;triples=[];supports=set()
    for left in range(7):
        for right in range(left+1,7):
            step=pow(right-left,-1,q);start=(-left*step)%q
            points=tuple((start+j*step)%q for j in range(7))
            if lam not in points:continue
            key=tuple(sorted(points));need(key not in supports,'Duplicate pair carrier');supports.add(key)
            positions=(points.index(0),points.index(1),points.index(lam))
            labels=(1,1,1 if kind=='same' else 2);full=[0]*7
            for pos,value in zip(positions,labels):full[pos]=value
            m3=len(patterns(tuple(full)));pair_counts=[]
            for omitted in range(3):
                row=full.copy();row[positions[omitted]]=0
                pair_counts.append(len(patterns(tuple(row))))
            term=m3-sum(pair_counts)+34;correction+=term
            triples.append({'positions':list(positions),'three_edge_count':m3,'pair_edge_counts':pair_counts,'third_difference':term})
    return {'q':q,'kind':kind,'lambda':lam,'base_pair_count':base,
            'triple_carriers':len(triples),'triple_interaction_sum':correction,
            'signed_edges':base+correction,'cnf_clauses':2*(base+correction)+1,
            'triple_terms':triples}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--q',type=int,default=103)
    parser.add_argument('--kind',choices=('same','mixed'),required=True);parser.add_argument('--lambda',dest='lam',type=int,required=True)
    args=parser.parse_args();print(json.dumps(edge_count(args.q,args.kind,args.lam)))

if __name__=='__main__':main()
