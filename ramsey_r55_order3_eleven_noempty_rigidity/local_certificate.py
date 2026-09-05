#!/usr/bin/env python3
"""Small literal obstructions explaining all fifteen full-formula refutations."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import classify


def make():
    data=classify.classify();core=next(r for r in data['cores'] if r['index']==194)
    red=classify.red_edges(core['bits']);rows=[]
    for case in data['cases']:
        masks=[sum(b<<i for i,b in enumerate(word)) for word in case['prefixes']]
        pair=min(m for m in masks if m.bit_count()==2)
        i=next(i for i in range(4) if pair&(1<<i))
        fixed=[12+f for f,m in enumerate(masks) if m in (1<<i,pair)]
        outside=[j for j in range(4) if not pair&(1<<j)]
        edge=next((a,b) for a in range(3*outside[0],3*outside[0]+3) for b in range(3*outside[1],3*outside[1]+3) if (a,b) not in red)
        rows.append(dict(index=case['index'],fixed_masks=masks,blue_k5=sorted(fixed+list(edge)),
            forced_blue=[dict(edge=list(e),red_triangle=list(range(3*i,3*i+3))) for e in combinations(fixed,2)]))
    return dict(format='r55-r4-core194-local-obstructions-v1',core=194,bits=core['bits'],vertices=22,cases=rows)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.write_text(json.dumps(make(),indent=2,sort_keys=True)+'\n')
