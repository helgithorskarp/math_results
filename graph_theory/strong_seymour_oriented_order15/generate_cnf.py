"""Exact oriented-graph Hall CNFs; see PROOF.md for the complete reduction.

The Hall encoding adapts strong_seymour_order15/generate_cnf.py to allow
missing arcs. Every UNSAT claim additionally requires an independent DRAT check.
"""
import argparse
import ctypes
import json
import itertools
from pathlib import Path
import time
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.pb import PBEnc
from pysat.solvers import Solver


def build(n,q=None,minimum_degree=6,source_size=6,root_max=None,audit_root=None,pivot_degree=None,audit_degrees=False):
    pool=IDPool();cnf=CNF()
    def e(i,j):
        if i==j:raise ValueError('loop')
        return pool.id(('e',i,j))
    def both(a,b,key):
        p=pool.id(key);cnf.extend([[-p,a],[-p,b],[p,-a,-b]]);return p
    ands={}
    def conj(a,b):
        key=tuple(sorted((a,b)))
        if key not in ands:ands[key]=both(a,b,('and',*key))
        return ands[key]
    def card(lits,k,kind='atleast',gate=None):
        clauses=getattr(CardEnc,kind)(lits,bound=k,vpool=pool,encoding=EncType.seqcounter).clauses
        cnf.extend(clauses if gate is None else [[-gate]+c for c in clauses])
    for i in range(n):
        for j in range(i):cnf.append([-e(i,j),-e(j,i)])
    # Take an arc-minimal counterexample before choosing the normalized root.
    # The elementary BLP arc-deletion argument makes every open directed
    # two-path have an alternate arc from another out-neighbor of its root.
    for u in (range(n) if audit_root is None and not audit_degrees else []):
        for v in range(n):
            if v==u:continue
            other=[w for w in range(n) if w not in (u,v)]
            into_v=[conj(e(u,w),e(w,v)) for w in other]
            for z in range(n):
                if z in (u,v):continue
                into_z=[conj(e(u,w),e(w,z)) for w in other if w!=z]
                cnf.append([-e(u,v),-e(v,z),e(u,z),*into_v,*into_z])
    for x in ([0] if audit_degrees else range(n) if audit_root is None else [audit_root]):
        deg=[e(x,y) for y in range(n) if y!=x]
        if audit_root is None:
            card(deg,minimum_degree)
            # Deleting an outgoing arc must make its tail strong. The new
            # degree d-1 cannot exceed the n-d possible second neighbors.
            card(deg,(n+1)//2,'atmost')
        high7=pool.id(('h7',x));high8=pool.id(('h8',x))
        if audit_root is None:
            for k,flag in [(7,high7),(8,high8)]:
                card(deg,k,gate=flag);card(deg,k-1,'atmost',-flag)
        else:cnf.extend([[high7],[-high8]])
        if audit_degrees:return cnf,pool
        left={y:pool.id(('left',x,y)) for y in range(n) if y!=x}
        right={z:pool.id(('right',x,z)) for z in range(n) if z!=x}
        clauses=[]
        for y,h in left.items():clauses.append([-h,e(x,y)])
        for z,r in right.items():
            products=[]
            for y,h in left.items():
                if y==z:continue
                p=both(h,e(y,z),('p',x,y,z));products.append(p)
                clauses.append([-p,e(x,z),r])
            clauses.extend([[-r,-e(x,z)],[-r]+products])
            twice=CardEnc.atleast(products,bound=2,vpool=pool,encoding=EncType.seqcounter).clauses if len(products)>=2 else [[]]
            clauses.extend([[-r]+c for c in twice])
        eq=CardEnc.equals(list(right.values())+[-h for h in left.values()],bound=n-2,vpool=pool,encoding=EncType.seqcounter)
        clauses.extend(eq.clauses)
        at3=CardEnc.atleast(list(left.values()),bound=3,vpool=pool,encoding=EncType.seqcounter) if len(left)>=3 else CNF(from_clauses=[[]])
        clauses.extend(at3.clauses if minimum_degree==7 else [[high7]+c for c in at3.clauses])
        for y,h in left.items():
            inside=[both(left[z],e(y,z),('ip',x,y,z)) for z in left if z!=y]
            clauses.append(([-h] if minimum_degree==7 else [high7,-h])+inside)
        cnf.extend([[high8]+c for c in clauses])
    if audit_root is not None:return cnf,pool
    # Normalize a minimum-degree root and an inclusion-minimal Hall witness.
    for y in range(1,n):
        cnf.append([e(0,y) if y<=minimum_degree else -e(0,y)])
        cnf.append([pool.id(('left',0,y)) if y<=source_size else -pool.id(('left',0,y))])
        is_target=minimum_degree<y<minimum_degree+source_size
        cnf.append([pool.id(('right',0,y)) if is_target else -pool.id(('right',0,y))])
    # The normalized Hall source is inclusion-minimal, so each proper
    # nonempty subset has at least its own size of distinct Hall targets.
    for k in range(1,source_size):
        for subset in itertools.combinations(range(1,source_size+1),k):
            hits=[]
            for z in range(minimum_degree+1,minimum_degree+source_size):
                h=pool.id(('subset_hit',subset,z));hits.append(h)
                cnf.append([-h,*[e(y,z) for y in subset]])
                cnf.extend([[-e(y,z),h] for y in subset])
            card(hits,k)
    if q is not None:
        if len(q)!=source_size:raise ValueError('wrong fixed source order')
        for i in range(source_size):
            for j in range(source_size):
                if i!=j:cnf.append([e(i+1,j+1) if q[i]>>j&1 else -e(i+1,j+1)])
    # Among minimum-degree roots choose x maximizing
    # M(x)=max_{y in N+(x)} |N+(x) intersect N+(y)|.
    # Thus any arc u->v with minimum-degree tail has common degree <=M(x).
    upper={}
    for t in range(2,minimum_degree):
        candidates=[]
        for y in range(1,minimum_degree+1):
            lits=[e(y,z) for z in range(1,minimum_degree+1) if z!=y]
            flag=pool.id(('root_internal_atleast',y,t));candidates.append(flag)
            card(lits,t,gate=flag);card(lits,t-1,'atmost',-flag)
        upper[t]=pool.id(('root_max_atleast',t))
        cnf.append([-upper[t],*candidates])
        cnf.extend([[-f,upper[t]] for f in candidates])
    beta={}
    for u in range(n):
        beta[u]=pool.id(('hall_size_atleast_root',u))
        card([pool.id(('left',u,v)) for v in range(n) if v!=u],source_size,gate=beta[u])
    false=pool.id(('constant_false',));cnf.append([-false])
    for u in range(n):
        for v in range(u+1,n):
            flagu=pool.id(('h7' if minimum_degree==6 else 'h8',u))
            flagv=pool.id(('h7' if minimum_degree==6 else 'h8',v))
            a=conj(e(u,v),-flagu);b=conj(e(v,u),-flagv)
            active=pool.id(('min_tail',u,v))
            cnf.extend([[-a,active],[-b,active],[-active,a,b]])
            common=[conj(e(u,w),e(v,w)) for w in range(n) if w not in (u,v)]
            for t,limit in upper.items():
                clauses=CardEnc.atmost(common,bound=t-1,vpool=pool,encoding=EncType.seqcounter).clauses
                cnf.extend([[-active,limit,*c] for c in clauses])
                # Among the maximum-M roots, x minimizes its smallest Hall
                # source size. If a minimum-degree tail u has M(u)=M(x),
                # every Hall source at u consequently has size >=source_size.
                next_limit=upper.get(t+1,false)
                cnf.extend([[-a,next_limit,beta[u],*c] for c in clauses])
                cnf.extend([[-b,next_limit,beta[v],*c] for c in clauses])
    if root_max is not None:
        if source_size!=minimum_degree or q is not None:raise ValueError('maximum normalization requires the whole source')
        if not 1<=root_max<minimum_degree:raise ValueError('bad maximum')
        for t,flag in upper.items():cnf.append([flag if root_max>=t else -flag])
        # S=R; relabel an internal maximum-degree vertex as 1 and its
        # internal out-neighbors as 2,...,root_max+1.
        for v in range(2,minimum_degree+1):
            cnf.append([e(1,v) if v<=root_max+1 else -e(1,v)])
    if pivot_degree is not None:
        if root_max is None:raise ValueError('pivot degree requires normalized maximum')
        card([e(1,j) for j in range(n) if j!=1],pivot_degree,'equals')
    # Sort the Hall-target columns; permuting those vertices fixes x and S.
    targets=list(range(minimum_degree+1,minimum_degree+source_size))
    for a,b in zip(targets,targets[1:]):
        lits=[];weights=[];bound=0
        for i in range(source_size):
            for coeff,direction in [(3**i,0),(2*3**i,1)]:
                la=e(i+1,a) if direction==0 else e(a,i+1)
                lb=e(i+1,b) if direction==0 else e(b,i+1)
                lits += [la,-lb];weights += [coeff,coeff];bound+=coeff
        cnf.extend(PBEnc.leq(lits,weights=weights,bound=bound,vpool=pool).clauses)
    return cnf,pool


CASES = {f"s{s}": (s, None, None) for s in (3, 4, 5)}
CASES.update({f"s6-m{m}": (6, m, None) for m in (1, 2, 3)})
CASES.update({f"s6-m{m}-p{p}": (6, m, p) for m in (4, 5) for p in (6, 7, 8)})


def case_formula(name):
    s, m, p = CASES[name]
    return build(15, minimum_degree=6, source_size=s, root_max=m, pivot_degree=p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=CASES)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    cnf, pool = case_formula(args.case)
    cnf.to_file(str(args.output))
    print(json.dumps({"case": args.case, "variables": pool.top,
                      "clauses": len(cnf.clauses)}))
