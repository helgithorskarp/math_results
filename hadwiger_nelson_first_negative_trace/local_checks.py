"""Exact symbolic expansion and exhaustive modulo-eight scope checks."""
from verify import A,load,require
from itertools import product
from hashlib import sha256
import json


def symbolic():
    M=load('polynomials','hadwiger_nelson_cross_six_cycle/identities.py',
           '2c0b7986b5da71c06f5d152a4c83c0c6196c2cdac3942cab6243f5da0541e370')
    a,b,c,d,z,w,s,t,D,E,h=M.variables('a b c d z w s t D E h')
    def plus(x,y):return tuple(a+b for a,b in zip(x,y))
    def minus(x,y):return tuple(a-b for a,b in zip(x,y))
    def scale(x,c):return tuple(c*a for a in x)
    def times(x,y):
        a,b=x;c,d=y
        return a*c-b*d,a*d+b*c-b*d
    def bar(x):return x[0]-x[1],-x[1]
    def trace(x):return 2*x[0]-x[1],0
    def norm(x):return x[0]*x[0]-x[0]*x[1]+x[1]*x[1],0
    X,Y,Z,W,U=(a,b),(c,d),(z,w),(s,t),(D,E)
    def f(x,y):return minus(plus(norm(x),scale(norm(y),4)),times(U,times(bar(x),y)))
    left=minus(f(plus(X,scale(Z,2*h)),plus(Y,scale(W,h))),f(X,Y))
    linear=minus(plus(scale(trace(times(bar(X),Z)),2),scale(trace(times(bar(Y),W)),4)),
                 times(U,plus(times(bar(X),W),scale(times(bar(Z),Y),2))))
    quadratic=minus(scale(plus(norm(Z),norm(W)),2),times(U,times(bar(Z),W)))
    right=scale(plus(linear,scale(quadratic,2*h)),h)
    require(all(not (M.P(x)-M.P(y)).terms for x,y in zip(left,right)),'scaled identity failed')
    return {'coefficient_identities':2,'left_term_counts':[len(M.P(x).terms) for x in left]}


def quotient_audit():
    m=8;pts=list(product(range(m),repeat=2))
    def norm(x):return (x[0]**2-x[0]*x[1]+x[1]**2)%m
    def bar(x):return (x[0]-x[1])%m,-x[1]%m
    def mul(x,y):
        # Evaluate the product polynomial and reduce omega^2=-omega-1.
        p=[x[0]*y[0],x[0]*y[1]+x[1]*y[0],x[1]*y[1]]
        return (p[0]-p[2])%m,(p[1]-p[2])%m
    units=[p for p in pts if norm(p)%2]
    count=0;h=sha256();deep=[]
    for D in units:
        for x in pts:
            for y in pts:
                c=mul(D,mul(bar(x),y))
                if ((2*(norm(x)+norm(y))-c[0])%m,-c[1]%m)!=(2,0):continue
                count+=1
                xunit=bool(norm(x)%2);yunit=bool(norm(y)%2)
                require(xunit!=yunit,'integral residue split failed')
                shallow=y if xunit else x
                require(all(a%4==0 for a in shallow),'zero endpoint not in 4O')
                h.update((json.dumps([D,x,y],separators=(',',':'))+'\n').encode())
    for k in (1,2,3):
        groups={};solutions=0;hh=sha256();mx=1<<k;my=1<<(k-1)
        for D in units:
            for X in units:
                for Y in units:
                    c=mul(D,mul(bar(X),Y))
                    if ((norm(X)+4*norm(Y)-c[0]-(1<<(2*k)))%m,-c[1]%m)!=(0,0):continue
                    solutions+=1
                    key=(D,tuple(x%mx for x in X),tuple(y%my for y in Y))
                    shallow=tuple(y%mx for y in Y)
                    require(key not in groups or groups[key]==shallow,'shallow residue class is not constant')
                    groups[key]=shallow
                    hh.update((json.dumps([D,X,Y],separators=(',',':'))+'\n').encode())
        deep.append({'k':k,'candidate_scaled_pairs':len(units)**3,'solutions_mod8':solutions,
                     'source_coset_groups':len(groups),'shallow_residue_classes_per_group':1,
                     'solution_stream_sha256':hh.hexdigest()})
    return {'modulus':m,'unit_traces_D':len(units),'integral_candidate_pairs':len(units)*len(pts)**2,
            'integral_solutions':count,'integral_solution_sha256':h.hexdigest(),'nonintegral':deep,
            'finite_checks_are_not_the_uniform_proof':True}

if __name__=='__main__':
    print(json.dumps({'symbolic':symbolic(),'quotient_audit':quotient_audit()},indent=2))
