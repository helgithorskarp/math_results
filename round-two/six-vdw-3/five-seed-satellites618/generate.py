#!/usr/bin/env python3
"""Full outside-carrier pair system with an explicit monochromatic local core."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def parameters(q,case):
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'Prime q>=7 required')
    if q==103:
        need(case in (1,2,3),'Unknown production seed-hole case')
        holes=((5,53,101),(5,53,102),(5,54,101))[case-1]
        seed=tuple(sorted(set(range(5))|{101,102,5,6,52,53,54,55}-set(holes)))
    else:
        need(q in (7,11,13) and 1<=case<=3,'Only specified small controls supported')
        holes=(0,1,case+1)
        seed=tuple(x for x in range(q) if x not in holes)[:3]
    outside=tuple(x for x in range(q) if x not in holes)
    need(len(holes)==3 and set(seed)<=set(outside) and outside[0] in seed,'Invalid core seed')
    return holes,seed,outside

def generate(q,case,path):
    holes,seed,outside=parameters(q,case);root=outside[0]
    labels={pair:i+1 for i,pair in enumerate(itertools.combinations(outside,2))}
    def edge(x,y):return labels[tuple(sorted((x,y)))]
    rows=set()
    for x,y in itertools.combinations(outside[1:],2):
        a,b,c=edge(root,x),edge(root,y),edge(x,y)
        rows.update(tuple(sorted(row)) for row in ((-a,b,c),(a,-b,c),(a,b,-c),(-a,-b,-c)))
    cycle_count=len(rows);ladders=set()
    for step in range(1,(q+1)//2):
        for start in range(q):
            points=tuple((start+j*step)%q for j in range(7))
            if not set(holes).intersection(points):
                row=tuple(sorted(edge(points[j],points[j+3]) for j in range(4)))
                ladders.add(row);rows.add(row);rows.add(tuple(sorted(-x for x in row)))
    units={(-edge(root,x),) for x in seed if x!=root};rows.update(units)
    raw=('p cnf '+str(len(labels))+' '+str(len(rows))+'\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(rows))).encode()
    path.write_bytes(raw)
    return {'q':q,'case':case,'holes':list(holes),'seed':list(seed),'regular_columns':list(outside),'root':root,
            'variables':len(labels),'root_cycle_clauses':cycle_count,'seven_ladders':len(ladders),
            'seed_units':len(units),'clauses':len(rows),'counter_variables':0,'weight_cap':None,
            'hypothesis':'all regular local-core field points have the five-AP seed color',
            'orientation_anchor':'u(root)=0 by global color exchange','cnf_sha256':hashlib.sha256(raw).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',type=int,default=103)
    p.add_argument('--case',type=int,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(generate(a.q,a.case,a.output)))
