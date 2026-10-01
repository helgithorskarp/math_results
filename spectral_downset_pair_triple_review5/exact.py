"""Reviewer-owned determinant and adjugate arithmetic; no author import."""
from fractions import Fraction as F
from itertools import permutations
from math import gcd,lcm
import json

def require(test,message):
    if not test:raise ValueError(message)

def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def determinant(a):
    n=len(a);require(n<=6 and all(len(row)==n for row in a),'determinant dimension')
    if not n:return F(1)
    require(all(type(x)is int or isinstance(x,F) for row in a for x in row),'inexact determinant input')
    scale=lcm(*(F(x).denominator for row in a for x in row))
    z=[[int(F(x)*scale) for x in row] for row in a];total=0
    for p in permutations(range(n)):
        value=1
        for i,j in enumerate(p):value*=z[i][j]
        if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2:value=-value
        total+=value
    return F(total,scale**n)

def inverse(a):
    n=len(a);require(n>0,'empty inverse');d=determinant(a);require(d,'singular inverse')
    result=[[(-1)**(i+j)*determinant([[a[r][c] for c in range(n) if c!=i]
                   for r in range(n) if r!=j])/d for j in range(n)] for i in range(n)]
    require(all(sum(a[i][k]*result[k][j] for k in range(n))==int(i==j)
                for i in range(n) for j in range(n)),'adjugate residual')
    return result

def leading(a):
    require(a and len(a)<=6 and all(len(row)==len(a) for row in a),'strict matrix dimension')
    require(all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a))),'asymmetric matrix')
    out=[determinant([row[:k] for row in a[:k]]) for k in range(1,len(a)+1)]
    require(all(x>0 for x in out),'not positive definite by Sylvester')
    return out

def polynomial(base,slope):
    n=len(base);require(2<=n<=6 and len(slope)==n and all(len(row)==n for row in base+slope),'Schur dimension')
    require(all(not slope[i][j] for i in range(1,n) for j in range(1,n)),'moving remainder')
    B=[row[1:] for row in base[1:]];minors=leading(B);inv=inverse(B)
    a0=base[0][0];a1=slope[0][0];v0=base[0][1:];v1=slope[0][1:]
    bilinear=lambda a,b:sum(a[i]*inv[i][j]*b[j] for i in range(n-1) for j in range(n-1))
    c=(a0-bilinear(v0,v0),a1-2*bilinear(v0,v1),-bilinear(v1,v1))
    scale=lcm(*(x.denominator for x in c));integers=[int(x*scale) for x in c]
    divisor=gcd(*integers);require(divisor>0,'zero polynomial')
    integers=[x//divisor for x in integers]
    return dict(coefficients_ascending=integers,positive_scale=str(F(divisor,scale)),
                remainder_leading_minors=list(map(str,minors)))

def value(coefficients,x):return sum(F(c)*x**i for i,c in enumerate(coefficients))
