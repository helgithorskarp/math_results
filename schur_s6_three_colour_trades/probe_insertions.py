"""Constructive trades with exact admissible insertions into fixed classes.

UNSAT/UNKNOWN are exploratory solver observations. A SAT model is accepted
only after direct checking of the complete 537-entry colouring.
"""
import argparse
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import time

from pysat.solvers import Solver


def check(c):
    return [(x,z-x,z,c[z]) for z in range(2,len(c))
            for x in range(1,z//2+1) if c[x]==c[z-x]==c[z] and c[z]!=0]


def insertion_sets(c, n=537):
    """Exact single-insertion test for each initially sum-free colour class."""
    out={}
    for d in range(1,7):
        A={v for v in range(1,len(c)) if c[v]==d}
        if any(x+y in A for x in A for y in A):
            out[d]=None
            continue
        blocked={x+y for x in A for y in A}
        blocked.update(abs(x-y) for x in A for y in A)
        blocked.update(x//2 for x in A if x%2==0)
        out[d]=set(range(1,n+1))-A-blocked
    return out


def domains_for(c,palette,extra,n=537):
    if len(c)==n:c=c+[0]
    if len(c)!=n+1:raise ValueError('wrong input length')
    ports=insertion_sets(c,n)
    if not set(extra).isdisjoint(palette):raise ValueError('overlapping labels')
    if any(ports[d] is None for d in extra):raise ValueError('defective fixed class')
    free={v for v in range(1,n+1) if c[v] in palette or c[v]==0}
    domains=[set()]+[{c[v]} for v in range(1,n+1)]
    for v in free:
        domains[v]=set(palette)|{d for d in extra if v in ports[d]}
    return c,domains,free,ports


def solve(c,palette,extra,budget=100000,seed_phases=False,n=537,force_split=False):
    start=time.monotonic()
    c,D,free,ports=domains_for(c,palette,extra,n)
    if any(col not in palette for x,y,z,col in check(c)):
        return {'status':'invalid_outside'}
    variables={};clauses=[]
    for v in sorted(free):
        for d in sorted(D[v]):variables[v,d]=len(variables)+1
        clauses.append([variables[v,d] for d in sorted(D[v])])
        for a,b in combinations(sorted(D[v]),2):
            clauses.append([-variables[v,a],-variables[v,b]])
    edge_count=0
    for z in range(2,n+1):
        for x in range(1,z//2+1):
            E=sorted({x,z-x,z})
            common=set.intersection(*(D[v] for v in E))
            if not common:continue
            edge_count+=1
            for d in sorted(common):
                clauses.append([-variables[v,d] for v in E if v in free])
    # The free palette labels remain globally interchangeable. Fix a
    # vertex with precisely those choices; no extra label is then excluded.
    anchor=next((v for v in sorted(free) if D[v]==set(palette)),None)
    if anchor is not None:clauses.append([variables[anchor,palette[0]]])
    if force_split:
        if n!=537 or len(palette)!=4:raise ValueError('splitting constraint requires the certified four-class family')
        for old in palette:
            A=[v for v in sorted(free) if c[v]==old]
            for d in sorted(set.intersection(*(D[v] for v in A))):
                clauses.append([-variables[v,d] for v in A])
    with Solver(name='cadical195',bootstrap_with=clauses) as solver:
        if seed_phases:
            rename={d:d for d in range(1,7)}
            if anchor is not None and c[anchor] in palette:
                old=c[anchor];new=palette[0]
                rename[old],rename[new]=new,old
            phase={v:rename.get(c[v],palette[0]) for v in free}
            solver.set_phases([var if phase[v]==d else -var for (v,d),var in variables.items()])
        solver.conf_budget(budget)
        answer=solver.solve_limited()
        result={'status':{True:'SAT',False:'UNSAT',None:'UNKNOWN'}[answer],
                'palette':list(palette),'extra':list(extra),'vertices':len(free),
                'ports':{str(d):sorted(ports[d]&free) for d in extra},
                'variables':len(variables),'clauses':len(clauses),
                'anchor':anchor,'force_split':force_split,'seconds':time.monotonic()-start,'stats':solver.accum_stats()}
        if answer:
            model=set(solver.get_model());new=c.copy()
            for v in free:
                choices=[d for d in D[v] if variables[v,d] in model]
                if len(choices)!=1:raise RuntimeError('bad one-hot decode')
                new[v]=choices[0]
            if set(new[1:])-set(range(1,7)) or check(new):
                raise RuntimeError('invalid SAT colouring')
            result['colouring']=''.join(map(str,new[1:]))
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--inputs',nargs='+',default=['baseline','near537','team_near_190','team_near_359'])
    p.add_argument('--budget',type=int,default=100000)
    p.add_argument('--size',type=int,default=3)
    p.add_argument('--mode',choices=['single','all'],default='single')
    p.add_argument('--output',required=True)
    p.add_argument('--seed-phases',action='store_true')
    p.add_argument('--force-split',action='store_true')
    a=p.parse_args()
    pub=Path(__file__).resolve().parent
    fixtures=json.loads((pub/'fixtures.json').read_text())
    cert=json.loads((pub/'certificate.json').read_text())['cases']
    proofs={(r['input'],tuple(r['palette'])):set(r['vertices']) for r in cert}
    results=[]
    for name in a.inputs:
        c=[0]+list(map(int,fixtures[name]['colours']))
        badcols={row[3] for row in check(c)}
        ports=insertion_sets(c)
        print(name,'port counts',{d:len(P) if P is not None else None for d,P in ports.items()},flush=True)
        for T in combinations(range(1,7),a.size):
            if not badcols<=set(T):continue
            extras=[(d,) for d in range(1,7) if d not in T] if a.mode=='single' else [tuple(d for d in range(1,7) if d not in T)]
            for E in extras:
                available=set().union(*(ports[d] for d in E))
                W=proofs.get((name,T))
                if W is not None and not W & available:
                    result={'status':'excluded_by_existing_witness','palette':list(T),'extra':list(E)}
                else:result=solve(c,T,E,a.budget,a.seed_phases,force_split=a.force_split)
                result['input']=name
                results.append(result)
                print(name,T,E,result['status'],round(result.get('seconds',0),3),flush=True)
                Path(a.output).write_text(json.dumps(results,indent=2)+'\n')
                if result['status']=='SAT':
                    Path(a.output).with_suffix('.colouring.txt').write_text(result['colouring']+'\n')
                    raise SystemExit(0)


if __name__=='__main__':main()
