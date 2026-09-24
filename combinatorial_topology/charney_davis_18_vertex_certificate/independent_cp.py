#!/usr/bin/env python3
"""Independent integer model: direct degrees and link edge counts, no CNF."""
import argparse
import itertools as it
import json
import time
from pathlib import Path
from ortools.sat.python import cp_model
from cases import enumerate_cases


def check(case, seconds):
    m=cp_model.CpModel(); vertices=range(18)
    pairs=list(it.combinations(vertices,2)); fixed={}
    edges={p:m.new_bool_var(f'e{p}') for p in pairs}
    def e(u,v): return edges[tuple(sorted((u,v)))]
    def fix(u,v,val):
        fixed[tuple(sorted((u,v)))]=bool(val); m.add(e(u,v)==int(val))
    for u,v in pairs:
        if v<6: fix(u,v,False)
        if u<6 and 6<=v<12: fix(u,v,v==u+6)
    for a,row in enumerate(case['edges']):
        for r in range(6): fix(a,r+12,r in row)
    degree=[m.new_int_var(3,7,f'q{v}') for v in vertices]
    high=[m.new_bool_var(f'h{v}') for v in vertices]
    for v in vertices:
        m.add(degree[v]==sum(e(u,v) for u in vertices if u!=v))
        m.add(degree[v]>=4).only_enforce_if(high[v])
        m.add(degree[v]==3).only_enforce_if(high[v].Not())
    m.add(sum(high)<=10)
    for a in range(case['k']): m.add(degree[a]==3)
    for a in range(case['k'],6):
        m.add(degree[a]>=4); m.add(degree[a+6]>=4)
    for a in range(5): m.add(degree[a]<=degree[a+1])
    for r in range(12,18): m.add(sum(e(a,r) for a in range(6))>=2)
    def conjunction(lits,name):
        z=m.new_bool_var(name)
        m.add_bool_and(lits).only_enforce_if(z)
        m.add_bool_or([x.Not() for x in lits]+[z])
        return z
    triangles={S:conjunction([e(*p) for p in it.combinations(S,2)],f't{S}')
               for S in it.combinations(vertices,3)}
    half_quad=[]; link_quad=[]
    for v in vertices:
        a=m.new_int_var(-15,-12,f'quad{v}')
        b=m.new_int_var(-42,-24,f'lquad{v}')
        m.add_allowed_assignments([degree[v],a,b],
              [(q,q*(q-11)//2,q*(q-19)//2) for q in range(3,8)])
        half_quad.append(a); link_quad.append(b)
    m.add(230+sum(half_quad)-sum(triangles.values())<=-1)
    complement_size=sum(edges.values())
    for v in vertices:
        terms=[]
        for u in vertices:
            if u==v: continue
            z=m.new_int_var(0,7,f'nq{v}_{u}')
            m.add_multiplication_equality(z,[e(u,v),degree[u]])
            terms.append(z)
        tv=sum(z for S,z in triangles.items() if v in S)
        m.add(47-complement_size+link_quad[v]+sum(terms)-tv>=0)
        m.add(tv<=1).only_enforce_if(high[v].Not())
    for u,v in pairs:
        common=[conjunction([e(u,w),e(v,w)],f'c{u}_{v}_{w}')
                for w in vertices if w not in (u,v)]
        m.add(sum(common)<=1).only_enforce_if([e(u,v).Not(),high[u].Not(),high[v].Not()])
    for S in it.combinations(vertices,5):
        internal=list(it.combinations(S,2))
        if any(fixed.get(p) is True for p in internal): continue
        face=conjunction([e(*p).Not() for p in internal],f'f{S}')
        extensions=[conjunction([e(u,v).Not() for u in S],f'x{S}_{v}')
                    for v in vertices if v not in S]
        m.add(sum(extensions)==2).only_enforce_if(face)
    for S in it.combinations(vertices,7):
        internal=list(it.combinations(S,2))
        if not any(fixed.get(p) is True for p in internal):
            m.add_bool_or([e(*p) for p in internal])
    solver=cp_model.CpSolver(); solver.parameters.num_search_workers=1
    solver.parameters.random_seed=1; solver.parameters.max_time_in_seconds=seconds
    status=solver.solve(m)
    return {'id':case['id'],'status':solver.status_name(status),
            'conflicts':solver.num_conflicts,'branches':solver.num_branches,
            'wall_seconds':round(solver.wall_time,6)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seconds',type=int,default=60)
    ap.add_argument('--output',type=Path,required=True); ap.add_argument('--case')
    args=ap.parse_args(); rows=[]
    for case in enumerate_cases():
        if args.case and case['id']!=args.case: continue
        row=check(case,args.seconds); rows.append(row)
        args.output.write_text(json.dumps(rows,indent=2)+'\n'); print(json.dumps(row),flush=True)
        if row['status']!='INFEASIBLE': raise RuntimeError('Independent validation incomplete')
    if not args.case: assert len(rows)==25


if __name__=='__main__': main()
