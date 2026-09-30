"""Weighted-mean reduction in Q[t,c,x,Q][L]/(L^2-Q*g).

L is the signed phase parameter, g=(1-c^2)(1-x^2), b=t*(c*x+L).
The two complete substitution algorithms are binomial reduction and Horner
evaluation in the quadratic extension. Python integers/Fraction only.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb

ZERO=(0,0,0,0)
ONE={ZERO:F(1)}

def add(*items):
    out=defaultdict(F)
    for p in items:
        for e,k in p.items():out[e]+=k
    return {e:k for e,k in out.items() if k}

def scale(p,v):return {e:k*v for e,k in p.items() if k*v}

def mul(p,q):
    out=defaultdict(F)
    for e,k in p.items():
        for f,v in q.items():out[tuple(a+b for a,b in zip(e,f))]+=k*v
    return {e:k for e,k in out.items() if k}

def power(p,n):
    out=ONE
    while n:
        if n&1:out=mul(out,p)
        n//=2
        if n:p=mul(p,p)
    return out

def variable(i):
    e=list(ZERO);e[i]=1
    return {tuple(e):F(1)}

def evaluate(p,values):
    out=F(0)
    for e,k in p.items():
        for i in range(4):k*=values[i]**e[i]
        out+=k
    return out

def binomial_reduce(delta,skew):
    """Set m=1; substitute b=t*(c*x+L); reduce every L power."""
    even=defaultdict(F);odd=defaultdict(F)
    for source,p in enumerate([delta,skew]):
        for e,v in p.items():
            n,c,x,q=e[0],e[2],e[3],e[4]
            # Every m exponent contributes its coefficient at m=1.
            for k in range(n+1):
                ell=k+source;h=ell//2
                target=odd if ell%2 else even
                for i in range(h+1):
                    for j in range(h+1):
                        exponent=(n,c+n-k+2*i,x+n-k+2*j,q+h)
                        target[exponent]+=v*comb(n,k)*comb(h,i)*comb(h,j)*(-1)**(i+j)
    return ({e:v for e,v in even.items() if v},
            {e:v for e,v in odd.items() if v})

def horner_reduce(delta,skew):
    """Different algorithm: Horner arithmetic in the quadratic extension."""
    t,c,x,q=[variable(i) for i in range(4)]
    g=mul(add(ONE,scale(power(c,2),-1)),add(ONE,scale(power(x,2),-1)))
    relation=mul(q,g)
    b0=mul(t,mul(c,x));b1=t
    def one_polynomial(p):
        n=max(e[0] for e in p);groups=[defaultdict(F) for _ in range(n+1)]
        for e,k in p.items():groups[e[0]][(0,e[2],e[3],e[4])]+=k
        a={};b={}
        for group in reversed(groups):
            a,b=(add(mul(a,b0),mul(relation,mul(b,b1)),group),
                 add(mul(a,b1),mul(b,b0)))
        return a,b
    d0,d1=one_polynomial(delta);j0,j1=one_polynomial(skew)
    return add(d0,mul(relation,j1)),add(d1,j0)

def q_unit(p):
    """Q=q/4, for the full signed-kernel certificate."""
    return {e:k*F(1,4)**e[3] for e,k in p.items()}

def envelope(even,odd):
    """Second Newton upper bound for sqrt(g), eta=z/2, Q=z^2/4."""
    p={(e[0],e[1],e[2],2*e[3]):k*F(1,4)**e[3] for e,k in even.items()}
    r={(e[0],e[1],e[2],2*e[3]+1):k*F(1,2)*F(1,4)**e[3] for e,k in odd.items()}
    c,x=variable(1),variable(2)
    s=add(ONE,scale(mul(c,x),-1))
    g=mul(add(ONE,scale(power(c,2),-1)),add(ONE,scale(power(x,2),-1)))
    den=scale(mul(s,add(power(s,2),g)),4)
    num=add(power(s,4),scale(mul(power(s,2),g),6),power(g,2))
    return add(mul(den,p),mul(num,r))

def canonical(p):return [[list(e),str(k)] for e,k in sorted(p.items())]
