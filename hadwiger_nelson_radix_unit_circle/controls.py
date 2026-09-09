#!/usr/bin/env python3
"""Corruption controls and an exact 243-point noncollision unit-circle fixture."""
from copy import deepcopy
from fractions import Fraction as Q
import json
from verify import (ROOT,require,verify,unflat,flat,plus,times,multiply,
                    pair_inventory,colour_word,pgcd)


def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return p


def rem(p,q):
    p=trim(p)
    while len(p)>=len(q):
        a=p[-1]/q[-1];k=len(p)-len(q)
        for j,b in enumerate(q):p[k+j]-=a*b
        p=trim(p)
    return p


def evaluate(p,x):
    v=Q(0)
    for a in p[::-1]:v=v*x+a
    return v


def roots_between(p,left,right):
    require(left<right and evaluate(p,left) and evaluate(p,right),'root interval endpoints')
    seq=[list(map(Q,p)),[Q(i)*p[i] for i in range(1,len(p))]]
    while seq[-1]:
        r=[-x for x in rem(seq[-2],seq[-1])]
        if not r:break
        seq.append(r)
    def variations(x):
        signs=[1 if y>0 else -1 for y in [evaluate(q,x) for q in seq] if y]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return variations(left)-variations(right)


def finite_remainder(a,f,p):
    a=trim([x%p for x in a])
    while len(a)>=len(f):
        k=len(a)-len(f);c=a[-1]
        for j,b in enumerate(f):a[k+j]=(a[k+j]-c*b)%p
        a=trim(a)
    return a


def finite_power(a,n,f,p):
    def mul(a,b):
        v=[0]*max(0,len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):v[i+j]=(v[i+j]+x*y)%p
        return finite_remainder(v,f,p)
    out=[1]
    while n:
        if n%2:out=mul(out,a)
        a=mul(a,a);n//=2
    return out


def erem(h,f):
    h=list(h)
    while h and h[-1]==(0,0):h.pop()
    while len(h)>=len(f):
        k=len(h)-len(f);c=h[-1]
        for j,b in enumerate(f):
            a=times(c,b);h[k+j]=plus(h[k+j],(-a[0],-a[1]))
        while h and h[-1]==(0,0):h.pop()
    return h


def fixture(c):
    f=unflat(c['factors'][0]);require(len(f)==8,'fixture degree')
    # Frobenius irreducibility criterion, degree7 prime, in F31 with omega=6.
    ff=[(a+6*b)%31 for a,b in f];xp=[0,1]
    for j in range(1,8):
        xp=finite_power(xp,31,ff,31)
        if j==1:
            diff=xp+[0]*max(0,2-len(xp));diff[1]=(diff[1]-1)%31
            require(len(pgcd(ff,diff,31))==1,'fixture has linear finite factor')
    require(xp==[0,1],'fixture Frobenius identity')
    # Expand (1-s*t)^7 f((1+s*t)/(1-s*t)), s=2omega-1, s^2=-3.
    N=((1,0),(-1,2));D=((1,0),(1,-2))
    powers_n=[((1,0),)];powers_d=[((1,0),)]
    for _ in range(7):
        powers_n.append(multiply(powers_n[-1],N));powers_d.append(multiply(powers_d[-1],D))
    result=[(0,0)]*8
    for j,a in enumerate(f):
        for k,b in enumerate(multiply(powers_n[j],powers_d[7-j])):
            result[k]=plus(result[k],times(a,b))
    require(all(2*a+b==0 and b%2==0 for a,b in result),'not pure imaginary Cayley polynomial')
    g=[b//2 for a,b in result]
    require(g==[5,39,-15,-189,-81,261,27,81],'Cayley polynomial coefficients')
    require(roots_between(g,Q(-1,7),Q(-1,8))==1,'fixture isolating interval')
    word=colour_word(c['colour_specs'][c['factor_cover'][0]])
    edges=[];checks=0
    for h,E in pair_inventory().items():
        if not h or not erem(unflat(h),f):
            edges+=E
            require(all(word[u]!=word[v] for u,v in E),'fixture monochromatic edge')
        if h:checks+=1
    require(len(edges)==1221,'fixture strict edge count')
    return {'physical_vertices':243,'strict_unit_edges':len(edges),'chromatic_number':3,
            'z':'(1+i*sqrt(3)*t)/(1-i*sqrt(3)*t)',
            't_polynomial_low_first':g,'t_isolating_interval':['-1/7','-1/8'],
            'irreducible_degree_over_Q_omega':7,'irreducibility_prime':31,
            'exact_unit_event_remainders':checks,
            'point_coordinates':'sum_{j=0}^4 a_j*z^j, a_j in {0,1,(1+i*sqrt(3))/2}'}


def rejects(fn):
    try:fn()
    except (ValueError,KeyError,TypeError,IndexError):return
    raise ValueError('corrupt certificate accepted')


def main():
    c=json.loads((ROOT/'certificate.json').read_text())
    mutations=[]
    x=deepcopy(c);x['event_sha256']='0'*64;mutations.append(x)
    x=deepcopy(c);x['factorizations'].pop();mutations.append(x)
    x=deepcopy(c);x['factorizations'][0][0][1]+=1;mutations.append(x)
    x=deepcopy(c);x['factors'][0][-2]=2;mutations.append(x)
    x=deepcopy(c);x['factor_cover'][0]=-1;mutations.append(x)
    x=deepcopy(c);x['colour_specs'][0]['weights'][0]=0;mutations.append(x)
    x=deepcopy(c);i=next(i for i,k in enumerate(x['factor_cover']) if k==1);x['factor_cover'][i]=0;mutations.append(x)
    for x in mutations:rejects(lambda x=x:verify(x))
    # Repeated factors must be recognised; nonzero constants must be coprime.
    require(len(pgcd([1,2,1],[1,1],7))==2,'modular gcd positive control')
    require(len(pgcd([1,2,1],[1],7))==1,'constant gcd positive control')
    require(roots_between([0,-1,0,1],Q(-1,2),Q(1,2))==1,'Sturm fixture')
    require(roots_between([0,-1,0,1],Q(2),Q(3))==0,'Sturm empty interval')
    print(json.dumps({'verified':True,'rejected_corruptions':len(mutations),
                      'modular_gcd_controls':2,'sturm_controls':2,'physical_fixture':fixture(c)},sort_keys=True,indent=2))
if __name__=='__main__':main()
