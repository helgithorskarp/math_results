#!/usr/bin/env python3
"""Produce a GF2 inverse and complete low-parity weight histogram."""
import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


def need(ok,message):
    if not ok:
        raise ValueError(message)


def generate():
    n=102;ones=(1<<n)-1;seed=range(80,87)
    rows=[sum(1<<(k*x%103-1) for x in seed) for k in range(1,103)]
    augmented=[row | 1<<(n+i) for i,row in enumerate(rows)]
    for col in range(n):
        pivot=next((r for r in range(col,n) if augmented[r]>>col&1),None)
        need(pivot is not None,'Singular proposed orbit incidence matrix; no exclusion')
        augmented[col],augmented[pivot]=augmented[pivot],augmented[col]
        for r in range(n):
            if r!=col and augmented[r]>>col&1:
                augmented[r]^=augmented[col]
    need(all(augmented[i]&ones==1<<i for i in range(n)),'Left reduction failed')
    inverse_rows=[row>>n for row in augmented]
    inverse_columns=[sum(((inverse_rows[r]>>k)&1)<<r for r in range(n)) for k in range(n)]
    hist=Counter()
    for v in inverse_columns:
        hist[(ones^v).bit_count()]+=1
    for i,j,k in combinations(range(n),3):
        hist[(ones^inverse_columns[i]^inverse_columns[j]^inverse_columns[k]).bit_count()]+=1
    return {'agent':'six-vdw-3','role':'researcher','q':103,'period':618,
            'phase':[0,0,0,1,1,1],'seed_actual_AP':{'start':80,'step':1},
            'inverse_columns_hex':[hex(v) for v in inverse_columns],
            'parity_input_weights':[1,3],'parity_input_count':sum(hist.values()),
            'minimum_reconstructed_weight':min(hist),
            'complete_weight_histogram':dict(sorted(hist.items()))}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.write_text(json.dumps(generate(),indent=2)+'\n')
