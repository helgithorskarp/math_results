"""Exact integer polynomials and complete quadratic-field sign certificates."""
from pathlib import Path
from fractions import Fraction as F
from math import comb,isqrt
import json,hashlib


def decode(xs):
    out={}
    for power,value in xs:
        number=F(value)
        if number.denominator!=1:raise ValueError('integer coefficient encoding')
        if number:out[tuple(power)]=int(number)
    return out


def clean(out):return {power:value for power,value in out.items() if value}
def scale(a,t):return clean({power:t*value for power,value in a.items()})
def add(*polys):
    out={}
    for poly in polys:
        for power,value in poly.items():out[power]=out.get(power,0)+value
    return clean(out)


def mul(a,b):
    out={}
    for (i,j),x in a.items():
        for (ii,jj),y in b.items():
            power=i+ii,j+jj
            out[power]=out.get(power,0)+x*y
    return clean(out)


def digest(poly):
    return hashlib.sha256(json.dumps([[list(power),str(value)] for power,value in sorted(poly.items())],separators=(',',':')).encode()).hexdigest()


def evaluate(poly,q,k):return sum(value*q**i*k**j for (i,j),value in poly.items())


def divide(num,den):
    """Exact division in Z[q,k], including the full multiply-back check."""
    if not den:raise ValueError('zero whole polynomial denominator')
    if any(type(v) is not int for poly in (num,den) for v in poly.values()):
        raise ValueError('integer polynomial division input')
    rest=dict(num);out={};power,leading=max(den.items())
    while rest:
        position,value=max(rest.items())
        delta=position[0]-power[0],position[1]-power[1]
        if min(delta)<0:raise ValueError('nondivisible whole polynomial monomial')
        coefficient,remainder=divmod(value,leading)
        if remainder:raise ValueError('nondivisible integer polynomial coefficient')
        out[delta]=out.get(delta,0)+coefficient
        for (i,j),number in den.items():
            target=i+delta[0],j+delta[1]
            next_value=rest.get(target,0)-coefficient*number
            if next_value:rest[target]=next_value
            elif target in rest:del rest[target]
    out=clean(out)
    if mul(out,den)!=num:raise ValueError('whole polynomial division multiply-back failed')
    return out


def shift_k(poly,k0):
    out={}
    for (i,j),value in poly.items():
        for jj in range(j+1):
            power=i,jj
            out[power]=out.get(power,0)+value*comb(j,jj)*k0**(j-jj)
    return clean(out)


def curve(poly):
    """2^degree N((6k-29+P)/2+u,k)=F(u,k)+P H(u,k).

    Exact Horner arithmetic in Q[k,u,P]/(P^2-(28k^2+36k+81)).
    Pair coordinates are (u degree,k degree).
    """
    degree=max(i for i,j in poly)
    L={(0,1):6,(0,0):-29,(1,0):2};B={(0,2):28,(0,1):36,(0,0):81}
    bydegree=[{} for _ in range(degree+1)]
    for (i,j),value in poly.items():bydegree[i][0,j]=value
    a,b=bydegree[degree],{}
    for i in range(degree-1,-1,-1):
        a,b=add(mul(L,a),mul(B,b),scale(bydegree[i],2**(degree-i))),add(a,mul(L,b))
    return a,b


def surd_sign(a,b):
    # Exact comparison of a+b sqrt7; sqrt7 is irrational.
    if a==b==0:return 0
    if a>=0 and b>=0:return 1
    if a<=0 and b<=0:return -1
    value=a*a-7*b*b
    if not value:raise ValueError('impossible nonzero rational sqrt7')
    return (1 if value>0 else -1) if a>0 else (1 if value<0 else -1)


def curve_certificate(poly,k0,upper_num=4,upper_den=1):
    a,b=curve(poly);a,b=shift_k(a,k0),shift_k(b,k0)
    plus={power:value for power,value in b.items() if value>0}
    minus={power:value for power,value in b.items() if value<0}
    # 17/5+2sqrt7 k < P < upper_num/upper_den+2sqrt7 k.
    # Lower bound holds for k>0. Upper4 holds for k>=19;
    # upper7/2 is valid for k>=67.
    common=5*upper_den
    actual_a=add(scale(a,common),scale(plus,17*upper_den),scale(minus,5*upper_num))
    actual_b=scale(mul({(0,1):1,(0,0):k0},b),2*common)
    powers=set(actual_a)|set(actual_b)
    negative=[power for power in powers if surd_sign(actual_a.get(power,0),actual_b.get(power,0))<0]
    return {'k0':k0,'upper_P_additive_bound':str(F(upper_num,upper_den)),
            'whole_polynomial_count':len(powers),'negative_count':len(negative),
            'positive_constant':surd_sign(actual_a.get((0,0),0),actual_b.get((0,0),0))>0,
            'entire_lower_pair_sha256':[digest(actual_a),digest(actual_b)],
            'negative_head':[list(power) for power in sorted(negative)[:8]],
            'is_completed_certificate':not negative and surd_sign(actual_a.get((0,0),0),actual_b.get((0,0),0))>0}


def cutoff(k):
    D=28*k*k+36*k+81
    q=(6*k-25+isqrt(D))//2
    while 2*q-6*k+25<0 or (2*q-6*k+25)**2<D:q+=1
    return q-2


def fixed_k(poly,q0,k):
    dense=[0]*(max(i for i,j in poly)+1)
    for (i,j),value in poly.items():dense[i]+=value*k**j
    shifted=[sum(dense[j]*comb(j,i)*q0**(j-i) for j in range(i,len(dense))) for i in range(len(dense))]
    return {'q0':q0,'k':k,'negative_count':sum(value<0 for value in shifted),
            'positive_constant':shifted[0]>0,'degree':len(shifted)-1,
            'whole_shifted_sha256':digest({(i,0):v for i,v in enumerate(shifted) if v})}
