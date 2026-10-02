#!/usr/bin/env python3
"""Exact closed-cell support checks and rigorous determinant Bernstein gates.

Rational outward rounding is explicit. These polynomial routines supply
validated enclosures; geometric and determinant arguments are in PROOF.md.
"""
import os
for _key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_key]='1'
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from math import comb
import argparse,hashlib,json,resource,time
import geometry as H
SCALE=10**24

@dataclass(frozen=True)
class B:
    lo:int
    hi:int
    def __post_init__(self):
        H.require(type(self.lo)==type(self.hi)==int and self.lo<=self.hi,'integer outward enclosure')
    @staticmethod
    def rational(value):
        value=F(value);n=value.numerator*SCALE;d=value.denominator
        return B(n//d,-((-n)//d))
    @staticmethod
    def interval(value):
        a,b=B.rational(value.lo),B.rational(value.hi)
        return B(a.lo,b.hi)
    def __add__(self,other):return B(self.lo+other.lo,self.hi+other.hi)
    def __neg__(self):return B(-self.hi,-self.lo)
    def __sub__(self,other):return self+-other
    def __mul__(self,other):
        products=[self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi]
        return B(min(products)//SCALE,-((-max(products))//SCALE))
    def ratio(self,factor):
        factor=F(factor)
        if factor<0:return -self.ratio(-factor)
        n,d=factor.numerator,factor.denominator
        return B(self.lo*n//d,-((-self.hi*n)//d))
    def bounds(self):return [str(F(self.lo,SCALE)),str(F(self.hi,SCALE))]
    def absolute(self):return max(abs(self.lo),abs(self.hi))
ZERO,ONE=B(0,0),B(SCALE,SCALE)

def add(a,b):
    out=a.copy()
    for key,value in b.items():out[key]=out.get(key,ZERO)+value
    return {k:v for k,v in out.items()if v!=ZERO}

def neg(a):return {k:-v for k,v in a.items()}

def mul(a,b):
    out={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():
            key=(i+k,j+l);out[key]=out.get(key,ZERO)+v*w
    return {k:v for k,v in out.items()if v!=ZERO}

def determinant(matrix,deadline):
    n=len(matrix);H.require(all(len(row)==n for row in matrix),'square determinant')
    dp={0:{(0,0):ONE}}
    for row in range(n):
        if time.monotonic()>=deadline:raise TimeoutError('exact determinant gate deadline incomplete')
        following={}
        for mask,value in dp.items():
            for column in range(n):
                if mask&(1<<column):continue
                product=mul(value,matrix[row][column])
                if (mask>>(column+1)).bit_count()%2:product=neg(product)
                key=mask|(1<<column);following[key]=add(following.get(key,{}),product)
        dp=following
    return dp[(1<<n)-1]

def bernstein(polynomial,degree):
    H.require(all(i+j<=degree for i,j in polynomial),'triangle total polynomial degree')
    coefficients=[]
    for k in range(degree+1):
        for l in range(degree+1-k):
            value=ZERO
            for (i,j),a in polynomial.items():
                if i<=k and j<=l:
                    value=value+a.ratio(F(comb(k,i)*comb(l,j),comb(degree,i+j)*comb(i+j,i)))
            coefficients.append(value)
    return coefficients

def affine_triangle(coefficients,triangle):
    a,b,c=triangle
    return {(0,0):coefficients[0]+coefficients[1]*a[0]+coefficients[2]*a[1],
            (1,0):coefficients[1]*(b[0]-a[0])+coefficients[2]*(b[1]-a[1]),
            (0,1):coefficients[1]*(c[0]-a[0])+coefficients[2]*(c[1]-a[1])}
