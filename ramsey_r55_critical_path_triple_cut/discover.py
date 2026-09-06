"""Optional bounded discovery of the degree-exact, two-outside-consistent example."""
import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
from math import lcm
from pathlib import Path
import resource
import time

MASKS = (5388912, 5404008, 5683824)  # red R(3,4;8), complemented below


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


@lru_cache(None)
def upper(p, q):
    if min(p, q) == 1:
        return 1
    a, b = upper(p-1, q), upper(p, q-1)
    return a + b - int(a % 2 == 0 and b % 2 == 0)


def core(mask):
    pairs = list(itertools.combinations(range(8), 2))
    red = {(0, 1), (0, 2)} | {(0, v) for v in range(3, 11)}
    red |= {(u+3, v+3) for i, (u, v) in enumerate(pairs) if not(mask >> i & 1)}
    rows = [0]*11
    for u, v in red:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def build(mask):
    g = core(mask)
    cliques = {}
    for color in (False, True):
        cliques[color] = {0: [0]}
        for k in range(1, 6):
            cliques[color][k] = [sum(1 << v for v in vs)
                for vs in itertools.combinations(range(11), k)
                if all(bool(g[u] >> v & 1) == color for u,v in itertools.combinations(vs,2))]
        need(not cliques[color][5], 'fixed core K5')
    domain = []
    for x in range(2048):
        if (x & 7) not in range(2, 8):
            continue
        if any(x & t == t for t in cliques[True][4]):
            continue
        if any(x & t == 0 for t in cliques[False][4]):
            continue
        domain.append(x)
    rows = []
    def add(coeff, bound, label):
        rows.append((tuple(coeff), bound, label))
    targets = [32] + [d-g[v].bit_count() for v,d in enumerate([20]*3+[21]*8)]
    equality = [[1]*len(domain)] + [[(x >> v)&1 for x in domain] for v in range(11)]
    for j,(row,b) in enumerate(zip(equality,targets)):
        add(row,b,['eq+',j]);add([-a for a in row],-b,['eq-',j])
    # Every actual extension obeys the full common-neighborhood union bounds.
    for a in range(4):
        for b in range(4):
            if a+b == 0:
                continue
            for A in cliques[True][a]:
                for B in cliques[False][b]:
                    if A & B:
                        continue
                    fixed = sum(not((A|B) >> v & 1) and g[v] & A == A and g[v] & B == 0
                                for v in range(11))
                    cap = upper(5-a,5-b)-1-fixed
                    coeff = [int(x & A == A and x & B == 0) for x in domain]
                    if any(coeff) or cap < 0:
                        add(coeff,cap,['root',A,B])
    # Identical rows are merged at the tightest bound, preserving a root label.
    merged = {}
    for a,b,label in rows:
        if a not in merged or b < merged[a][0]:
            merged[a] = (b,label)
    ordered = [(a,*merged[a]) for a in sorted(merged)]
    return g,domain,ordered


import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=30);args=parser.parse_args()
    need(args.seconds>0,'positive time bound');work=args.work;work.mkdir(exist_ok=False)
    start=time.monotonic();g,domain,rows=build(5388912)
    A=np.array([a for a,b,label in rows]);b=np.array([b for a,b,label in rows])
    result=milp(np.zeros(len(domain)),integrality=np.ones(len(domain)),bounds=Bounds(0,32),
                constraints=LinearConstraint(A,-np.inf,b),options={'time_limit':args.seconds})
    report={'status':'NO_INTEGER_WITNESS','solver_status':int(result.status),'message':result.message}
    if result.x is not None:
        x=[round(v) for v in result.x]
        if min(x)<0 or not all(sum(a*v for a,v in zip(row,x))<=bound for row,bound,_ in rows):
            raise ValueError('integer primal mismatch')
        types=[t for t,v in zip(domain,x) for _ in range(v)]
        if len(types)!=32:raise ValueError('typed vertex count')
        report.update(status='INTEGER_ATTACHMENTS_CHECKED',types=types)
        (work/'attachments.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        triples={c:[sum(1<<v for v in vs) for vs in itertools.combinations(range(11),3)
                    if all(bool(g[u]>>v&1)==c for u,v in itertools.combinations(vs,2))]
                 for c in (True,False)}
        fixed={};free=[]
        for i,j in itertools.combinations(range(32),2):
            red=not any(types[i]&types[j]&t==t for t in triples[True])
            blue=not any((types[i]|types[j])&t==0 for t in triples[False])
            if not(red or blue):raise ValueError('integer pair incompatibility')
            if red and blue:free.append((i,j))
            else:fixed[i,j]=red
        deg=np.zeros((32,len(free)),dtype=int)
        for j,(u,v) in enumerate(free):deg[u,j]=deg[v,j]=1
        debts=[21-types[i].bit_count()-sum(c for e,c in fixed.items() if i in e) for i in range(32)]
        completion=milp(np.zeros(len(free)),integrality=np.ones(len(free)),bounds=Bounds(0,1),
                        constraints=LinearConstraint(deg,debts,debts),options={'time_limit':args.seconds})
        report.update(pair_free_edges=len(free),pair_fixed_red=sum(fixed.values()),
                      pair_fixed_blue=len(fixed)-sum(fixed.values()),completion_status=int(completion.status),
                      completion_message=completion.message)
        if completion.x is not None:
            vals=[round(v) for v in completion.x]
            if any(v not in (0,1) for v in vals) or list(deg@np.array(vals))!=debts:raise ValueError('completion mismatch')
            red={(u,v) for u,v in itertools.combinations(range(11),2) if g[u]>>v&1}
            red|={(v,11+i) for i,t in enumerate(types) for v in range(11) if t>>v&1}
            red|={(11+u,11+v) for (u,v),c in fixed.items() if c}
            red|={(11+u,11+v) for (u,v),c in zip(free,vals) if c}
            doc={'n':43,'red_edges':[list(e) for e in sorted(red)]}
            (work/'graph.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
            report['status']='GRAPH_PENDING_LITERAL_CHECK'
    report['elapsed_seconds']=time.monotonic()-start
    (work/'result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
