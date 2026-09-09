#!/usr/bin/env python3
"""Regenerate the factor cover and colour words from scratch (SymPy exact)."""
import argparse
from itertools import product
import hashlib
import json
from pathlib import Path
import time

UNITS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
DIGITS=((0,0),)+UNITS
T=((0,0),(1,0),(0,1))


def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1]
def bar(a):return a[0]+a[1],-a[1]
def add(a,b):return a[0]+b[0],a[1]+b[1]
def flatten(p):return tuple(x for c in p for x in c)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()


def inventory():
    rows=set()
    for r in product(DIGITS,repeat=5):
        first=next((x for x in r if x!=(0,0)),None)
        if first is not None:rows.add(tuple(mul(x,bar(first)) for x in r))
    if len(rows)!=2801:raise ValueError('displacement coverage')
    return sorted(rows)


def event(row):
    p=list(row)
    while p[0]==(0,0):p.pop(0)
    while p[-1]==(0,0):p.pop()
    n=len(p)-1
    if not n:return ()
    reverse=[bar(x) for x in p[::-1]]
    h=[(0,0)]*(2*n+1)
    for i,a in enumerate(p):
        for j,b in enumerate(reverse):h[i+j]=add(h[i+j],mul(a,b))
    h[n]=add(h[n],(-1,0))
    inverse=bar(h[-1])
    if mul(inverse,h[-1])!=(1,0):raise ValueError('leading unit')
    return tuple(mul(a,inverse) for a in h)


def f4mul(a,b):
    c=0
    for i in range(2):
        if b>>i&1:c^=a<<i
    if c&4:c^=7
    return c


def bad_rows(rows,spec):
    q=spec['field'];w=spec['weights'];out=set()
    for i,row in enumerate(rows):
        if q==3:c=sum(w[j]*(a-b) for j,(a,b) in enumerate(row))%3
        else:
            c=0
            for j,(a,b) in enumerate(row):c^=f4mul(w[j],(a%2)^((b%2)<<1))
        if not c:out.add(i)
    return out


def produce(progress=None):
    from sympy import QQ,Poly,sqrt,I,symbols
    z=symbols('z');K=QQ.algebraic_field(I*sqrt(3))
    rows=inventory();row_h=[event(r) for r in rows];hs=sorted(set(row_h)-{()})
    factorizations=[];all_factors=set();start=time.monotonic()
    for i,h in enumerate(hs):
        P=Poly(sum((a+b*(1+I*sqrt(3))/2)*z**j for j,(a,b) in enumerate(h)),z,domain=K)
        unit,fs=P.factor_list()
        if unit!=1:raise ValueError('nonmonic factorization')
        part=[]
        for f,e in fs:
            ff=[]
            for c in f.all_coeffs()[::-1]:
                v=K.from_sympy(c).to_list();v=[K.dom.zero]*(2-len(v))+v
                a,b=v[1]-v[0],2*v[0]
                if a.denominator!=1 or b.denominator!=1:raise ValueError('nonintegral factor')
                ff.append((int(a),int(b)))
            ff=tuple(ff);part.append((ff,e));all_factors.add(ff)
        factorizations.append(part)
        if progress and i%100==0:progress({'factorized':i,'total':len(hs),'elapsed_seconds':round(time.monotonic()-start,2)})
    factors=sorted(all_factors);ids={f:i for i,f in enumerate(factors)}
    parts=[[[ids[f],e] for f,e in part] for part in factorizations]
    parts_by_h={h:part for h,part in zip(hs,parts)}
    active=[set() for _ in factors]
    for i,h in enumerate(row_h):
        if h:
            for k,e in parts_by_h[h]:active[k].add(i)
    specs=[{'field':q,'weights':[1]+list(w)} for q in (3,4) for w in product(range(1,q),repeat=4)]
    bad=[bad_rows(rows,s) for s in specs]
    covers=[];selected=[]
    for f,A in zip(factors,active):
        if len(f)-1<=4:covers.append(-1);continue
        k=next((j for j,b in enumerate(bad) if not A&b),None)
        if k is None:raise ValueError('No linear colour cover; a physical/SAT decision is required for '+str(f))
        spec=specs[k]
        if spec not in selected:selected.append(spec)
        covers.append(selected.index(spec))
    return {'schema':'hn-radix-unit-circle-v1','event_sha256':digest([flatten(h) for h in hs]),
            'factors':[flatten(f) for f in factors], 'factorizations':parts,
            'colour_specs':selected,'factor_cover':covers}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    c=produce(lambda x:print(json.dumps(x),flush=True))
    a.out.write_text(json.dumps(c,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'certificate_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest(),'bytes':a.out.stat().st_size}))
if __name__=='__main__':main()
