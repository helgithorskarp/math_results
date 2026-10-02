#!/usr/bin/env python3
"""Full outside-cyclic pair model with one opposite-colored core satellite."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def need(condition,message):
    if not condition:
        raise ValueError(message)


def parameters(q,case,opposite):
    if q == 103:
        need(case in (1,2,3),'Unknown production hole representative')
        holes = ((5,53,101),(5,53,102),(5,54,101))[case-1]
        full = set(range(-2,7)) | {j*pow(2,-1,q)%q for j in (1,3,5,7)}
        core = tuple(sorted({x%q for x in full}-set(holes)))
        need(opposite in set(core)-set(range(5)),'Opposite point must be a regular satellite')
    else:
        need(q in (7,11,13) and case in (1,2,3),'Only specified small controls are supported')
        holes = (0,1,case+1)
        core = tuple(x for x in range(q) if x not in holes)[:3]
        need(opposite in core[1:],'Small opposite point is outside the fixed core or equals its root')
    regular = tuple(x for x in range(q) if x not in holes)
    need(regular[0] in core and opposite != regular[0],'Invalid anchored core')
    return holes,core,regular


def generate(q,case,opposite,path):
    holes,core,regular = parameters(q,case,opposite)
    root = regular[0]
    labels = {pair:i+1 for i,pair in enumerate(itertools.combinations(regular,2))}
    def edge(x,y):return labels[tuple(sorted((x,y)))]
    rows = set()
    for x,y in itertools.combinations(regular[1:],2):
        a,b,c = edge(root,x),edge(root,y),edge(x,y)
        rows.update(tuple(sorted(row)) for row in ((-a,b,c),(a,-b,c),(a,b,-c),(-a,-b,-c)))
    cycles = len(rows)
    ladders = set()
    for step in range(1,(q+1)//2):
        for start in range(q):
            ap = tuple((start+j*step)%q for j in range(7))
            if set(holes).intersection(ap):
                continue
            row = tuple(sorted(edge(ap[j],ap[j+3]) for j in range(4)))
            ladders.add(row)
            rows.add(row)
            rows.add(tuple(sorted(-x for x in row)))
    units = {(edge(root,x) if x == opposite else -edge(root,x),) for x in core if x != root}
    rows.update(units)
    raw = ('p cnf '+str(len(labels))+' '+str(len(rows))+'\n'+''.join(' '.join(map(str,row))+' 0\n' for row in sorted(rows))).encode()
    path.write_bytes(raw)
    return {'q':q,'case':case,'holes':list(holes),'regular_core':list(core),'opposite_satellite':opposite,
            'fixed_core_bits':[[x,int(x==opposite)] for x in core],'regular_columns':list(regular),
            'root':root,'variables':len(labels),'root_cycle_clauses':cycles,'seven_ladders':len(ladders),
            'fixed_core_units':len(units),'positive_core_units':1,'clauses':len(rows),
            'other_regular_bits_free':len(regular)-len(core),'counter_variables':0,'weight_cap':None,
            'no_five_assumption':False,'no_six_assumption':False,'extra_growth_cuts':0,
            'orientation_anchor':'u(root)=0 by global color exchange; no root unit',
            'hypothesis':'one specified regular core satellite has color one; all other regular core points have color zero',
            'cnf_sha256':hashlib.sha256(raw).hexdigest()}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--q',type=int,default=103)
    p.add_argument('--case',type=int,required=True)
    p.add_argument('--opposite',type=int,required=True)
    p.add_argument('--output',type=Path,required=True)
    a = p.parse_args()
    print(json.dumps(generate(a.q,a.case,a.opposite,a.output)))
