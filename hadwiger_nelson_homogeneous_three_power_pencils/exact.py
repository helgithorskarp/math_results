"""Sparse Q[d,c,b,a] arithmetic and exact Eisenstein/F4 operations."""
from fractions import Fraction as Q
from itertools import product
ZERO=(0,0,0,0)
ONE={ZERO:Q(1)}


def need(ok,message):
    if not ok:
        raise ValueError(message)


def add(p,q,scale=1):
    out=dict(p)
    for m,c in q.items():
        out[m]=out.get(m,Q(0))+scale*c
        if not out[m]:
            del out[m]
    return out


def scale(k,p):
    return {m:k*c for m,c in p.items() if k*c}


def mul(p,q):
    out={}
    for m,c in p.items():
        for n,e in q.items():
            key=tuple(a+b for a,b in zip(m,n))
            out[key]=out.get(key,Q(0))+c*e
    return {m:c for m,c in out.items() if c}


def constant(k):
    return scale(Q(k),ONE)


def variable(i):
    m=tuple(int(i==j) for j in range(4))
    return {m:Q(1)}


def cmul(u,v):
    return add(mul(u[0],v[0]),mul(u[1],v[1]),-3),add(mul(u[0],v[1]),mul(u[1],v[0]))


def cadd(u,v):
    return add(u[0],v[0]),add(u[1],v[1])


def cscale(k,u):
    return scale(k,u[0]),scale(k,u[1])


def norm(u):
    return add(mul(u[0],u[0]),mul(u[1],u[1]),3)


def equations(signs):
    d,c,b,a=[variable(i) for i in range(4)]
    U=(a,b);V=(add(ONE,a,-1),scale(-1,b));W=(c,d)
    omega=(constant(Q(1,2)),constant(Q(1,2)))
    omega2=(constant(Q(-1,2)),constant(Q(1,2)))
    e,s,t,k,l=signs
    vectors=[cadd(U,W),cadd(V,cscale(e,W)),
             cadd(cadd(U,cscale(s,cmul(omega,V))),cscale(t,cmul(omega2,W))),
             cadd(cadd(U,cscale(k,cmul(omega2,V))),cscale(l,cmul(omega,W)))]
    return [add(norm(v),ONE,-1) for v in vectors],[norm(U),norm(V),norm(W)]


def decode(encoded):
    out={}
    for monomial,coefficient in encoded:
        need(len(monomial)==4 and all(type(e)==int and e>=0 for e in monomial),'monomial domain')
        m=tuple(monomial);c=Q(coefficient)
        need(m not in out and c!=0,'duplicate or zero coefficient')
        out[m]=c
    return out


def order(m):
    return sum(m),tuple(-e for e in reversed(m))


def remainder(p,basis):
    """Division only: a zero result proves ideal membership without a GB claim."""
    p=dict(p);r={}
    leading=[max(g,key=order) for g in basis]
    while p:
        m=max(p,key=order);c=p[m]
        for g,n in zip(basis,leading):
            if all(a>=b for a,b in zip(m,n)):
                shift=tuple(a-b for a,b in zip(m,n));co=c/g[n]
                p=add(p,mul({shift:co},g),-1)
                break
        else:
            r[m]=c;del p[m]
    return r


def eval_poly(p,values):
    result=Q(0)
    for m,c in p.items():
        for v,e in zip(values,m):
            c*=v**e
        result+=c
    return result


EUNITS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def emul(x,y):
    a,b=x;c,d=y
    return a*c-b*d,a*d+b*c+b*d


def econj(x):
    return x[0]+x[1],-x[1]


def enorm(x):
    a,b=x
    return a*a+a*b+b*b


def eadd(x,y):
    return x[0]+y[0],x[1]+y[1]


def canonical_row(row):
    return min(tuple(emul(u,c) for c in row) for u in EUNITS)


def gf_mul(a,b):
    out=0
    while b:
        if b&1:out^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return out


def residue(e):
    return (e[0]%2)+2*(e[1]%2)


def canonical_normal(row):
    pivot=next(v for v in row if v)
    inverse=next(x for x in (1,2,3) if gf_mul(x,pivot)==1)
    return tuple(gf_mul(x,inverse) for x in row)
