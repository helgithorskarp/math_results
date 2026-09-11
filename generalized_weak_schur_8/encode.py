#!/usr/bin/env python3
"""Exact prefix subset-sum encoding; see README.md for its mathematical scope."""
import argparse, json, time
from pathlib import Path

def generate(n, k, r):
    if not (2 <= k <= n and 1 <= r <= n):
        raise ValueError("Require 2 <= k <= n and 1 <= r <= n")
    clauses=[]
    top=n
    reach={}
    for c in [0,1]:
        previous={(0,0):0}  # zero is a constant true marker, never a literal.
        for i in range(1,r+1):
            current={(0,0):0}
            same=i if c else -i
            for j in range(1,min(i,k)+1):
                for s in range(j*(j+1)//2, min(n,j*(2*i-j+1)//2)+1):
                    top+=1; z=top; current[j,s]=z
                    if (j,s) in previous: clauses.append([-previous[j,s],z])
                    if (j-1,s-i) in previous:
                        prior=previous[j-1,s-i]
                        clauses.append(([-prior] if prior else [])+[-same,z])
            previous=current
        reach[c]=previous
        for (j,s),z in previous.items():
            if j==k:
                clauses.append([-z,-s if c else s])
            elif j==k-1:
                for x in range(r+1,n-s+1):
                    clauses.append([-z,-x if c else x,-(x+s) if c else x+s])
    return top,clauses

def main():
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,required=True)
    p.add_argument('--k',type=int,default=8);p.add_argument('--r',type=int,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--solver',default='glucose3')
    p.add_argument('--conflicts',type=int,default=300000)
    p.add_argument('--generate-only',action='store_true');args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    nv,clauses=generate(args.n,args.k,args.r)
    with (args.out/'input.cnf').open('w') as f:
        f.write(f'p cnf {nv} {len(clauses)}\n')
        for cl in clauses:f.write(' '.join(map(str,cl))+' 0\n')
    print(json.dumps({'variables':nv,'clauses':len(clauses),'generation_seconds':time.monotonic()-start}),flush=True)
    if args.generate_only:
        return
    from pysat.solvers import Solver
    with Solver(name=args.solver,bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(args.conflicts);result=solver.solve_limited()
        state={'n':args.n,'k':args.k,'r':args.r,'solver':args.solver,
            'status':'UNSAT' if result is False else 'RELAXATION_SAT' if result else 'BUDGET',
            'variables':nv,'clauses':len(clauses),'seconds':time.monotonic()-start,'stats':solver.accum_stats()}
        if result is False:(args.out/'proof.drat').write_text('\n'.join(solver.get_proof())+'\n')
        if result is True:
            model=solver.get_model();state['coloring']=[int(x>0) for x in model[:args.n]]
        (args.out/'result.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(state),flush=True)

if __name__=='__main__': main()
