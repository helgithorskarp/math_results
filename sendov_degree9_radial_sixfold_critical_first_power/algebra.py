"""Sparse Q-polynomials in four variables. Author six-sendov-1, researcher.

Generic arithmetic reused from own source
f91cf040994c04fc1e7f03941695121064279d7a, algebra.py.
No multiplicity theorem or empirical signs are imported.
"""
from fractions import Fraction as F
from collections import defaultdict
from math import comb

ZERO=(0,)*4
ONE={ZERO:F(1)}

def add(*items):
 out=defaultdict(F)
 for p in items:
  for e,v in p.items():out[e]+=v
 return {e:v for e,v in out.items() if v}

def scale(p,v):return {e:k*v for e,k in p.items() if k*v}

def mul(p,r):
 out=defaultdict(F)
 for e,v in p.items():
  for f,k in r.items():out[tuple(a+b for a,b in zip(e,f))]+=v*k
 return {e:v for e,v in out.items() if v}

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

def canonical(p):return [[list(e),str(v)] for e,v in sorted(p.items())]

def evaluate(p,values):
 out=F(0)
 powers=[[values[i]**j for j in range(max(e[i] for e in p)+1)] for i in range(4)]
 for e,v in p.items():
  for i in range(4):v*=powers[i][e[i]]
  out+=v
 return out
