#!/usr/bin/env python3
"""Exact rational-polynomial kernel adapted from this reviewer's published audit9984.
All arithmetic is integer or Fraction. No target module or fixture is read.
"""
import argparse, hashlib, itertools, json, math, sys, time
from fractions import Fraction as F
from pathlib import Path
START=time.monotonic(); GUARD=45

def require(ok,msg):
    if not ok: raise ValueError(msg)
def tick(): require(time.monotonic()-START<GUARD,'incomplete: 45-second guard')
def trim(p):
    p=list(p)
    while p and not p[-1]:p.pop()
    return tuple(p)
def add(a,b):return trim((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b))))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,k):return trim(x*k for x in a)
def mul(a,b):
    if not a or not b:return ()
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def power(a,n):
    b=(1,)
    for _ in range(n):b=mul(b,a)
    return b
def primitive(p):
    p=trim(p)
    if not p:return p
    g=math.gcd(*p)
    return tuple(x//g for x in p)
def prem(a,b):
    """Positive multiple of the ordinary rational Euclidean remainder."""
    require(bool(b),'zero polynomial divisor');r=a
    while r and len(r)>=len(b):
        d=len(r)-len(b);k=r[-1];lead=b[-1]
        r=primitive(sub(scale(r,abs(lead)),(0,)*d+scale(b,k*(1 if lead>0 else -1))))
    return r
def gcdp(a,b):
    a,b=primitive(a),primitive(b)
    while b:a,b=b,prem(a,b)
    return neg(a) if a and a[-1]<0 else a
def exactdiv(a,b):
    require(bool(b),'zero exact divisor');r=a;q=[0]*max(0,len(a)-len(b)+1)
    while r and len(r)>=len(b):
        d=len(r)-len(b);k,rem=divmod(r[-1],b[-1]);require(rem==0,'nonintegral exact division')
        q[d]+=k;r=sub(r,(0,)*d+scale(b,k))
    require(not r,'inexact polynomial division');return trim(q)
def evaluate(a,x):
    z=F(0)
    for c in reversed(a):z=z*x+c
    return z
def derivative(a):return trim(i*a[i] for i in range(1,len(a)))
class Rat:
    def __init__(self,n=0,d=(1,)):
        n=(n,) if isinstance(n,int) else trim(n);d=(d,) if isinstance(d,int) else trim(d)
        require(bool(d),'zero rational denominator')
        if not n:self.n,self.d=(),(1,);return
        g=gcdp(n,d);n,d=exactdiv(n,g),exactdiv(d,g)
        content=math.gcd(*(n+d));n,d=tuple(x//content for x in n),tuple(x//content for x in d)
        if d[-1]<0:n,d=neg(n),neg(d)
        self.n,self.d=n,d
    def __add__(self,o):
        o=o if isinstance(o,Rat) else Rat(o);return Rat(add(mul(self.n,o.d),mul(o.n,self.d)),mul(self.d,o.d))
    __radd__=__add__
    def __neg__(self):return Rat(neg(self.n),self.d)
    def __sub__(self,o):return self+-asrat(o)
    def __rsub__(self,o):return asrat(o)+-self
    def __mul__(self,o):
        o=asrat(o);return Rat(mul(self.n,o.n),mul(self.d,o.d))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=asrat(o);require(bool(o.n),'zero rational inverse');return Rat(mul(self.n,o.d),mul(self.d,o.n))
    def __rtruediv__(self,o):return asrat(o)/self
    def __pow__(self,n):return Rat(power(self.n,n),power(self.d,n))
    def val(self,x):return evaluate(self.n,x)/evaluate(self.d,x)
def asrat(x):return x if isinstance(x,Rat) else Rat(x)
