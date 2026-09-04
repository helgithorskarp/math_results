#!/usr/bin/env python3
"""Check that one DIMACS clause multiset is contained in another."""

import argparse
from collections import Counter


def read(path):
    clauses=[];variables=declared=None
    for line in open(path):
        if line.startswith('c') or not line.strip():continue
        if line.startswith('p'):
            _,kind,variables,declared=line.split();assert kind=='cnf';variables=int(variables);declared=int(declared);continue
        lits=tuple(map(int,line.split()));assert lits[-1]==0
        clauses.append(tuple(sorted(lits[:-1])))
    if len(clauses)!=declared:raise RuntimeError(f'{path}: header mismatch')
    return variables,clauses


def main():
    p=argparse.ArgumentParser();p.add_argument('whole');p.add_argument('subset');args=p.parse_args()
    whole_vars,whole=read(args.whole);sub_vars,sub=read(args.subset)
    if sub_vars>whole_vars:raise RuntimeError('subset declares more variables')
    wc=Counter(whole);sc=Counter(sub)
    missing={c:n-wc[c] for c,n in sc.items() if n>wc[c]}
    if missing:raise RuntimeError(f'{len(missing)} clause types are not contained')
    print(f'VERIFIED whole_clauses={len(whole)} subset_clauses={len(sub)} variables={whole_vars}')


if __name__=='__main__':main()
