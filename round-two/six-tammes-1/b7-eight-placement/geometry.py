"""Minimal exact helpers extracted unchanged from published10068 source.

Actual author six-tammes-1. Dense kernel9878 copied via10068; source pins
and the exact extraction are recorded in PINS.json. No Cramer pilot used.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from hashlib import sha256
from math import gcd
import json
from poly import add,neg,mul,divide,bernstein
R,D=[F(0),F(1)],[F(2),F(-1)]
LO,HI=F(7,10),F(3,4)
A=((0,5,11),(0,6,11),(0,5,7),(5,9,11))
B=((1,2,4),(2,4,8),(1,2,10),(1,10,12))
FACTORS=(R,D,[F(1),F(-1)],[F(1),F(1)],[F(2),F(1)],[F(-1),F(2)],[F(1),F(2)])
PARENT_SHA='a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'

def need(ok,why):
    if not ok:raise ValueError(why)

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))+'\n'

def digest(x):return sha256(canonical(x).encode()).hexdigest()

def enc(p):return [str(x) for x in p]

def vecscale(p,v):return [mul(p,x) for x in v]

def vecadd(a,b):return [add(x,y) for x,y in zip(a,b)]

def primitive(p):
    if not p:return []
    scale=1
    for a in p:scale=scale*a.denominator//gcd(scale,a.denominator)
    ns=[int(a*scale) for a in p];content=0
    for n in ns:content=gcd(content,abs(n))
    return [F(n//content) for n in ns]

def strip(p):
    for f in FACTORS:
        while p and len(p)>=len(f):
            q,r=divide(p,f)
            if r:break
            p=q
    return primitive(p)

def direct_sign(p):
    bs=bernstein(p,LO,HI)
    return 1 if all(a>0 for a in bs) else -1 if all(a<0 for a in bs) else 0

def sign(p):return direct_sign(strip(p))

def inner(v,w):
    diag=[];sv=[];sw=[]
    for x,y in zip(v,w):diag=add(diag,mul(x,y));sv=add(sv,x);sw=add(sw,y)
    return add(mul([F(2),F(-2)],diag),mul(R,mul(sv,sw)))

def flip(u,v,w):return vecadd(vecscale(R,vecadd(u,v)),vecscale([F(-1)],w))

def reconstruct(ts):
    p={1:[[F(1)],[],[]],2:[[],[F(1)],[]],4:[[],[],[F(1)]]}
    p[8]=flip(p[2],p[4],p[1]);p[10]=flip(p[1],p[2],p[4]);p[12]=flip(p[1],p[10],p[2])
    done={tuple(sorted(t)) for t in B};todo=set(map(tuple,ts))-done
    while todo:
        t=next((t for t in sorted(todo) if len(set(t)&set(p))==2),None);need(t is not None,'fresh B triangle exists')
        e=sorted(set(t)&set(p));parents=[u for u in done if set(e)<=set(u)];need(len(parents)==1,'single B parent')
        old=next(x for x in parents[0] if x not in e);fresh=next(x for x in t if x not in e)
        p[fresh]=flip(p[e[0]],p[e[1]],p[old]);done.add(t);todo.remove(t)
    need(len(p)==9 and all(inner(v,v)==D for v in p.values()),'every unit B identity')
    for t in ts:
        for i,j in combinations(t,2):need(inner(p[i],p[j])==R,'every B contact identity')
    return p

def parent():
    blob=Path(__file__).with_name('PARENT.json').read_bytes();need(sha256(blob).hexdigest()==PARENT_SHA,'entire immutable9972 certificate')
    p=json.loads(blob);need(p['A']==[list(t) for t in A] and p['B']==[list(t) for t in B],'whole prescribed A4/B4 seeds')
    need(len(p['full_band_maps'])==53 and len(p['strict_improvement_maps'])==52,'parent finite lists')
    need(all(direct_sign(f)==1 for f in FACTORS),'all fixed removed factors positive on closed band')
    return p
