#!/usr/bin/env python3
"""One capped exact circumcenter trajectory from Exoo-Ismailescu G79."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import numpy as np
from flint import fmpq as Q
from pysat.solvers import Solver

SQUARES=(-3,-11,-247)
ZERO=(Q(0),)*8
ONE=(Q(1),)+ZERO[1:]
TABLE=[]
for i in range(8):
    row=[]
    for j in range(8):
        c=1
        for k,v in enumerate(SQUARES):
            if i&j&(1<<k):c*=v
        row.append((i^j,c))
    TABLE.append(row)

def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def mul(x,y):
    z=[Q(0)]*8
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:
                    k,c=TABLE[i][j];z[k]+=a*b*c
    return tuple(z)
def conj(x):return tuple(-a if i.bit_count()%2 else a for i,a in enumerate(x))
def norm(x):return mul(x,conj(x))
def inv(x):
    d=x;y=ONE
    for bit in (1,2,4):
        other=tuple(-v if i&bit else v for i,v in enumerate(d))
        y=mul(y,other);d=mul(d,other)
    if not d[0] or any(d[1:]):raise ValueError('singular inverse')
    z=tuple(a/d[0] for a in y)
    if mul(x,z)!=ONE:raise ValueError('inverse identity failed')
    return z
def numeric(z):
    a,b,c,d,e,f,g,h=(float(q.p)/float(q.q) for q in z)
    return complex(a-d*np.sqrt(33)-f*np.sqrt(741)-g*np.sqrt(2717),
                   b*np.sqrt(3)+c*np.sqrt(11)+e*np.sqrt(247)-h*np.sqrt(8151))

def source(seedfile):
    raw=json.loads(seedfile.read_text())
    base=[tuple(Q(v,36) for v in (c,-a,-b,-d,0,0,0,0)) for a,b,c,d in raw]
    rho=(Q(119,128),Q(0),Q(0),Q(0),Q(3,128),Q(0),Q(0),Q(0))
    if norm(rho)!=ONE:raise ValueError('nonunit source rotation')
    pts=base+[mul(rho,v) for v in base[1:]]
    if len(pts)!=79 or len(set(pts))!=79:raise ValueError('wrong seed cardinality')
    edges=[];aux=[]
    for i,j in combinations(range(79),2):
        n=norm(sub(pts[i],pts[j]))
        if n==ONE:edges.append((i,j))
        if n==(Q(11,3),)+ZERO[1:]:aux.append((i,j))
    if len(edges)!=165 or len(aux)!=118:raise ValueError('source transcription mismatch')
    return pts,edges,aux

def circumcenter(a,b,c):
    u=sub(b,a);v=sub(c,a)
    det=sub(mul(conj(u),v),mul(conj(v),u))
    if det==ZERO:raise ValueError('collinear triple')
    z=add(a,mul(sub(mul(norm(u),v),mul(norm(v),u)),inv(det)))
    if any(norm(sub(z,p))!=ONE for p in (a,b,c)):raise ValueError('not a unit-radius triple')
    return z

def key(z):return (round(z.real*1e8),round(z.imag*1e8))

class Proposals:
    """Numerical discovery only. Accepted points are reconstructed exactly."""
    def __init__(self,coords):
        self.pool={};self.selected=set();self.rejected=0
        self.coords=[]
        for z in coords:self.insert(z)
    def insert(self,z):
        idx=len(self.coords);self.coords.append(z);self.selected.add(key(z));self.pool.pop(key(z),None)
        if self.pool:
            keys=list(self.pool);zs=np.array([self.pool[k][0] for k in keys])
            hits=np.flatnonzero(np.abs(np.abs(zs-z)**2-1)<1e-7)
            for k in hits:self.pool[keys[int(k)]][1].add(idx)
        if idx==0:return
        old=np.array(self.coords[:-1]);d=z-old;d2=np.abs(d)**2
        good=np.flatnonzero((d2>1e-16)&(d2<=4))
        if len(good)==0:return
        factor=np.sqrt(np.maximum(0,1/d2[good]-.25))
        mid=(z+old[good])/2;offset=1j*d[good]*factor
        allnew=np.concatenate((mid+offset,mid-offset))
        fresh={}
        for q in allnew:
            k=key(q)
            if k not in self.selected and k not in self.pool:fresh[k]=complex(q)
        if not fresh:return
        keys=list(fresh);qs=np.array([fresh[k] for k in keys]);coords=np.array(self.coords)
        # Numeric tolerances propose contacts; never certify them.
        contacts=np.abs(np.abs(qs[:,None]-coords[None,:])**2-1)<1e-7
        for k,q,row in zip(keys,qs,contacts):self.pool[k]=[complex(q),set(map(int,np.flatnonzero(row)))]
    def choose(self,colours,exact):
        while True:
            ranked=[]
            for k,(q,ns) in self.pool.items():
                if len(ns)>=3:
                    score=(len({colours[i] for i in ns}),len(ns),-abs(q)**2,-k[0],-k[1])
                    ranked.append((score,k))
            if not ranked:return None
            _,k=max(ranked);q,ns=self.pool.pop(k)
            for triple in combinations(sorted(ns),3):
                try:z=circumcenter(*(exact[i] for i in triple))
                except ValueError:continue
                if z in set(exact):break
                if abs(numeric(z)-q)>1e-6:continue
                actual=[i for i,p in enumerate(exact) if norm(sub(z,p))==ONE]
                if len(actual)<3:raise ValueError('lost construction contacts')
                return z,triple,actual
            self.rejected+=1

def vclauses(v):
    xs=[4*v+c+1 for c in range(4)]
    return [xs]+[[-xs[a],-xs[b]] for a,b in combinations(range(4),2)]
def eclauses(a,b):return [[-4*a-c-1,-4*b-c-1] for c in range(4)]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--seed',type=Path,default=Path(__file__).with_name('seed40.json'))
    args=p.parse_args();args.work.mkdir(parents=True,exist_ok=True)
    pts,edges,aux=source(args.seed);pool=Proposals(list(map(numeric,pts)));tape=[];logs=[]
    clauses=[]
    for v in range(79):clauses.extend(vclauses(v))
    for a,b in edges:clauses.extend(eclauses(a,b))
    clauses.append([1]) # One vertex fixed by colour permutation only.
    started=time.monotonic();blocked=0;reason=None;word=None
    with Solver(name='cadical195',bootstrap_with=clauses) as solver:
        while True:
            used=solver.accum_stats().get('conflicts',0)
            if used>=500000:status='UNKNOWN';reason='trajectory conflict cap';break
            solver.conf_budget(min(100000,500000-used));answer=solver.solve_limited()
            status='SAT' if answer is True else 'UNSAT_SIGNAL' if answer is False else 'UNKNOWN'
            logs.append({'vertices':len(pts),'edges':len(edges),'status':status,'stats':solver.accum_stats()})
            if answer is not True:reason='solver result';break
            model=set(x for x in solver.get_model() if x>0);cols=[]
            for v in range(len(pts)):
                opts=[c for c in range(4) if 4*v+c+1 in model]
                if len(opts)!=1:raise ValueError('non-one-hot model')
                cols.append(opts[0])
            if any(cols[a]==cols[b] for a,b in edges):raise ValueError('bad SAT word')
            word=''.join(map(str,cols))
            if len(pts)%25==0 or len(pts) in (79,508):
                print(json.dumps({'n':len(pts),'e':len(edges),'queries':len(logs),'conflicts':solver.accum_stats()['conflicts'],'pool':len(pool.pool),'seconds':time.monotonic()-started}),flush=True)
            if len(pts)==508:reason='vertex cap';break
            proposal=pool.choose(cols,pts)
            if proposal is None:reason='three-contact proposals exhausted';break
            z,triple,actual=proposal;blocked+=len({cols[v] for v in actual})==4
            index=len(pts);pts.append(z);tape.append(list(triple))
            new=vclauses(index)
            for v in actual:edges.append((v,index));new.extend(eclauses(v,index))
            clauses.extend(new);solver.append_formula(new);pool.insert(numeric(z))
        stats=solver.accum_stats()
    out={'format':1,'source':'EI2018-G79','trajectory_cap':1,'vertex_cap':508,'query_conflict_cap':100000,'trajectory_conflict_cap':500000,'vertices':len(pts),'edges':len(edges),'seed_auxiliary_pairs':len(aux),'status':status,'exit_reason':reason,'queries':len(logs),'stats':stats,'tape':tape,'colouring':word if status=='SAT' else None,'blocked_previous_words':blocked,'rejected_numerical_proposals':pool.rejected,'seconds':time.monotonic()-started}
    (args.work/'certificate.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
    (args.work/'points.json').write_text(json.dumps([[str(c) for c in z] for z in pts],separators=(',',':'))+'\n')
    (args.work/'log.json').write_text(json.dumps(logs,indent=2)+'\n')
    if status!='SAT':
        (args.work/'query.cnf').write_text(f'p cnf {4*len(pts)} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    print(json.dumps({k:v for k,v in out.items() if k not in ('tape','colouring')}),flush=True)

if __name__=='__main__':main()
