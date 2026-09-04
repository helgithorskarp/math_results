#!/usr/bin/env python3
"""Map Ramsey-preserving edge-flip variants to canonical catalog records."""

import argparse
from collections import Counter


def main():
    p=argparse.ArgumentParser()
    p.add_argument('variants_tsv');p.add_argument('variant_canonical')
    p.add_argument('catalog_canonical');p.add_argument('complements_canonical')
    args=p.parse_args()
    base=open(args.catalog_canonical).read().splitlines();comp=open(args.complements_canonical).read().splitlines()
    lookup={g:('base',i) for i,g in enumerate(base)}
    for i,g in enumerate(comp):
        if g in lookup:raise RuntimeError('base/complement canonical sets overlap')
        lookup[g]=('complement',i)
    rows=[x.rstrip('\n').split('\t') for x in open(args.variants_tsv)]
    canonical=open(args.variant_canonical).read().splitlines()
    if len(rows)!=len(canonical):raise RuntimeError('variant/canonical length mismatch')
    counts=Counter();targets=set()
    print('radius\tparent\tedge_1\tedge_2\ttarget_kind\ttarget_index')
    for row,canon in zip(rows,canonical):
        if len(row)!=5:raise RuntimeError('bad variant row')
        radius,parent,e1,e2,_=row
        if canon not in lookup:raise RuntimeError(f'variant outside catalog at parent {parent}')
        kind,index=lookup[canon];print(f'{radius}\t{parent}\t{e1}\t{e2}\t{kind}\t{index}')
        counts[int(radius)]+=1;targets.add((kind,index))
    print(f'# SUMMARY radius1={counts[1]} radius2={counts[2]} distinct_targets={len(targets)}')


if __name__=='__main__':main()
