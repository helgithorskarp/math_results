#!/usr/bin/env python3
"""Discover, then exactly check, common-neighborhood union certificates.

No solver verdict is evidence. Integer primals, exact separating inequalities,
or a complete integer split with two separating inequalities authorize output.
"""
import csv
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import floor, gcd, lcm
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'ramsey_r55_coupled_signature_counts'
PINS={'CERTIFICATE.tsv':'3903b439068cd87a37fc716541a365894fd2498afdbaee8bcfa7edc3ac0916e9',
      'generate_certificate.py':'d9741c054f8c9f71b2d76fc9390748906f45c6ab90dc260fc85b867f696fef5c'}

def require(test, detail):
    if not test: raise ValueError(detail)

for name,digest in PINS.items():
    require(sha256((PRIOR/name).read_bytes()).hexdigest()==digest,name)
# Import by explicit spec to avoid a collision with this file's own name.
import importlib.util
spec=importlib.util.spec_from_file_location('old_generator',PRIOR/'generate_certificate.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

@lru_cache(None)
def upper(a,b):
    """Ramsey upper bound, including the even/even handshaking improvement."""
    if min(a,b)==1: return 1
    p,q=upper(a-1,b),upper(a,b-1)
    return p+q-int(p%2==0 and q%2==0)

def system(ds,M,mask):
    k=len(ds);adj=old.adjacency(mask,k)
    caps=old.signature_caps(adj,ds,M)
    require(caps is not None and bool(caps),'signature domain')
    xs=list(caps);bounds=list(caps.values())
    matrix=[[1]*len(xs)]+[[int(x>>i&1) for x in xs] for i in range(k)]
    target=[43-k]+[d-a.bit_count() for d,a in zip(ds,adj)]
    red=[];blue=[]
    for a in range(1<<k):
        vertices=[i for i in range(k) if a>>i&1]
        if all(adj[i]>>j&1 for i,j in combinations(vertices,2)): red.append(a)
        if all(not(adj[i]>>j&1) for i,j in combinations(vertices,2)): blue.append(a)
    roots=[];rows=[];rhs=[]
    for a in red:
        for b in blue:
            if a&b or not (a|b): continue
            t=sum(not ((a|b)>>i&1) and adj[i]&a==a and not (adj[i]&b) for i in range(k))
            roots.append((a,b))
            rows.append([int(x&a==a and not(x&b)) for x in xs])
            rhs.append(upper(5-a.bit_count(),5-b.bit_count())-1-t)
    return xs,bounds,matrix,target,roots,rows,rhs

def integer_vector(values):
    rational=[Fraction(float(v)).limit_denominator(10000) for v in values]
    scale=lcm(*(v.denominator for v in rational))
    values=[int(v*scale) for v in rational]
    divisor=gcd(*values)
    require(divisor>0,'nonzero separator')
    return [v//divisor for v in values]

def verify_separator(lam,mu,matrix,b,caps,H,u):
    require(all(type(v) is int for v in lam+mu) and all(v>=0 for v in mu),'integer separator')
    lhs=sum(v*t for v,t in zip(lam,b))
    rhs=sum(v*t for v,t in zip(mu,u))
    for j,cap in enumerate(caps):
        coefficient=sum(lam[i]*matrix[i][j] for i in range(len(b)))
        coefficient-=sum(mu[i]*H[i][j] for i in range(len(u)))
        rhs+=cap*max(0,coefficient)
    require(lhs>rhs,('exact separator failed',lhs,rhs))

def separator(matrix,b,caps,roots,H,u,extra=None):
    H=[list(row) for row in H];u=list(u)
    if extra is not None:
        H.append(extra[0]);u.append(extra[1])
    count=len(caps);dim=len(b);nr=len(u)
    A=np.array(matrix,float);C=np.array(H,float)
    # lambda*b > mu*u + sum c_X max(0,lambda*a_X-mu*h_X).
    objective=np.array([-v for v in b]+u+caps,float)
    inequalities=np.concatenate((A.T,-C.T,-np.eye(count)),axis=1)
    result=linprog(objective,A_ub=inequalities,b_ub=np.zeros(count),
                   bounds=[(-1,1)]*dim+[(0,None)]*(nr+count),
                   options={'time_limit':20})
    if not result.success or result.fun>=-1e-7: return None
    exact=integer_vector(result.x[:dim+nr]);lam,mu=exact[:dim],exact[dim:]
    verify_separator(lam,mu,matrix,b,caps,H,u)
    answer={'lambda':lam,'roots':[[a,bb,v] for (a,bb),v in zip(roots,mu) if v]}
    if extra is not None: answer['branch_weight']=mu[-1]
    return answer

def check_primal(values,denominator,matrix,b,caps,H,u):
    require(type(denominator) is int and denominator>0,'positive denominator')
    require(all(type(v) is int and 0<=v<=denominator*c for v,c in zip(values,caps)), 'primal box')
    require([sum(a*v for a,v in zip(row,values)) for row in matrix]==[denominator*t for t in b], 'primal equalities')
    require(all(sum(h*v for h,v in zip(row,values))<=denominator*t for row,t in zip(H,u)), 'primal union cuts')

def solve(ds,M,mask):
    xs,caps,A,b,roots,H,u=system(ds,M,mask)
    constraints=[LinearConstraint(A,b,b),LinearConstraint(H,-np.inf,u)]
    result=milp(np.zeros(len(xs)),integrality=np.ones(len(xs)),bounds=Bounds(0,caps),
                constraints=constraints,options={'time_limit':20})
    if result.success:
        y=[round(v) for v in result.x]
        check_primal(y,1,A,b,caps,H,u)
        return 'primal',{'values':[[x,v] for x,v in zip(xs,y) if v]}
    require(result.status==2,'incomplete MILP: '+str(result.message))
    dual=separator(A,b,caps,roots,H,u)
    if dual is not None: return 'dual',dual
    lp=linprog(np.zeros(len(xs)),A_ub=H,b_ub=u,A_eq=A,b_eq=b,
               bounds=[(0,c) for c in caps],options={'time_limit':20})
    require(lp.success,'no exact certificate and no real witness')
    fractions=[Fraction(float(v)).limit_denominator(10000) for v in lp.x]
    den=lcm(*(v.denominator for v in fractions));num=[int(v*den) for v in fractions]
    check_primal(num,den,A,b,caps,H,u)
    for j,v in enumerate(fractions):
        if v.denominator==1: continue
        low=[int(i==j) for i in range(len(xs))];cut=floor(v)
        left=separator(A,b,caps,roots,H,u,(low,cut))
        if left is None: continue
        right=separator(A,b,caps,roots,H,u,([-v for v in low],-cut-1))
        if right is not None:
            return 'split',{'signature':xs[j],'threshold':cut,'left':left,'right':right,
                            'real_primal':{'denominator':den,'values':[[x,v] for x,v in zip(xs,num) if v]}}
    raise ValueError('integer infeasibility lacks a certified one-variable split')

def main():
    with (PRIOR/'CERTIFICATE.tsv').open() as stream:
        rows=[r for r in csv.DictReader(stream,delimiter='\t') if r['kind']=='primal']
    require(len(rows)==332 and sum(int(r['orbit_size']) for r in rows)==4800,'input census')
    output=[]
    for row in rows:
        counts=list(map(int,row['counts_18_to_24'].split(',')))
        ds=[d for d,n in zip(range(18,25),counts) if d!=21 for _ in range(n)]
        kind,payload=solve(ds,int(row['M']),int(row['red_mask']))
        output.append('\t'.join([row['counts_18_to_24'],row['M'],row['red_mask'],row['orbit_size'],kind,
                                 json.dumps(payload,sort_keys=True,separators=(',',':'))]))
    print('counts_18_to_24\tM\tred_mask\torbit_size\tkind\tpayload')
    print('\n'.join(output))

if __name__=='__main__': main()
