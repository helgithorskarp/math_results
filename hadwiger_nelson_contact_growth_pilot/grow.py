#!/usr/bin/env python3
"""Four capped exact contact-growth trajectories; requires python-sat1.9.dev15."""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import time

DEN=96
LIMIT=508
CAP=100000
RUN_CAP=500000
BANK=4

def add(p,q):return tuple(a+b for a,b in zip(p,q))
def sub(p,q):return tuple(a-b for a,b in zip(p,q))

def norm(p):
    a,b,c,d,e,f,g,h=p
    return (a*a+5*b*b+33*c*c+165*d*d+3*e*e+15*f*f+11*g*g+55*h*h,
            2*(a*b+33*c*d+3*e*f+11*g*h),
            2*(a*c+5*b*d+e*g+5*f*h),
            2*(a*d+b*c+e*h+f*g))

def unit(p):return norm(p)==(DEN*DEN,0,0,0)

def rho(p):
    a,b,c,d,e,f,g,h=p
    q=(7*a-15*f,7*b-3*e,7*c-5*h,7*d-g,5*b+7*e,a+7*f,15*d+7*g,3*c+7*h)
    if any(v%8 for v in q):raise ValueError('rho image not integral')
    return tuple(v//8 for v in q)

def geometry():
    native=[]
    for a,b,c,d in product(range(-12,13),range(-2,3),range(-6,7),range(-3,4)):
        if a*a+33*b*b+3*c*c+11*d*d==144 and a*b+c*d==0:
            native.append((8*a,0,8*b,0,8*c,0,8*d,0))
    steps=sorted(set(native+[rho(v) for v in native]))
    raw=[(0,0,0,0),(12,0,0,0),(6,0,6,0),(18,0,6,0),
         (10,0,0,2),(5,-1,5,1),(15,-1,5,3)]
    spindle=[(8*a,0,8*b,0,8*c,0,8*d,0) for a,b,c,d in raw]
    seed=spindle+[rho(v) for v in spindle[1:]]
    if len(steps)!=60 or len(set(seed))!=13 or not all(map(unit,steps)):
        raise ValueError('geometry control failed')
    return steps,seed

def clauses_vertex(v):
    return [[4*v+c+1 for c in range(4)]]+[[-4*v-a-1,-4*v-b-1] for a in range(4) for b in range(a)]

def clauses_edge(a,b):return [[-4*a-c-1,-4*b-c-1] for c in range(4)]

def colour_model(solver,n):
    model=set(x for x in solver.get_model() if x>0)
    out=[]
    for v in range(n):
        cs=[c for c in range(4) if 4*v+c+1 in model]
        if len(cs)!=1:raise ValueError('invalid one-hot model')
        out.append(cs[0])
    return out

def tie_value(run,p):
    return int.from_bytes(hashlib.sha256((str(run)+':'+','.join(map(str,p))).encode()).digest()[:8],'big')

def run_case(run,work):
    from pysat.solvers import Solver
    steps,points=geometry();where={p:i for i,p in enumerate(points)}
    pool={};tape=[];edges=[];bank=[];log=[]
    def offer(v):
        p=points[v]
        for si,s in enumerate(steps):
            q=add(p,s)
            if q not in where:
                if q not in pool:pool[q]=[[],(v,si),tie_value(run,q)]
                pool[q][0].append(v)
    for v in range(len(points)):offer(v)
    for v in range(len(points)):
        edges.extend((u,v) for u in range(v) if unit(sub(points[v],points[u])))
    all_clauses=[]
    for v in range(len(points)):all_clauses.extend(clauses_vertex(v))
    for a,b in edges:all_clauses.extend(clauses_edge(a,b))
    # Seed vertices0,1,2 form a unit triangle. Colour renaming is sound.
    all_clauses.extend([[1],[6],[11]])
    started=time.monotonic();blocked_total=0;extra_edges=0
    status='SAT';last_colour=None
    with Solver(name='cadical195',bootstrap_with=all_clauses) as solver:
        while True:
            spent=solver.accum_stats().get('conflicts',0)
            if spent>=RUN_CAP:
                status='UNKNOWN_RUN_CAP';break
            solver.conf_budget(min(CAP,RUN_CAP-spent))
            answer=solver.solve_limited()
            status='SAT' if answer is True else 'UNSAT_SIGNAL' if answer is False else 'UNKNOWN_QUERY_CAP'
            row={'n':len(points),'e':len(edges),'status':status,'stats':solver.accum_stats()}
            log.append(row)
            if status!='SAT':break
            colour=colour_model(solver,len(points));last_colour=colour
            if any(colour[a]==colour[b] for a,b in edges):raise ValueError('improper decoded model')
            if not any(colour==old for old in bank):bank.append(colour)
            bank=bank[-BANK:]
            if len(points)%64==0 or len(points)==LIMIT:
                print(json.dumps({'run':run,**row,'pool':len(pool),'bank':len(bank),'seconds':time.monotonic()-started}),flush=True)
            if len(points)==LIMIT:break
            best=None;chosen=None
            for p,(ns,parent,tie) in pool.items():
                if len(ns)<2:continue
                blocked=sum(len({c[v] for v in ns})==4 for c in bank)
                degree=len(ns);height=norm(p)[0]
                score=(blocked,degree,-height,tie) if run==0 else (degree,blocked,-height,tie) if run==1 else (blocked,degree,tie,-height) if run==2 else (degree,blocked,tie,-height)
                if best is None or score>best:best=score;chosen=p
            if chosen is None:raise ValueError('contact pool exhausted')
            ns,parent,_=pool.pop(chosen)
            actual=[v for v,p in enumerate(points) if unit(sub(p,chosen))]
            if not set(ns)<=set(actual):raise ValueError('bad translation contacts')
            extra_edges+=len(set(actual)-set(ns))
            blocked_total+=sum(len({c[v] for v in actual})==4 for c in bank)
            next_bank=[]
            for old in bank:
                free=set(range(4))-{old[v] for v in actual}
                if free:next_bank.append(old+[min(free)])
            bank=next_bank
            v=len(points);points.append(chosen);where[chosen]=v;tape.append(parent)
            new_clauses=clauses_vertex(v)
            for u in actual:
                edges.append((u,v));new_clauses.extend(clauses_edge(u,v))
            all_clauses.extend(new_clauses);solver.append_formula(new_clauses);offer(v)
        stats=solver.accum_stats()
    entry={'run':run,'status':status,'vertices':len(points),'edges':len(edges),'tape':tape,
           'colouring':None if status!='SAT' else ''.join(map(str,last_colour)),
           'queries':len(log),'conflicts':stats.get('conflicts',0),'decisions':stats.get('decisions',0),
           'blocked_bank_words':blocked_total,'extra_strict_edges':extra_edges,
           'seconds':time.monotonic()-started}
    (work/f'run{run}_log.json').write_text(json.dumps(log,indent=2)+'\n')
    (work/f'run{run}_points.json').write_text(json.dumps(points,separators=(',',':'))+'\n')
    if status!='SAT':
        (work/'signal.cnf').write_text(f'p cnf {4*len(points)} {len(all_clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in all_clauses))
    print(json.dumps({k:v for k,v in entry.items() if k not in ('tape','colouring')}),flush=True)
    return entry

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True)
    args=p.parse_args();args.work.mkdir(parents=True,exist_ok=True)
    out={'format':1,'denominator':DEN,'step_count':60,'seed_vertices':13,
         'vertex_cap':LIMIT,'trajectory_cap':4,'query_conflict_cap':CAP,
         'trajectory_conflict_cap':RUN_CAP,'bank_cap':BANK,'runs':[]}
    for r in range(4):
        out['runs'].append(run_case(r,args.work))
        (args.work/'certificate.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
        if out['runs'][-1]['status']!='SAT':break

if __name__=='__main__':main()
