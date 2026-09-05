#!/usr/bin/env python3
"""Discover, round and exactly repair a creation-sensitive LP dual."""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

import numpy as np
import scipy
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'ramsey_r55_visible_obstruction_cover/generate.py'
PARENT_SHA='99ff96f44dcb7d7de18f92bcd04f2403e60825447f8d8e5ffedbbdb3249d9132'

def require(ok,message):
    if not ok:
        raise ValueError(message)

def parent():
    require(hashlib.sha256(PARENT.read_bytes()).hexdigest()==PARENT_SHA,'parent generator changed')
    spec=importlib.util.spec_from_file_location('cover_producer',PARENT)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def mixed_rows(rows,edges):
    index={e:i for i,e in enumerate(edges)}
    clauses={}
    for root in range(3):
        for red in (True,False):
            side=[u for u in range(43) if u!=root and bool(rows[root]>>u&1)==red]
            for four in combinations(side,4):
                five=tuple(sorted((root,)+four))
                pairs=list(combinations(five,2))
                if any(bool(rows[u]>>v&1)!=red for u,v in pairs if u<3):
                    continue
                free=[(u,v) for u,v in pairs if u>=3]
                original=sum(rows[u]>>v&1 for u,v in free)
                coefficient={index[u,v]:(1-2*(rows[u]>>v&1))*(1 if red else -1) for u,v in free}
                rhs=len(free)-1-original if red else original-1
                clauses[int(red),five]=(coefficient,rhs)
    return sorted(clauses.items())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    args=ap.parse_args();args.work.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();cover=parent()
    rows,edges,visible,fives,ineq,rhs,eq=cover.model()
    # The new theorem intentionally omits ALL pointwise root inequalities.
    ineq=ineq[:len(fives)];rhs=rhs[:len(fives)]
    mixed=mixed_rows(rows,edges)
    ineq.extend(row for key,(row,b) in mixed);rhs.extend(b for key,(row,b) in mixed)
    A=cover.matrix(ineq,780);B=cover.matrix(eq,780)
    sol=linprog(visible,A_ub=A,b_ub=rhs,A_eq=B,b_eq=np.zeros(len(eq)),bounds=(0,1),method='highs',
                options={'time_limit':60.0})
    require(sol.success,'bounded LP discovery did not finish')
    D=10000
    alpha=[max(0,-round(float(y)*D)) for y in sol.ineqlin.marginals]
    beta=[round(float(z)*D) for z in sol.eqlin.marginals]
    load=[0]*780
    for a,row in zip(alpha,ineq):
        for j,v in row.items():load[j]-=a*v
    for b,row in zip(beta,eq):
        for j,v in row.items():load[j]+=b*v
    penalties=[max(0,l-D*c) for l,c in zip(load,visible)]
    numerator=-sum(a*b for a,b in zip(alpha,rhs))-sum(penalties)
    require(numerator>38*D,'rounded certificate does not cross the claimed boundary')
    certificate={
        'format':'r55-creation-sensitive-cover-dual-v1','seed_sha256':cover.SEED_SHA,'denominator':D,
        'old_cliques':[[red,list(S),a] for (red,S),a in zip(fives,alpha) if a],
        'mixed_cliques':[[red,list(S),a] for ((red,S),(row,b)),a in zip(mixed,alpha[len(fives):]) if a],
        'degrees':[[u,beta[u-3]] for u in range(3,43) if beta[u-3]],
        'profiles':[[u,int(red),beta[40+2*u+int(not red)]] for u in range(3) for red in (True,False)
                    if beta[40+2*u+int(not red)]],
        'upper_penalties':[[*e,p] for e,p in zip(edges,penalties) if p],
    }
    cover.save(args.work/'certificate.json',certificate)
    # Canonical formula fingerprints are reproducibility aids, not proof inputs.
    linear_rows=[[[[j,int(v)] for j,v in sorted(row.items())],int(b)] for row,b in zip(ineq,rhs)]
    formula_sha=hashlib.sha256((json.dumps(linear_rows,separators=(',',':'))+'\n').encode()).hexdigest()
    eq_sha=hashlib.sha256((json.dumps([sorted(row.items()) for row in eq],separators=(',',':'))+'\n').encode()).hexdigest()
    canonical_mixed=[[red,list(S),[[j,int(v)] for j,v in sorted(row.items())],b]
                     for (red,S),(row,b) in mixed]
    mixed_sha=hashlib.sha256((json.dumps(canonical_mixed,separators=(',',':'))+'\n').encode()).hexdigest()
    discovery={'status':'NUMERICAL_DISCOVERY; exact certificate must be checked','numpy':np.__version__,'scipy':scipy.__version__,
               'primary_variables':780,'old_cover_rows':len(fives),'mixed_rows':len(mixed),'equality_rows':len(eq),
               'pointwise_rows':0,'mixed_width_histogram':dict(sorted(Counter(len(row) for key,(row,b) in mixed).items())),
               'inequality_rows_sha256':formula_sha,'equality_rows_sha256':eq_sha,'mixed_rows_sha256':mixed_sha,
               'numerical_LP_value':float(sol.fun),'rounded_bound_numerator':numerator,'rounded_bound_denominator':D,
               'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    cover.save(args.work/'discovery.json',discovery)
    print(json.dumps(discovery,sort_keys=True))

if __name__=='__main__':main()
