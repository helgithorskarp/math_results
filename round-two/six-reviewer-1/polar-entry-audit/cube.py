"""Credited OWN Laurent/cube arithmetic ONLY from source74977ee1,
owned_centered.py (original OWN785f5208). No identities or budgets imported.
"""
from fractions import Fraction as Q
def need(x,msg):
    if not x: raise ValueError(msg)

def clean(p): return {k:v for k,v in p.items() if v}
def add(*ps):
    d={}
    for p in ps:
        for k,v in p.items():d[k]=d.get(k,Q(0))+v
    return clean(d)
def sc(p,x): return clean({k:v*x for k,v in p.items()})
def cn(x): return {(0,()):Q(x)} if x else {}
def tok(v,n=1): return {(0,((v,n),)):Q(1)} if n else cn(1)
def phase(n):
    n%=3
    return {(n,()):Q(1)} if n<2 else {(0,()):Q(-1),(1,()):Q(-1)}
def mul(p,q):
    out={}
    for (a,ka),x in p.items():
        for (b,kb),y in q.items():
            k=dict(ka)
            for v,n in kb:k[v]=k.get(v,0)+n
            k=tuple(sorted((v,n) for v,n in k.items() if n))
            for (c,_),z in phase(a+b).items():out[(c,k)]=out.get((c,k),Q(0))+x*y*z
    return clean(out)
def prod(ps):
    o=cn(1)
    for p in ps:o=mul(o,p)
    return o
def pw(p,n):return prod([p]*n)
REAL={'a','eta','V','Q','J','R2','E','g','tail','M2','b','c','F'}
def barname(v):return v if v in REAL else v[4:] if v.startswith('bar_') else 'bar_'+v
def cj(p):
    out={}
    for (a,k),x in p.items():out=add(out,sc(mul(phase(-a),{(0,tuple(sorted((barname(v),n) for v,n in k))):Q(1)}),x))
    return out
def re(p):return sc(add(p,cj(p)),Q(1,2))
def sub(p,mapping):
    out={}
    for (a,k),x in p.items():
        t=sc(phase(a),x)
        for v,n in k:
            if v in mapping:
                need(n>=0,'negative substitution power')
                t=mul(t,pw(mapping[v],n))
            else:t=mul(t,tok(v,n))
        out=add(out,t)
    return out
def pack(p):return [[a,[[v,n] for v,n in k],str(x)] for (a,k),x in sorted(p.items())]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

