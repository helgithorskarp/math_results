"""Small exact Q(sqrt(33)) polynomial checker and real-root counter."""
from fractions import Fraction as F
from functools import reduce
from math import gcd,lcm

Z=(0,0)
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def minus(a,b):return a[0]-b[0],a[1]-b[1]
def times(a,b):return a[0]*b[0]+33*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def quotient(a,b):
    n=b[0]*b[0]-33*b[1]*b[1]
    if not n:raise ZeroDivisionError('zero quadratic element')
    c=times(a,(b[0],-b[1]));return F(c[0],n),F(c[1],n)
def sign(a):
    x,y=a
    if not x:return (y>0)-(y<0)
    if not y:return (x>0)-(x<0)
    if (x>0)==(y>0):return (x>0)-(x<0)
    d=x*x-33*y*y
    return ((x>0)-(x<0))*((d>0)-(d<0))
def trim(p):
    p=list(p)
    while p and p[-1]==Z:p.pop()
    return p
def primitive_positive(p):
    p=trim(p)
    if not p:return []
    d=lcm(*(F(v).denominator for c in p for v in c))
    q=[(int(a*d),int(b*d))for a,b in p]
    g=reduce(gcd,(abs(v)for c in q for v in c))
    return [(a//g,b//g)for a,b in q]
def canonical(p):
    p=primitive_positive(p)
    if not p:return ()
    a,b=p[-1];q=primitive_positive([times(c,(a,-b))for c in p])
    if q[-1][0]<0:q=[(-a,-b)for a,b in q]
    return tuple(q)
def multiply(a,b):
    if not a or not b:return []
    out=[Z]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=plus(out[i+j],times(x,y))
    return trim(out)
def division(a,b):
    a=trim(a);b=trim(b)
    if not b:raise ZeroDivisionError('zero polynomial')
    q=[Z]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        shift=len(a)-len(b);c=quotient(a[-1],b[-1]);q[shift]=c
        for j,x in enumerate(b):a[shift+j]=minus(a[shift+j],times(c,x))
        a=trim(a)
    return trim(q),a
def pgcd(a,b):
    a,b=trim(a),trim(b)
    while b:a,b=b,primitive_positive(division(a,b)[1])
    return canonical(a)
def derivative(p):return [(i*a,i*b)for i,(a,b)in enumerate(p)][1:]
def real_roots(p):
    p=trim(p)
    if len(p)<2:return 0
    seq=[p,derivative(p)]
    while seq[-1]:
        rem=division(seq[-2],seq[-1])[1]
        if not rem:break
        seq.append(primitive_positive([(-a,-b)for a,b in rem]))
    def variation(side):
        signs=[sign(q[-1])*(side**(len(q)-1))for q in seq]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variation(-1)-variation(1)
