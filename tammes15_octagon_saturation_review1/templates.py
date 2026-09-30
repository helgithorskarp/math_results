"""Independent necessary rank-four Gram tests for all ten second-ear pairs.

No author imports, lens formula, radicals, or frame inputs. Arithmetic in
SymPy QQ(t); every possible unit common neighbor forces a 4x4 Gram
determinant to vanish, even when the first three vectors are dependent.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import sympy as sp
from sympy.polys.fields import field
from check import A_EDGES, B_EDGES, P, need

def polynomial_sign(coeffs):
    """Power coefficients -> Bernstein coefficients on the fixed interval."""
    if not coeffs:
        return 0
    n=len(coeffs)-1;lo=F(1,2);step=F(1,10)
    shifted=[sum((F(coeffs[j])*comb(j,k)*lo**(j-k)*step**k
                  for j in range(k,n+1)),F(0)) for k in range(n+1)]
    b=[sum((shifted[k]*F(comb(i,k),comb(n,k))
            for k in range(i+1)),F(0)) for i in range(n+1)]
    if all(v>=0 for v in b) and any(v>0 for v in b):return 1
    if all(v<=0 for v in b) and any(v<0 for v in b):return -1
    return 0

def coefficient_list(p):
    if not p:return []
    return [F(int(v.numerator),int(v.denominator))
            for i in range(p.degree()+1) for v in [sp.QQ(p.get((i,),0))]]

def determinant(M):
    # Leibniz determinant; no solve/inverse or generic rank assumption.
    from itertools import permutations
    z=M[0][0]*0;ans=z
    for p in permutations(range(len(M))):
        term=M[0][p[0]]
        for i in range(1,len(M)):term*=M[i][p[i]]
        parity=sum(p[i]>p[j] for i,j in combinations(range(len(M)),2))%2
        ans+=-term if parity else term
    return ans

def verify():
    K,t=field('t',sp.QQ);o=K.one;z=K.zero
    H=[[o if i==j else t for j in range(3)] for i in range(3)]
    def dot(x,y):return sum((x[i]*H[i][j]*y[j] for i in range(3) for j in range(3)),z)
    basis=[(o,z,z),(z,o,z),(z,z,o)];a={0:basis[0],6:basis[1],7:basis[2]}
    r=2*t/(o+t)
    for v,i,j,k in [(5,0,6,7),(4,0,5,6),(1,0,4,5),(3,1,4,0),(2,1,3,4)]:
        a[v]=tuple(r*(x+y)-q for x,y,q in zip(a[i],a[j],a[k]))
    b={0:basis[0],3:basis[1],4:basis[2]}
    for v,i,j,k in [(2,0,3,4),(1,0,2,3)]:
        b[v]=tuple(r*(x+y)-q for x,y,q in zip(b[i],b[j],b[k]))
    need(all(dot(p,p)==o for p in [*a.values(),*b.values()]),'symbolic patch norms')
    kappa=dot(b[1],b[4]);w=dot(a[2],a[7])
    nb={i:{j for j in range(8) if tuple(sorted((i,j))) in A_EDGES} for i in range(8)}
    need(not nb[2]&nb[7],'first exceptional pair')
    cases=[]
    for i,j in combinations(range(8),2):
        old=nb[i]&nb[j]
        if len(old)!=1:continue
        if any(len(nb[q])+sum(q==x for x in (2,7,i,j))>5 for q in range(8)):continue
        old=next(iter(old));wij=dot(a[i],a[j]);divisor=o+wij
        need(polynomial_sign(coefficient_list(divisor.numer))*
             polynomial_sign(coefficient_list(divisor.denom))>0,'forced-ear denominator')
        v=tuple(2*t/divisor*(x+y)-q for x,y,q in zip(a[i],a[j],a[old]))
        need(dot(v,v)==o and dot(v,a[i])==dot(v,a[j])==t,'symbolic second-ear identities')
        g2,g7=dot(a[2],v),dot(a[7],v)
        M=[[o,w,g2,t],[w,o,g7,t],[g2,g7,o,kappa],[t,t,kappa,o]]
        d=determinant(M)
        coeffs=coefficient_list(d.numer);den=coefficient_list(d.denom)
        ds=polynomial_sign(den);need(ds!=0,'Gram determinant denominator')
        ns=polynomial_sign(coeffs)
        cases.append({'pair':[i,j,old],'gram_determinant_sign':ns*ds,
                      'numerator':coeffs})
    need(len(cases)==10,'second-ear exhaustive coverage')
    active=[i for i,q in enumerate(cases) if q['gram_determinant_sign']==0]
    need(active==[8] and cases[8]['pair']==[5,6,0],'unique nonexcluded template')
    x=sp.Symbol('x');num=sp.Poly.from_list(
        [sp.Rational(v.numerator,v.denominator) for v in cases[8]['numerator'][::-1]],x,domain=sp.QQ)
    rootpoly=sp.Poly.from_list(P[::-1],x,domain=sp.QQ)
    quotient,remainder=sp.div(num,rootpoly)
    need(remainder.is_zero,'independent Gram numerator root factor')
    other=[F(int(v.p),int(v.q)) for v in reversed(quotient.all_coeffs())]
    need(polynomial_sign(other)!=0,'other Gram factors nonzero')
    need(num.count_roots(sp.Rational(1,2),sp.Rational(3,5))==1,'Gram numerator root count')
    return {'case_pairs':[q['pair'] for q in cases],
            'gram_determinant_signs':[q['gram_determinant_sign'] for q in cases],
            'active_index':8,'active_numerator':list(map(str,cases[8]['numerator'])),
            'other_factor':list(map(str,other)),
            'method':'all ten necessary rank-four Gram determinants; no squaring'}

if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2,sort_keys=True))
