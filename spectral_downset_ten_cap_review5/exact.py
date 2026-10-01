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
    n=len(a);require(n<=7 and all(len(row)==n for row in a),'determinant dimension')
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
    require(a and len(a)<=7 and all(len(row)==len(a) for row in a),'strict matrix dimension')
    require(all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a))),'asymmetric matrix')
    out=[determinant([row[:k] for row in a[:k]]) for k in range(1,len(a)+1)]
    require(all(x>0 for x in out),'not positive definite by Sylvester')
    return out
