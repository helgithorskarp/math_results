"""Fresh sparse polynomial over field.E. Six variables J3,J4,G,sigma,M,b."""
from field import E,Q,need

ZERO=(0,)*6


def const(v):
    v=E(v)
    return {ZERO:v}if v else {}


def var(j):
    e=[0]*6;e[j]=1
    return {tuple(e):E(1)}


def add(*polys):
    out={}
    for p in polys:
        for k,v in p.items():
            out[k]=out.get(k,E(0))+v
    return {k:v for k,v in out.items()if v}


def scale(p,a):
    a=E(a)
    return {k:v*a for k,v in p.items()if v*a}


def mul(a,b):
    out={}
    for k,v in a.items():
        for l,w in b.items():
            m=tuple(x+y for x,y in zip(k,l))
            out[m]=out.get(m,E(0))+v*w
    return {k:v for k,v in out.items()if v}


def power(p,n):
    out=const(1)
    for _ in range(n):out=mul(out,p)
    return out


def sub(a,b):
    return add(a,scale(b,-1))


def conj(p):
    return {k:v.conjugate()for k,v in p.items()}


def real(p):
    return scale(add(p,conj(p)),Q(1,2))


def derivative(p,j):
    out={}
    for k,v in p.items():
        if k[j]:
            n=list(k);n[j]-=1;out[tuple(n)]=v*k[j]
    return out


def substitute(p,values):
    out={}
    for k,v in p.items():
        term=const(v)
        for j,n in enumerate(k):
            if n:term=mul(term,power(values.get(j,var(j)),n))
        out=add(out,term)
    return out


def evaluate(p,values):
    out=E(0)
    for k,v in p.items():
        for x,n in zip(values,k):
            if n:v=v*E(x)**n
        out=out+v
    return out


def record(p):
    return [[list(k),v.record()]for k,v in sorted(p.items())]


def same(a,b,message):
    need(a==b,message)
