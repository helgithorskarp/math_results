#!/usr/bin/env python3
"""Optional portable discovery/regeneration. SymPy 1.14.0 over Q(n).

Author: six-downset-3, researcher. One numeric/native thread. The independent
standard-library verify.py checks the output; neither CAS output nor finite
sampling replaces the harmonic-completeness and lift proofs in PROOF.md.
"""
import argparse
import itertools
import json
from pathlib import Path
import sympy as sp


def require(x,msg):
    if not x:raise ValueError(msg)


def normal(x):
    return sp.factor(sp.cancel(x))


def choose(x,k):
    return sp.prod(x-i for i in range(k))/sp.factorial(k)


def elementary(M):
    return [sp.Integer(1)]+[
        normal(sum(M.extract(ix,ix).det(method='domain-ge')
                   for ix in itertools.combinations(range(M.rows),k)))
        for k in range(1,M.rows+1)]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    require(sp.__version__=='1.14.0','reproduction requires SymPy 1.14.0')
    n,u=sp.symbols('n u')
    pairs=[(a,b) for a in range(1,5) for b in range(a,5)]
    variables=sp.symbols(' '.join('b%d%d'%p for p in pairs))
    B=sp.zeros(4)
    for (a,b),v in zip(pairs,variables):B[a-1,b-1]=B[b-1,a-1]=v
    N=normal(1+sum(choose(n,a) for a in range(1,5)))
    s=normal(sum(choose(n-1,b-1) for b in range(1,5)))
    equations=[sum(B[a-1,b-1]*choose(n-a-1,b-1) for b in range(1,5))-s for a in range(1,5)]
    equations += [sum(B[a-1,b-1]*choose(n-a,b) for b in range(1,5))-(N-1-s) for a in range(1,5)]
    sol=list(sp.linsolve(equations,variables))
    require(len(sol)==1,'single affine family representation')
    family=[normal(x) for x in sol[0]]
    free=sorted(set().union(*(x.free_symbols for x in family))-{n},key=str)
    require(list(map(str,free))==['b33','b34','b44'],'three generic free parameters')
    choices=sp.solve([family[i] for i in (0,1,4)],free)
    require(isinstance(choices,dict) and set(choices)==set(free),'b11=b12=b22=0 selection')
    substitution=dict(zip(variables,[normal(x.subs(choices)) for x in family]))
    require(all(normal(x.subs(substitution))==0 for x in equations),'generic linear residual')
    beta=B.subs(substitution)
    d=(n-4)*(n-3)*(n-2)
    b13=-2*n*(n-5)/((n-3)*(n-2))
    b14=n*(n*n+3*n-22)/d
    b23=-n*(n*n-9*n+2)/d
    b24=n*(n+1)*(n+2)/d
    b33=12*n*(n+3)/d
    b34=n*(n**3-3*n*n-16*n-108)/((n-6)*d)
    b44=n*(n**4-10*n**3+29*n*n-20*n+324)/((n-7)*(n-6)*d)
    expected=sp.Matrix([[0,0,b13,b14],[0,0,b23,b24],[b13,b23,b33,b34],[b14,b24,b34,b44]])
    require(all(normal(x)==0 for x in beta-expected),'all sixteen formula entries')
    # Boundary witnesses are separate exact substitutions in the original
    # counting equations. Never evaluate the generic formula at its poles.
    boundary={6:sp.Matrix([[-2,0,2,4],[0,sp.Rational(4,3),0,22],[2,0,24,0],[4,22,0,0]]),
              7:sp.Matrix([[0,sp.Rational(-8,5),1,4],[sp.Rational(-8,5),sp.Rational(2,5),3,6],
                           [1,3,2,26],[4,6,26,0]])}
    for nn,bb in boundary.items():
        subs=dict(zip(variables,[bb[a-1,b-1] for a,b in pairs]))
        require(all(x.subs(n,nn).subs(subs)==0 for x in equations),'separate boundary linear residual')
    m=N-1; q=(n*n-3*n+4)/2; A=s+(n-1)*q
    g=4*n**3-15*n*n+29*n-12
    H=m-n*s*s/A
    require(normal(A-g/6)==0,'star Gram eigenvalue')
    require(normal(H-n*(n-1)*(n**4+4*n**3+17*n*n-106*n+168)/(24*g))==0,
            'exact projection norm')
    delta=n*(n-1)*(n-2)*(n-3)/4; bound=3*(n-1)*(n-2)*(n-3)/2
    require(normal(delta/(2*bound*(bound*H+delta))-
                   4*g/(3*(n-1)*(n-2)*(n-3)*(n**5+3*n**4+29*n**3-183*n*n+390*n-216)))==0,
            'larger safe endpoint')
    mg={}
    for j in range(5):
        layers=list(range(max(1,j),5))
        K=sp.Matrix([[s*int(a==b)-(choose(n,b) if j==0 else 0)
                      +(-1)**j*beta[a-1,b-1]*choose(n-a-j,b-j)
                      for b in layers] for a in layers]).applyfunc(normal)
        G=sp.diag(*(choose(n-2*j,a-j) for a in layers))
        require(all(normal(x)==0 for x in G*K-(G*K).T),'harmonic metric symmetry')
        e=elementary(K);r=(2,3,3,2,1)[j]
        require(all(x==0 for x in e[r+1:]),'prescribed characteristic zero coefficients')
        for k in range(1,r+1):
            mg['C%d_shift_e%d'%(j,k)]=normal(sum((-1)**(k-l)*sp.binomial(r-l,k-l)*e[l] for l in range(k+1)))
            mg['U%d_shift_e%d'%(j,k)]=normal(sum((-1)**l*sp.binomial(r-l,k-l)*(N-1)**(k-l)*e[l] for l in range(k+1)))
    result={'agent':'six-downset-3','role':'researcher','coefficient_domain':'Q[n]',
            'substitution':'n=8+u,u>=0','CAS_discovery':'SymPy '+sp.__version__,'margins':{},
            'status':'Exact coefficient identities; all-orders soundness requires the harmonic, gap, lift and rank-repair proofs in PROOF.md.'}
    for name,x in mg.items():
        num,den=sp.fraction(normal(x.subs(n,8+u)))
        a=list(reversed(sp.Poly(num,u,domain=sp.ZZ).all_coeffs()))
        b=list(reversed(sp.Poly(den,u,domain=sp.ZZ).all_coeffs()))
        require(all(v>=0 for v in a+b) and a[0]>0 and b[0]>0,'positive polynomial coefficients')
        result['margins'][name]={'expression':str(x),'numerator_ascending':list(map(int,a)),
                                'denominator_ascending':list(map(int,b))}
    if args.check:require(result==json.loads(args.check.read_text()),'coefficient certificate differs')
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'ok':True,'CAS':'SymPy '+sp.__version__,'domain':'Q(n)',
                      'generic_free_parameters':list(map(str,free)),'zero_weight_choice':['b11','b12','b22'],
                      'positive_margins':len(mg),'separate_boundary_orders':sorted(boundary)}))


if __name__=='__main__':main()
