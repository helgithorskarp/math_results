#!/usr/bin/env python3
"""Finite sorting controls and literal candidate-rejection controls."""
import copy
import itertools as it
import json
from fractions import Fraction
from pathlib import Path
import tempfile
import degree_filter
import verify_rejection
import independent_check


def require(ok,message):
    if not ok:
        raise ValueError(message)


def reject(call):
    try:
        call()
    except (ValueError,KeyError):
        return
    raise ValueError('corruption accepted')


def sorting():
    # Three equal-color blocks, four possible root keys, three free cross bits.
    # Exhaust every graph in this finite analog; predicates are block-invariant.
    pairs=list(it.combinations(range(3),2))
    cases=[]
    for keys in it.product(range(4),repeat=3):
        for word in range(8):
            degree=[keys[i]+sum((word>>k)&1 for k,p in enumerate(pairs) if i in p) for i in range(3)]
            predicates=[all(lo<=v<=hi for v in degree) for lo,hi in ((0,2),(1,3),(2,4),(3,5))]
            predicates.append(keys==(0,0,0))
            cases.append((keys,word,predicates))
    ordered=[x for x in cases if tuple(sorted(x[0],reverse=True))==x[0]]
    repeated=[x for x in ordered if len(set(x[0]))<3]
    require((len(cases),len(ordered),len(repeated))==(512,160,128),'toy carrier count')
    for k in range(5):
        parent=sum(x[2][k] for x in cases)
        selected=sum(x[2][k] for x in ordered)
        pd=sum(x[2][k] and len(set(x[0]))==3 for x in cases)
        sd=sum(x[2][k] and len(set(x[0]))==3 for x in ordered)
        require(pd==6*sd,'distinct-root transport failed')
        require(selected<=Fraction(parent,6)+len(repeated),'safe transfer failed')
    require(sum(x[2][-1] for x in ordered)>Fraction(sum(x[2][-1] for x in cases),6),
            'control failed to detect unsafe factorial division')
    return {'toy_graphs':512,'invariant_predicates':5,'unsafe_factorial_division_detected':True}


def main():
    pairs=list(it.combinations(range(43),2))
    graphs=[]
    for bit in (0,1):
        graphs.append({'n':43,'red_hex':format(((1<<903)-1)*bit,'0226x')})
    witnesses=[]
    for g in graphs:
        c=degree_filter.check(g);verify_rejection.verify(g,c);witnesses.append(c)
    # Two disjoint cliques: degrees pass, but this is plainly not a Ramsey graph.
    value=sum(1<<i for i,(u,v) in enumerate(pairs) if (u<21)==(v<21))
    balanced={'n':43,'red_hex':format(value,'0226x')}
    require(degree_filter.check(balanced)['status']=='DEGREE_PASS_NO_RAMSEY_VERDICT',
            'degree pass overstated')
    bad=copy.deepcopy(witnesses[0]);bad['vertices'][1]=bad['vertices'][0]
    reject(lambda:verify_rejection.verify(graphs[0],bad))
    bad2=copy.deepcopy(witnesses[0]);bad2['color']^=1
    reject(lambda:verify_rejection.verify(graphs[0],bad2))
    reject(lambda:verify_rejection.verify(graphs[1],witnesses[0]))
    reject(lambda:degree_filter.check({'n':43,'red_hex':'8'+'0'*225}))
    # Polynomial audit controls exercise mixed powers and exact coefficient mass.
    p=[0]*25;p[0]=2;p[6]=3
    require(independent_check.pair_product([p]*2,18)==(25,25),'Kronecker control')
    # Direct twofold-cover inequality on a triangle of independent bits.
    assignments=list(it.product((0,1),repeat=3));relations=list(it.product((0,1),repeat=4))
    inequalities=0
    for a,b,c in it.product(relations,repeat=3):
        count=sum(a[2*x+y] and b[2*y+z] and c[2*x+z] for x,y,z in assignments)
        require(count*count <= sum(a)*sum(b)*sum(c),'twofold inequality control')
        inequalities+=1
    print(json.dumps({'status':'CONTROLS_PASS','sorting':sorting(),
                      'literal_graph_rejections':2,'degree_pass_without_ramsey_verdict':True,
                      'corruptions_rejected':4,'small_product_inequalities':inequalities},sort_keys=True))


if __name__=='__main__':
    main()
