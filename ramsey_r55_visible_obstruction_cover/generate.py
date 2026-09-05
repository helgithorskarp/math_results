#!/usr/bin/env python3
"""Numerical discovery only; verify.py supplies exact proof and graph checks."""
import argparse
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

import numpy as np
import scipy
from scipy.optimize import linprog, milp, Bounds, LinearConstraint
from scipy.sparse import csr_matrix, vstack

HERE = Path(__file__).resolve().parent
SEED = HERE.parent/'ramsey_r55_k5_neutral_component/EXIT_GRAPH.json'
SEED_SHA = '9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916'
PINS = {
    'ramsey_r55_triple_graph_realization/verify.py':'154358fe08d7c07f2818aa4105ce127d3767a4af736362d55c7ba79ed683c207',
    'ramsey_r55_cell_preserving_repair/verify.py':'4e92829610eb2fe6956a42365c9de77d5c639541aefd44d3d05b896a94697cd0',
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def save(path, value):
    pending = path.with_suffix(path.suffix+'.pending')
    pending.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    pending.replace(path)

def load(relative):
    path = HERE.parent/relative
    require(hashlib.sha256(path.read_bytes()).hexdigest()==PINS[relative], 'dependency changed')
    spec = importlib.util.spec_from_file_location(path.parent.name,path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def model():
    require(hashlib.sha256(SEED.read_bytes()).hexdigest()==SEED_SHA,'seed changed')
    audit = load('ramsey_r55_triple_graph_realization/verify.py')
    check = load('ramsey_r55_cell_preserving_repair/verify.py')
    rows = audit.decode(json.loads(SEED.read_text()))
    adj = check.neighbors(rows)
    edges = list(combinations(range(3,43),2))
    ix = {e:i for i,e in enumerate(edges)}
    signs = [1-2*int(v in adj[u]) for u,v in edges]
    visible = [int((rows[u]&7)^(rows[v]&7)!=7) for u,v in edges]
    fives = [(int(red),S) for red in (True,False) for S in sorted(audit.monochromatic_bitsets(rows,red))]
    inequalities = [{ix[e]:-1 for e in combinations(S,2)} for red,S in fives]
    rhs = [-1]*len(fives)
    equalities = [{i:signs[i] for i,e in enumerate(edges) if u in e} for u in range(3,43)]
    for u in range(3):
        for red in (True,False):
            S = adj[u] if red else set(range(43))-adj[u]-{u}
            equalities.append({i:signs[i] for i,(a,b) in enumerate(edges) if a in S and b in S})
    for u,red,S,cap,A,B in check.conditions(adj):
        inequalities.append({ix[tuple(sorted((u,v)))]:signs[ix[tuple(sorted((u,v)))]]*(1 if red else -1)
                             for v in S if min(u,v)>=3})
        actual = len(S&adj[u]) if red else len(S-adj[u])
        rhs.append(cap-actual)
    return rows,edges,visible,fives,inequalities,rhs,equalities

def matrix(records,n):
    rr,cc,dd=[],[],[]
    for i,row in enumerate(records):
        for j,v in row.items():
            rr.append(i); cc.append(j); dd.append(v)
    return csr_matrix((dd,(rr,cc)),shape=(len(records),n),dtype=float)

def exact_dual(sol,objective,denominator,edges,fives,inequalities,equalities):
    # Round the discovery dual; exact upper-box penalties repair every
    # overloaded edge. No solver feasibility or optimality is a proof input.
    alpha = [max(0,-round(float(y)*denominator)) for y in sol.ineqlin.marginals]
    beta = [round(float(z)*denominator) for z in sol.eqlin.marginals]
    load = [0]*len(edges)
    for a,row in zip(alpha,inequalities):
        for j,v in row.items():
            load[j] -= a*v
    for b,row in zip(beta,equalities):
        for j,v in row.items():
            load[j] += b*v
    penalties = [max(0,l-denominator*c) for l,c in zip(load,objective)]
    return {
        'denominator':denominator,
        'cliques':[[red,list(S),a] for (red,S),a in zip(fives,alpha) if a],
        'degrees':[[u,beta[u-3]] for u in range(3,43) if beta[u-3]],
        'profiles':[[u,int(red),beta[40+2*u+int(not red)]] for u in range(3) for red in (True,False)
                    if beta[40+2*u+int(not red)]],
        'upper_penalties':[[*edge,p] for edge,p in zip(edges,penalties) if p],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--seconds',type=float,default=60)
    ap.add_argument('--certificates-only',action='store_true')
    args = ap.parse_args()
    require(args.seconds>0,'positive bound required')
    args.work.mkdir(parents=True,exist_ok=False)
    start = time.monotonic()
    rows,edges,visible,fives,ineq,rhs,eq = model()
    A,B = matrix(ineq,len(edges)),matrix(eq,len(edges))
    proof = {'format':'r55-visible-obstruction-cover-duals-v1','seed_sha256':SEED_SHA}
    discovery = {'numpy':np.__version__,'scipy':scipy.__version__,'primary_variables':len(edges),
                 'old_K5_rows':len(fives),'pointwise_rows':len(ineq)-len(fives),'equalities':len(eq),'LP':{}}
    for name,obj,denom in [('visible',visible,12),('total',[1]*780,1000)]:
        sol=linprog(obj,A_ub=A[:len(fives)],b_ub=rhs[:len(fives)],A_eq=B,b_eq=[0]*len(eq),
                    bounds=(0,1),method='highs')
        require(sol.success,'LP discovery did not finish')
        proof[name]=exact_dual(sol,obj,denom,edges,fives,ineq[:len(fives)],eq)
        discovery['LP'][name]={'numerical_objective':float(sol.fun),'status':int(sol.status)}
    save(args.work/'certificate.json',proof)
    if not args.certificates_only:
        sol=milp(visible,integrality=np.ones(780),bounds=Bounds(0,1),
                 constraints=LinearConstraint(vstack([A,B]),np.r_[np.full(len(ineq),-np.inf),np.zeros(len(eq))],
                                              np.r_[rhs,np.zeros(len(eq))]),
                 options={'time_limit':args.seconds,'mip_rel_gap':0.0})
        discovery['MIP']={'status':int(sol.status),'message':sol.message,'seconds_limit':args.seconds,
                          'numerical_objective':float(sol.fun) if sol.fun is not None else None}
        if sol.x is not None:
            new=list(rows)
            for (u,v),x in zip(edges,sol.x):
                if x>0.5:
                    new[u]^=1<<v; new[v]^=1<<u
            save(args.work/'GRAPH.json',{'format':'r55-triple-degree-exact-mixed-graph-v1',
                                       'red_adjacency_hex':[format(r,'x') for r in new]})
        else:
            discovery['status']='NO_INTEGER_WITNESS; stored exact bounds may still verify'
    discovery['elapsed_seconds']=time.monotonic()-start
    discovery['peak_RSS_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    save(args.work/'discovery.json',discovery)
    print(json.dumps(discovery,sort_keys=True))

if __name__=='__main__':
    main()
