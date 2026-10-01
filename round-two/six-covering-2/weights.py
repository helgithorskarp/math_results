"""One-thread discovery of exact integer residual-capacity certificates. Solver status alone proves nothing."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse
from collections import Counter
from itertools import combinations
import json
from math import gcd,lcm
from pathlib import Path
from time import monotonic
import warnings
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from orbits import orbit_data,quotient_rows,boxes_from_weights,divisors

def populations(W,m):
    out=[0]*m
    for x,w in enumerate(W):
        if w: out[x%m]+=int(w)
    return out

def pair_cap(W,m,n):
    left=populations(W,m);right=populations(W,n);ell=lcm(m,n)
    meet=populations(W,ell);g=gcd(m,n);q=n//g;inverse=pow(m//g,-1,q)
    return max(left[a]+right[b]-(meet[(a+m*((b-a)//g*inverse%q))%ell] if (b-a)%g==0 else 0)
               for a in range(m) for b in range(n))

def fractional_pairs(W,B,k=14):
    active=B[:k]
    single={m:max(populations(W,m)) for m in active}
    edges=[];savings=[]
    for m,n in combinations(active,2):
        s=single[m]+single[n]-pair_cap(W,m,n)
        if s>0:edges.append((m,n));savings.append(s)
    if not edges:return []
    index={m:i for i,m in enumerate(active)}
    rr=[];cc=[]
    for j,(m,n) in enumerate(edges):rr.extend((index[m],index[n]));cc.extend((j,j))
    mat=coo_matrix(([1]*len(rr),(rr,cc)),shape=(len(active),len(edges))).tocsr()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',message='Unrecognized options detected')
        r=linprog(-np.array(savings,dtype=float),A_ub=mat,b_ub=np.ones(len(active)),
                  bounds=(0,1),method='highs',options={'threads':1,'time_limit':1})
    if r.x is None:return []
    vals=[int(round(2*v)) for v in r.x]
    if any(v not in (0,1,2) or abs(v/2-t)>1e-6 for v,t in zip(vals,r.x)):return []
    degree=Counter()
    for edge,v in zip(edges,vals):
        for m in edge:degree[m]+=v
    if max(degree.values(),default=0)>2:return []
    return [(edge,v) for edge,v in zip(edges,vals) if v]

def solve(L,A,triangle=None,limit=2,pair_weights=None):
    B=[m for m in divisors(L) if m>=8 and m not in dict(A)]
    orbits,rows=quotient_rows(L,A,B);width=len(orbits)
    if pair_weights:
        degree=Counter()
        for edge,coef in pair_weights:
            if len(edge)!=2 or coef not in (1,2) or any(m not in B for m in edge):raise ValueError('Invalid fractional pair proposal')
            for m in edge:degree[m]+=coef
        if max(degree.values(),default=0)>2:raise ValueError('Overcharged resource')
        groups=[((m,),(2-degree[m])/2) for m in B if degree[m]<2]+[(tuple(edge),coef/2) for edge,coef in pair_weights]
    elif triangle:
        tr=set(triangle)
        groups=[((m,),1) for m in B if m not in tr]+[(e,0.5) for e in combinations(sorted(tr),2)]
    else:groups=[((m,),1) for m in B]
    rr=[];cc=[];vv=[];nr=0
    singleton={m:[] for m in B}
    for m,key,row in rows:singleton[m].append(tuple(sorted(row.items())))
    pairpops={}
    def pops(m):
        if m not in pairpops:
            vals=[Counter() for _ in range(m)]
            for j,O in enumerate(orbits):
                for x in O:vals[x%m][j]+=1
            pairpops[m]=vals
        return pairpops[m]
    for gi,(group,mult) in enumerate(groups):
        if len(group)==1: vectors=singleton[group[0]]
        else:
            m,n=group;g=gcd(m,n);ell=lcm(m,n);q=n//g;inverse=pow(m//g,-1,q)
            lm=pops(m);ln=pops(n);li=pops(ell);vectors=set()
            for a in range(m):
                for b in range(n):
                    v=lm[a]+ln[b]
                    if (b-a)%g==0:
                        v.subtract(li[(a+m*((b-a)//g*inverse%q))%ell])
                    vectors.add(tuple(sorted((j,val) for j,val in v.items() if val)))
        for v in sorted(vectors):
            for j,val in v:rr.append(nr);cc.append(j);vv.append(val)
            rr.append(nr);cc.append(width+gi);vv.append(-1);nr+=1
    mat=coo_matrix((vv,(rr,cc)),shape=(nr,width+len(groups))).tocsr()
    eq=coo_matrix(([len(O) for O in orbits],([0]*width,list(range(width)))),shape=(1,width+len(groups))).tocsr()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',message='Unrecognized options detected')
        r=linprog(np.r_[np.zeros(width),[mult for group,mult in groups]],A_ub=mat,b_ub=np.zeros(nr),
                  A_eq=eq,b_eq=[1],bounds=(0,None),method='highs',options={'threads':1,'time_limit':limit})
    info={'prefix':A,'triangle':triangle,'pair_weights':pair_weights,'orbits':width,'rows':nr,'status':r.status,'objective':r.fun}
    if r.x is None:return info,None
    best=None
    for scale in (10000,100000,1000000):
        values=[max(0,int(round(float(v)*scale))) for v in r.x[:width]]
        W=[0]*L
        for O,w in zip(orbits,values):
            for x in O:W[x]=w
        single={m:max(populations(W,m)) for m in B}
        cap2=sum(int(2*mult)*(single[group[0]] if len(group)==1 else pair_cap(W,*group)) for group,mult in groups)
        gap2=2*sum(W)-cap2
        best=(gap2,W,single)
        if gap2>0:break
    gap2,W,single=best
    common=gcd(*[v for v in W if v])
    if common>1:W=[v//common for v in W];single={m:v//common for m,v in single.items()};gap2//=common
    info.update({'gap2':gap2,'single_gap':sum(W)-sum(single.values()),'demand':sum(W)})
    weights={x:w for x,w in enumerate(W) if w}
    if triangle:pair_weights=[(e,1) for e in combinations(sorted(triangle),2)]
    payload={'L':L,'minimum':8,'anchors':A,'pairs2':pair_weights or [],'boxes':boxes_from_weights(L,A,weights),'gap2':gap2}
    return info,(W,payload)
