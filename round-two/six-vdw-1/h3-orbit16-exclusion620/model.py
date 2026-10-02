"""Arbitrary antipodal phase rows on chosen multiplicative field cosets."""
import argparse
import json
from math import gcd
from pathlib import Path

SCOPE='Chosen multiplicative subgroup field invariance; arbitrary antipodal phase rows; all actual cyclic regular APs; poles absent.'


def build(q,half,length,H,fixed=None,palette=False):
    if not all(type(x) is int for x in [q,half,length]) or not(3<=q<=31 and 1<=half<=10 and 2<=length<=7):
        raise ValueError('bounded physical domain')
    if any(q%d==0 for d in range(2,q)) or gcd(q,2*half)!=1:
        raise ValueError('prime/CRT domain')
    if type(H) is not list or not H or any(type(h) is not int or not 1<=h<q for h in H) or H!=sorted(set(H)) or 1 not in H or any(a*b%q not in H for a in H for b in H):
        raise ValueError('explicit actual multiplicative subgroup')
    if type(palette) is not bool or (fixed is not None and(type(fixed) is not int or not 0<=fixed<2**half or palette)):
        raise ValueError('fixed-row/palette domain')
    remaining=set(range(1,q));cosets=[]
    while remaining:
        r=min(remaining);coset=sorted({r*h%q for h in H})
        if len(coset)!=len(H) or not set(coset)<=remaining:raise ValueError('complete disjoint coset cover')
        cosets.append(coset);remaining-=set(coset)
    lookup={r:i for i,c in enumerate(cosets) for r in c}
    n=2*q*half;nv=half*len(cosets)
    points=[None if x%q==0 else (1 if x%(2*half)<half else -1)*(half*lookup[x%q]+x%half+1) for x in range(n)]
    AP=set()
    # Reversal covers both directions. The separate auditor visits every first/second pair.
    for start in range(n):
        for step in range(1,n//2+1):
            terms=[points[(start+j*step)%n] for j in range(length)]
            if None in terms:continue
            support=set(terms)
            if any(-v in support for v in support):continue
            for sign in [1,-1]:AP.add(tuple(sorted((sign*v for v in support),key=lambda v:(abs(v),v))))
    fixed_units=[] if fixed is None else [[j+1 if (fixed>>j)&1 else -(j+1)] for j in range(half)]
    palette_units=[[-1]] if palette else []
    clauses=AP|{tuple(c) for c in fixed_units+palette_units}
    return {'author':'six-vdw-1','role':'researcher','model_kind':'arbitrary_subgroup_antipodal_regular',
            'field_prime':q,'row_half':half,'AP_length':length,'period':n,'subgroup':H,
            'cosets':cosets,'fixed_first_coset_row':fixed,'palette':palette,'variables':nv,
            'free_point_inputs_before_AP':nv-(half if fixed is not None else int(palette)),
            'point_literals':points,'membership_clauses':[],'fixed_row_clauses':fixed_units,
            'palette_clauses':palette_units,'distinct_AP_clauses':len(AP),
            'clauses':[list(c) for c in sorted(clauses)],'scope':SCOPE}


def write(d,path):
    if path.exists() or path.with_suffix('.cnf').exists():raise ValueError('preserve model')
    path.write_text(json.dumps(d,sort_keys=True)+'\n')
    path.with_suffix('.cnf').write_text(f"p cnf {d['variables']} {len(d['clauses'])}\n"+''.join(' '.join(map(str,c))+' 0\n' for c in d['clauses']))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args()
    d=build(31,10,7,[1,5,25],16);write(d,a.output)
    print(json.dumps({k:d[k] for k in ['model_kind','variables','free_point_inputs_before_AP','distinct_AP_clauses','subgroup','cosets','fixed_first_coset_row','scope']}|{'clauses':len(d['clauses']),'membership_clauses':0},sort_keys=True),flush=True)
