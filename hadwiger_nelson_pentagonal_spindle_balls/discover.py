import json,time,argparse
from pathlib import Path
from itertools import combinations
import numpy as np
import model as m

def prime_recipe():
    p=1000000001
    # p=1 mod15 and p=3 mod4 make a primitive15th root and sqrt(-11) easy.
    while not(p%15==1 and p%4==3 and m.isprime(p) and pow(p-11,(p-1)//2,p)==1):p+=2
    for g in range(2,p):
        r=pow(g,(p-1)//15,p)
        if all(pow(r,d,p)!=1 for d in (1,3,5)):break
    beta=pow(p-11,(p+1)//4,p);t=(5+beta)*pow(6,-1,p)%p
    return p,r,t
def graph(P,work):
    p,r,t=prime_recipe();ev,bar=m.projection(p,r,t);A=np.array([ev(z) for z in P],dtype=np.int64);B=np.array([bar(z) for z in P],dtype=np.int64)
    edges=[];false=0
    for i in range(len(P)):
        js=np.flatnonzero(((A[i]-A[i+1:])*(B[i]-B[i+1:]))%p==1)+i+1
        for j in map(int,js):
            if m.unit(m.ps(P[i],P[j])):edges.append((i,j))
            else:false+=1
    out={'p':p,'root15':r,'eta':t,'vertices':len(P),'edges':len(edges),'modular_false_positives':false,'edge_sha256':m.digest(edges)}
    (work/'geometry.json').write_text(json.dumps(out,indent=2)+'\n');(work/'edges.json').write_text(json.dumps(edges)+'\n');print(out,flush=True);return edges
def colour(n,edges,k=4):
    from pysat.solvers import Solver
    clauses=[]
    for v in range(n):
        clauses.append([k*v+c+1 for c in range(k)])
        for a,b in combinations(range(k),2):clauses.append([-k*v-a-1,-k*v-b-1])
    for a,b in edges:
        for c in range(k):clauses.append([-k*a-c-1,-k*b-c-1])
    with Solver(name='cadical195',bootstrap_with=clauses) as s:
        s.conf_budget(1000000);sat=s.solve_limited()
        if sat:
            pos={x for x in s.get_model() if x>0};w=''.join(str(next(c for c in range(k) if k*v+c+1 in pos)) for v in range(n));m.require(all(w[i]!=w[j] for i,j in edges),'bad colour');return w
        return 'UNSAT' if sat is False else 'UNKNOWN'
def run(work):
    work.mkdir(parents=True,exist_ok=True);t=time.time();P,orbits,families=m.make();(work/'points.json').write_text(json.dumps(P)+'\n');(work/'families.json').write_text(json.dumps(families)+'\n');edges=graph(P,work)
    host=colour(len(P),edges);(work/'host_colour.json').write_text(json.dumps({'result':host})+'\n');print('host',host if len(host)<20 else 'SAT',flush=True)
    out=[]
    if len(host)==len(P):
        for orb,ids in families:
            take=set(ids);es=[(a,b) for a,b in edges if a in take and b in take];out.append({'orbits':orb,'vertices':len(ids),'edges':len(es),'status':'HOST_WORD'})
    else:
        for k,(orb,ids) in enumerate(families):
            take={a:i for i,a in enumerate(ids)};es=[(take[a],take[b]) for a,b in edges if a in take and b in take];word=colour(len(ids),es);out.append({'orbits':orb,'vertices':len(ids),'edges':len(es),'result':word});print(k,orb,len(es),'SAT' if len(word)==len(ids) else word,flush=True);(work/'family_results.json').write_text(json.dumps(out)+'\n')
    (work/'family_results.json').write_text(json.dumps(out)+'\n');print('seconds',time.time()-t,flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('work',type=Path);args=ap.parse_args();run(args.work)
