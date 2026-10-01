"""Author six-sendov-1, researcher: generic exact four-variable arithmetic.

Copied with attribution from 4c04ae6fa05920f3f749ffec6ecb1f8aa3ad219a,
radial sixfold source. Earlier transform provenance is in LITERATURE.md.
No theorem or numerical signs are imported.
"""
from fractions import Fraction as F
from collections import defaultdict
from math import comb, lcm

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


def evaluate_fast(p, values):
    """Exact integer common-denominator evaluation, not rounded numerics."""
    if not p:
        return F(0)
    values = tuple(F(v) for v in values)
    degrees = tuple(max(e[i] for e in p) for i in range(4))
    coefficient_den = lcm(*(F(v).denominator for v in p.values()))
    weights = [[v.numerator ** j * v.denominator ** (n-j)
                for j in range(n+1)] for v, n in zip(values, degrees)]
    numerator = 0
    for e, coefficient in p.items():
        coefficient = F(coefficient)
        term = coefficient.numerator * (coefficient_den // coefficient.denominator)
        for i in range(4):
            term *= weights[i][e[i]]
        numerator += term
    denominator = coefficient_den
    for value, degree in zip(values, degrees):
        denominator *= value.denominator ** degree
    return F(numerator, denominator)


def compile_evaluator(p):
    """Prepare the same exact integer evaluation for repeated control points."""
    if not p:
        return lambda values: F(0)
    degrees = tuple(max(e[i] for e in p) for i in range(4))
    base = lcm(*(F(v).denominator for v in p.values()))
    terms = [(e, F(v).numerator * (base // F(v).denominator)) for e, v in p.items()]
    def evaluate_compiled(values):
        values = tuple(F(v) for v in values)
        weights = [[v.numerator**j * v.denominator**(n-j)
                    for j in range(n+1)] for v, n in zip(values, degrees)]
        total = 0
        for e, coefficient in terms:
            for i in range(4):
                coefficient *= weights[i][e[i]]
            total += coefficient
        denominator = base
        for value, degree in zip(values, degrees):
            denominator *= value.denominator**degree
        return F(total, denominator)
    return evaluate_compiled
