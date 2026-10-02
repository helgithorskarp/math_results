"""Exact Q-coefficient positivity through four triangular load shifts.

The five-variable raw polynomial and each four-variable coefficient stay
separately below the fixed30000-term limit. No expanded shifted polynomial
in five variables or enlarged term limit is used.
"""
from fractions import Fraction as F
from pathlib import Path
from math import prod
import importlib.util,random,signal
spec=importlib.util.spec_from_file_location('four_coefficient_engine',Path(__file__).with_name('polynomial.py'))
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
engine.DIM=4;engine.ZERO=(0,)*4
P=engine.P;require=engine.require;ZERO=engine.ZERO
def var(i):return P({tuple(int(i==j) for j in range(4)):1})
def substitute(p,index,replacement):
    groups={}
    for ex,c in p.a.items():
        power=ex[index];key=tuple(0 if j==index else ex[j] for j in range(4))
        row=groups.setdefault(power,{})
        row[key]=row.get(key,0)+c
    out=P()
    for power in range(max(groups,default=-1),-1,-1):out=out*replacement+P(groups.get(power,{}),p.den)
    return out
def load_shifts(p):
    # Initial variables t,D,a,u; final variables T,B,V,U.
    # Triangular order prevents revisiting newly substituted variables.
    for index,replacement in [(2,2*var(1)+var(2)),(3,var(0)+var(3)),(1,var(0)+var(1)+1),(0,var(0)+1)]:p=substitute(p,index,replacement)
    return p
def evaluate(p,point):
    return sum((F(c,p.den)*prod(F(x)**e for x,e in zip(point,ex)) for ex,c in p.a.items()),F(0))
def split_Q(raw):
    groups={}
    require(raw.den>0,'positive raw coefficient denominator')
    for ex,c in raw.a.items():
        require(len(ex)==5 and all(type(x) is int and x>=0 for x in ex),'raw five-variable exponent')
        row=groups.setdefault(ex[0],{});key=tuple(ex[1:])
        require(key not in row,'duplicate coefficient monomial');row[key]=c
    return {power:P(row,raw.den) for power,row in groups.items()}
def certify(raw):
    rows=[]
    for power,original in sorted(split_Q(raw).items()):
        signal.alarm(60);shifted=load_shifts(original)
        require(all(c>=0 for c in shifted.a.values()),'negative shifted coefficient')
        if power==0:require(shifted.positive(),'strict Q0 coefficient')
        for point in [(0,0,0,0),(1,2,3,4)]:
            T,B,V,U=point;t=T+1;D=t+B+1;a=2*D+V;u=t+U
            require(evaluate(shifted,point)==evaluate(original,(t,D,a,u)),'shifted/unshifted point identity control')
        rows.append({'Q_power':power,'terms':len(shifted.a),'degree':shifted.degree(),'constant':str(F(shifted.a.get(ZERO,0),shifted.den)),'sha256':shifted.fingerprint(),'nonnegative_coefficients':True})
        signal.alarm(0)
    require(rows and rows[0]['Q_power']==0,'missing strict Q0 coefficient')
    return {'raw_terms':len(raw.a),'raw_degree':raw.degree(),'raw_sha256':raw.fingerprint(),'Q_coefficients':rows,'total_shifted_coefficient_terms':sum(row['terms'] for row in rows),'strictly_positive_on_nonnegative_domain':True}
def shift_controls():
    # Direct schoolbook power substitution, independent of Horner's recursion.
    rng=random.Random(202610012)
    replacements=[var(0)+1,var(0)+var(1)+2,2*var(0)+2*var(1)+var(2)+4,var(0)+var(3)+1]
    for repeat in range(3):
        raw=P({tuple(rng.randrange(3) for _ in range(4)):rng.randrange(-20,21) for _ in range(6)},7)
        direct=P()
        for ex,c in raw.a.items():
            term=P(F(c,raw.den))
            for i,e in enumerate(ex):
                for _ in range(e):term=engine.reference_mul(term,replacements[i])
            direct=direct+term
        require(load_shifts(raw)==direct,'Horner/direct-power shift control')
    require(not P(-1).positive(),'negative coefficient rejected')
    require(not P({(1,0,0,0):1}).positive(),'missing positive constant rejected')
