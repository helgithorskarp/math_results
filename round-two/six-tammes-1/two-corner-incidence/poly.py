"""Exact rational polynomial arithmetic. six-tammes-1, researcher."""
from fractions import Fraction as Q
from math import comb

def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return p
def add(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,v in enumerate(a):c[i]+=v
    for i,v in enumerate(b):c[i]+=v
    return trim(c)
def scale(a,c):return trim([v*c for v in a])
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    c=[Q(0)]*max(0,len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def divrem(a,b):
    a=trim(a);b=trim(b)
    if not b:raise ValueError('zero divisor')
    c=[Q(0)]*max(0,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        k=len(a)-len(b);v=a[-1]/b[-1];c[k]+=v
        a=sub(a,[Q(0)]*k+scale(b,v))
    return trim(c),a
def gcd(a,b):
    while b:_,c=divrem(a,b);a,b=b,c
    return scale(a,1/a[-1]) if a else []
def bernstein(p,lo,hi):
    n=len(p)-1;power=[Q(0)]*(n+1)
    for i,x in enumerate(p):
        for j in range(i+1):power[j]+=x*comb(i,j)*lo**(i-j)*(hi-lo)**j
    return [sum((power[j]*Q(comb(k,j),comb(n,j)) for j in range(k+1)),Q(0)) for k in range(n+1)]
