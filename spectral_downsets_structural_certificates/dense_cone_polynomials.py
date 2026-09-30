#!/usr/bin/env python3
"""Exact coefficient certificate in Z[A,B,X] for the dense-cone 3-block.

A=h-d-2 >=0, B=2d-h >=0, X=h-d-2-lambda in [0,h-2].
No interpolation, floating arithmetic, CAS or graph input is used here.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
import json


def constant(v):
    return {(0,0,0):v} if v else {}


def var(i):
    return {tuple(int(j==i) for j in range(3)):1}


def add(*xs):
    out=defaultdict(int)
    for x in xs:
        for p,v in x.items():out[p]+=v
    return {p:v for p,v in out.items() if v}


def scale(v,x):
    return {p:v*a for p,a in x.items() if v*a}


def mul(*xs):
    out=constant(1)
    for x in xs:
        nxt=defaultdict(int)
        for p,a in out.items():
            for q,b in x.items():nxt[tuple(i+j for i,j in zip(p,q))]+=a*b
        out={p:v for p,v in nxt.items() if v}
    return out


def determinant3(matrix):
    terms=[]
    for p in permutations(range(3)):
        sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        terms.append(scale(sign,mul(*(matrix[i][p[i]] for i in range(3)))))
    return add(*terms)


def determinant_polynomial():
    A,B,X=[var(i) for i in range(3)]
    a=add(A,constant(2));d=add(a,B);h=add(a,d)
    hm2=add(h,constant(-2));hm4=add(h,constant(-4))
    lam=add(A,scale(-1,X));g=add(hm2,scale(-1,X))
    E=add(mul(d,hm4),constant(2))
    e=add(mul(E,add(constant(4),X)),mul(scale(2,B),add(constant(1),scale(-1,g))))
    c=add(mul(h,d),scale(-1,mul(a,lam)))
    b=add(scale(-1,d),scale(2,lam));k=add(mul(d,h),constant(-2));top=add(h,constant(1))
    second=add(mul(top,c,d),scale(-1,mul(b,b)))
    correction=add(mul(top,d,d,d,hm2,hm2),mul(c,k,k),scale(-2,mul(b,k,d,hm2)))
    P=add(mul(d,hm2,hm2,second,e),scale(-1,mul(g,E,correction)))

    # Independently expand the six Leibniz terms of the cleared rational
    # Gram matrix, rather than trusting the hand-derived determinant formula.
    D=mul(d,hm2);common=mul(D,E)
    cleared=[[mul(top,common),mul(b,hm2,E),scale(-1,mul(k,g,E))],
             [mul(b,hm2,E),mul(c,hm2,E),scale(-1,mul(g,common))],
             [scale(-1,mul(k,g,E)),scale(-1,mul(g,common)),mul(g,e,D)]]
    if determinant3(cleared)!=mul(g,hm2,E,E,P):
        raise ValueError("Polynomial determinant/Leibniz identity failed")
    return P,hm2


def records(poly):
    return [[*p,v] for p,v in sorted(poly.items())]


def evaluate(poly,A,B,X):
    return sum(v*A**i*B**j*X**k for (i,j,k),v in poly.items())


def verify_certificate():
    P,limit=determinant_polynomial()
    if max(k for i,j,k in P)!=3:
        raise ValueError("Unexpected spectral polynomial degree")
    parts=[{(i,j,0):v for (i,j,k),v in P.items() if k==r} for r in range(4)]
    lower=add(parts[2],mul(parts[3],limit))
    positives=[parts[0],parts[1],lower]
    if any(not Q or any(v<=0 for v in Q.values()) or Q.get((0,0,0),0)<=0 for Q in positives):
        raise ValueError("A positive-coefficient polynomial certificate failed")
    if not parts[3] or any(v>=0 for v in parts[3].values()):
        raise ValueError("Cubic coefficient must be nonpositive")

    samples=[]
    for h,d in ((4,2),(6,3),(6,4),(7,4),(8,6),(12,6),(12,10),(50,30)):
        for lam in (F(-d),F(h-d-2),F(h-2*d-2,2)):
            g=d+lam;alpha=F(h-d,d);w=F(2*(d-1),d*(h-2));z=F(2*(2*d-h),d*(h-4)+2)
            b=-1+2*lam/d;c=h-alpha*lam;e=h+2+z-(1+z)*g
            # This direct scalar determinant is a second rational evaluation
            # of the polynomial, including g=0 where the 3-image is absent.
            det=(h+1)*c*e+2*b*(1+w)*g-(h+1)*g-c*(1+w)**2*g-e*b*b
            denominator=d**3*(h-2)**2*(d*(h-4)+2)
            A=h-d-2;B=2*d-h;X=A-lam
            if evaluate(P,A,B,X)!=denominator*det or det<=0:
                raise ValueError("Direct rational determinant cross-check failed")
            samples.append([h,d,str(lam),str(det)])
    certificate={"P0":records(parts[0]),"P1":records(parts[1]),
                 "P2_plus_limit_P3":records(lower),"minus_P3":records(scale(-1,parts[3]))}
    digest=sha256(json.dumps(certificate,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return dict(coefficient_domain="Z[A,B,X]",degree_X=3,expanded_terms=len(P),
                positive_terms=[len(Q) for Q in positives],
                positive_constant_coefficients=[Q[(0,0,0)] for Q in positives],
                negative_cubic_terms=len(parts[3]),certificate_sha256=digest,
                direct_rational_checks=samples),certificate


if __name__=="__main__":
    result,certificate=verify_certificate()
    print(json.dumps({"verification":result,"coefficient_certificate":certificate},sort_keys=True,indent=2))
