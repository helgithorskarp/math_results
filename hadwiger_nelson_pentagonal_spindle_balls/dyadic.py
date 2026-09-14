"""Sixteen 451-point dyadic successors, chosen after the odd-module barrier."""
import json,argparse,time
from pathlib import Path
from itertools import product,combinations_with_replacement
import numpy as np
import model as m
from discover import prime_recipe,colour

def make_cases(canonical=False):
    rho=m.add(m.ONE,m.POW[5]);alpha=m.add(m.ONE,m.scale(m.POW[5],2));sqrt5=m.add(m.ONE,m.scale(m.add(m.POW[3],m.POW[12]),2))
    wn=m.add(m.scale(m.ONE,7),m.mul(alpha,sqrt5));require=m.require
    require(m.mul(wn,m.conj(wn))==m.scale(m.ONE,64),'dyadic phase is unit')
    rp=[m.ONE]
    for _ in range(5):rp.append(m.mul(rp[-1],rho))
    core=[(m.scale(m.ONE,8),m.Z),(m.Z,m.scale(m.ONE,8)),(wn,m.Z),(m.Z,wn)]
    out=[]
    for j,h,l in product(range(1,5),range(2),range(2)):
        u=m.mul(m.POW[3*j],wn if l else m.scale(m.ONE,8));extra=(m.Z,u) if h else (u,m.Z)
        U=[(m.mul(a,r),m.mul(b,r)) for a,b in core+[extra] for r in rp]
        require(len(U)==30 and all(m.norm3(z)==(m.scale(m.ONE,192),m.Z) for z in U),'dyadic unit inventory')
        P=([(m.Z,m.Z)]+[m.pa(a,b) for a,b in combinations_with_replacement(U,2) if a!=m.pneg(b)]) if canonical else sorted({m.pa(a,b) for a,b in combinations_with_replacement(U,2)})
        require(len(P)==len(set(P))==451,'dyadic point count')
        out.append(((j,h,l),P))
    return out
def graph(P,recipe):
    p,r,t=recipe;ev,bar=m.projection(p,r,t);inv8=pow(8,-1,p)
    A=np.array([ev(z)*inv8%p for z in P],dtype=np.int64);B=np.array([bar(z)*inv8%p for z in P],dtype=np.int64)
    edges=[];false=0
    for i in range(len(P)):
        js=np.flatnonzero(((A[i]-A[i+1:])*(B[i]-B[i+1:]))%p==1)+i+1
        for j in map(int,js):
            if m.norm3(m.ps(P[i],P[j]))==(m.scale(m.ONE,192),m.Z):edges.append((i,j))
            else:false+=1
    return edges,false
def run(work):
    start=time.time();recipe=prime_recipe();out=[]
    for key,P in make_cases():
        edges,false=graph(P,recipe);word=colour(451,edges);r={'key':key,'vertices':451,'edges':len(edges),'edge_sha256':m.digest(edges),'false_positive':false,'result':word};out.append(r);print(key,len(edges),'SAT' if len(word)==451 else word,flush=True);(work/'dyadic_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('seconds',time.time()-start)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('work',type=Path);args=ap.parse_args();run(args.work)
