"""Positive row clearing copied from credited9778; new univariate q4 shift.
Every division/removal/orientation is exact, with unchanged resource guards.
"""
from fractions import Fraction as F
from math import gcd,lcm,prod
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom,denominator
from exact import require

def shift(p):
 require(all(e[0]==0 for e in p.a),'univariate specialization')
 v=P({(0,1):1});q=4+v;answer=P()
 for e,c in sorted(p.a.items()):answer=answer+P(F(c,p.den))*q**e[1]
 return answer

def encode(p):return {'denominator':p.den,'terms':[[list(e),str(c)] for e,c in sorted(p.a.items())]}

def clear_original(matrix):
    # Multiply each ORIGINAL row by a positive-on-domain common denominator,
    # then divide only by exact positive common factors. Shift only afterward.
    positive={}
    for key,p in ATOMS.items():
        s=shift(p)
        if s.positive():positive[key]=(p,s,1)
        elif (-s).positive():positive[key]=(-p,-s,-1)
    rows=[];domains=[];removed=[];constants=[]
    for row in matrix:
        powers={}
        for z in row:
            for key,e in z.den.items():powers[key]=max(powers.get(key,0),e)
        require(all(k in positive for k in powers),'all row denominators positive on stated domain')
        sign=prod(positive[k][2]**e for k,e in powers.items())
        cleared=[sign*z.num*denominator({k:e-z.den.get(k,0) for k,e in powers.items() if e>z.den.get(k,0)}) for z in row]
        removals={}
        for k,(factor,_,_) in positive.items():
            while True:
                quotients=[z.exact_div(factor) for z in cleared]
                if any(z is None for z in quotients):break
                cleared=quotients;removals[k]=removals.get(k,0)+1
        den=1
        for z in cleared:den=lcm(den,z.den)
        content=0
        for z in cleared:
            for v in z.a.values():content=gcd(content,abs(v*(den//z.den)))
        require(content>0,'nonzero row and positive normalization')
        rows.append([P({e:v*(den//z.den)//content for e,v in z.a.items()}) for z in cleared])
        def data(items):
            return [{'original':encode(positive[k][0]),'shifted':encode(positive[k][1]),'power':e} for k,e in sorted(items.items())]
        domains.append(data(powers));removed.append(data(removals));constants.append(str(F(den,content)))
    return rows,domains,removed,constants
