"""Two exact polynomial positivity methods, each including both endpoints.

The generator uses integer Bernstein coefficients. The checker uses a
separate rational affine-substitution implementation. The arithmetic audit
uses rational centered Taylor bounds, with a complete binary cover when
its first enclosure is insufficient. None uses floating point.
"""
from fractions import Fraction as Q
from math import factorial,comb,gcd
from algebra import require

def degree(p):return max((k[0] for k in p.c),default=0)

def integer_bernstein(p,lo,hi):
    n=degree(p);M=lo.denominator*hi.denominator//gcd(lo.denominator,hi.denominator)
    A=lo.numerator*(M//lo.denominator);B=hi.numerator*(M//hi.denominator)-A
    power=[sum(v*comb(k[0],j)*A**(k[0]-j)*B**j*M**(n-k[0]) for k,v in p.c.items() if k[0]>=j) for j in range(n+1)]
    return [sum(power[k]*factorial(j)//factorial(j-k)*factorial(n-k) for k in range(j+1)) for j in range(n+1)]

def rational_bernstein(p,lo,hi):
    """Build p(lo+(hi-lo)s) by rational Horner, then change basis."""
    n=degree(p);coef=[Q(p.c.get((i,0,0),0)) for i in range(n+1)];width=hi-lo
    power=[coef[-1]]
    for x in reversed(coef[:-1]):
        nxt=[Q()]*(len(power)+1)
        for i,v in enumerate(power):nxt[i]+=lo*v;nxt[i+1]+=width*v
        nxt[0]+=x;power=nxt
    return [sum((power[k]*Q(comb(j,k),comb(n,k)) for k in range(j+1)),Q()) for j in range(n+1)]

def taylor_lower(p,lo,hi):
    """Triangle enclosure from the exact centered power coefficients."""
    mid=(lo+hi)/2;radius=(hi-lo)/2;n=degree(p)
    co=[sum((Q(v*comb(k[0],j))*mid**(k[0]-j) for k,v in p.c.items() if k[0]>=j),Q()) for j in range(n+1)]
    return co[0]-sum((abs(co[j])*radius**j for j in range(1,n+1)),Q())

def taylor_positive(p,lo,hi,max_depth=10):
    count=0;deepest=0;stack=[(lo,hi,0)]
    while stack:
        a,b,d=stack.pop();count+=1;deepest=max(deepest,d)
        if taylor_lower(p,a,b)>0:continue
        require(d<max_depth,'INCOMPLETE Taylor sign cover; no positivity certificate')
        m=(a+b)/2;stack.extend(((m,b,d+1),(a,m,d+1)))
    return count,deepest
