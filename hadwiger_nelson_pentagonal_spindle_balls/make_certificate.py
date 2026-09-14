"""Regenerate the two 16-word interface certificates; optional PySAT only here."""
import argparse,json
from pathlib import Path
from itertools import product,combinations
from pysat.solvers import Solver
import model as m
import dyadic
from discover import graph,prime_recipe

def words(P,edges,den):
    rho=m.add(m.ONE,m.POW[5]);M=[(m.Z,m.Z),(m.ONE,m.Z),(rho,m.Z),(m.add(m.ONE,rho),m.Z),(m.Z,m.ONE),(m.Z,rho),(m.Z,m.add(m.ONE,rho))]
    M=[tuple(m.scale(x,den) for x in z) for z in M];where={z:i for i,z in enumerate(P)};term=[where[z] for z in M];es=set(edges)
    me=[(i,j) for i,j in combinations(range(7),2) if tuple(sorted((term[i],term[j]))) in es]
    pats=[p for p in product(range(4),repeat=7) if p[0]==0 and all(p[i]<=max(p[:i])+1 for i in range(1,7)) and all(p[i]!=p[j] for i,j in me)]
    clauses=[]
    for i in range(len(P)):
        clauses.append([4*i+c+1 for c in range(4)])
        for c,d in combinations(range(4),2):clauses.append([-4*i-c-1,-4*i-d-1])
    for i,j in edges:
        for c in range(4):clauses.append([-4*i-c-1,-4*j-c-1])
    out=[]
    with Solver(name='cadical195',bootstrap_with=clauses) as solver:
        for pat in pats:
            solver.conf_budget(1000000);m.require(solver.solve_limited(assumptions=[4*v+c+1 for v,c in zip(term,pat)]) is True,'no positive certificate')
            pos={v for v in solver.get_model() if v>0};w=''.join(str(next(c for c in range(4) if 4*i+c+1 in pos)) for i in range(len(P)))
            m.require(all(w[i]!=w[j] for i,j in edges),'bad generated word');out.append({'pattern':pat,'word':w})
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();args.work.mkdir(parents=True,exist_ok=True)
    P,_,_=m.make();host=words(P,graph(P,args.work),1)
    _,Q=dyadic.make_cases()[0];rows=words(Q,dyadic.graph(Q,prime_recipe())[0],8)
    _,canonical=dyadic.make_cases(canonical=True)[0];where={p:i for i,p in enumerate(canonical)}
    for row in rows:
        w=['']*451
        for p,c in zip(Q,row['word']):w[where[p]]=c
        row['word']=''.join(w)
    args.output.write_text(json.dumps({'host':host,'dyadic':rows},indent=2)+'\n')
if __name__=='__main__':main()
