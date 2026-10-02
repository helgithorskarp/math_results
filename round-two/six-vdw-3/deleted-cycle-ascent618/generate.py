#!/usr/bin/env python3
"""Deleted seven-ladder system with no field-five seed, in exact pair parities."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def generate(q,lam,path):
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'Prime q>=7 required')
    need(1<lam<q,'Invalid normalized holes')
    holes={0,1,lam};outside=tuple(x for x in range(q) if x not in holes);root=outside[0]
    labels={pair:i+1 for i,pair in enumerate(itertools.combinations(outside,2))}
    def edge(x,y):return labels[tuple(sorted((x,y)))]
    rows=set()
    for x,y in itertools.combinations(outside[1:],2):
        a,b,c=edge(root,x),edge(root,y),edge(x,y)
        rows.update(tuple(sorted(row)) for row in ((-a,b,c),(a,-b,c),(a,b,-c),(-a,-b,-c)))
    cycle_count=len(rows);ladders=set();five=set()
    for step in range(1,(q+1)//2):
        for start in range(q):
            points=tuple((start+j*step)%q for j in range(7))
            if not holes.intersection(points):
                row=tuple(sorted(edge(points[j],points[j+3]) for j in range(4)))
                ladders.add(row);rows.add(row);rows.add(tuple(sorted(-x for x in row)))
            points=tuple((start+j*step)%q for j in range(5))
            if not holes.intersection(points):
                support=tuple(sorted(points));five.add(support)
    for support in five:rows.add(tuple(sorted(edge(support[0],x) for x in support[1:])))
    raw=('p cnf '+str(len(labels))+' '+str(len(rows))+'\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(rows))).encode()
    path.write_bytes(raw)
    return {'q':q,'lambda':lam,'holes':sorted(holes),'regular_columns':list(outside),'root':root,
            'variables':len(labels),'root_cycle_clauses':cycle_count,'seven_ladders':len(ladders),
            'no_five_supports':len(five),'clauses':len(rows),'orientation_anchor':'u(root)=0 only in decoding; no unit clause',
            'hypothesis':'no monochromatic five-term field AP avoiding holes','counter_variables':0,
            'cnf_sha256':hashlib.sha256(raw).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--q',type=int,default=103)
    p.add_argument('--lambda',dest='lam',type=int,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(generate(a.q,a.lam,a.output)))
