#!/usr/bin/env python3
"""Reconstruct every rational endpoint coefficient by two exact derivations.

This certifies the finite polynomial step. The minimizer, geometric and
communication-identity reductions are written mathematics in PROOF.md.
Python >=3.11, standard library only, no floating arithmetic or external data.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json


def profile_expansion(k):
    """Binomial expansion followed by analytic integration in t."""
    m = 6-k
    out = defaultdict(Q)
    r2 = [(0,0,Q(1)), (1,1,Q(8)), (2,2,Q(16))]
    for i in range(k+1):
        for j in range(m+1):
            n = i+j
            for h in range(j+1):
                scale = Q(9*(-1)**n*comb(k,i)*comb(m,j)*comb(j,h))*Q(8,m)**h
                for v in range(h+1):
                    c = scale*comb(h,v)*(-1)**v
                    for a in range(9-n):
                        out[n+h+a,h,v] += c*comb(8-n,a)/((n+1)*(n+2))
                    for a in range(7-n):
                        d = c*comb(6-n,a)
                        for ra,rv,rc in r2:
                            out[n+h+a+ra,h,v+rv] += d*rc/(n+2)
                            out[n+h+a+ra+2,h,v+rv] -= d*rc/((n+2)*(n+3))
    for h in range(m+1):
        scale = Q(comb(m,h))*Q(8,m)**h
        for v in range(h+1):
            c = scale*comb(h,v)*(-1)**v
            for ra,rv,rc in r2:
                out[h+ra,h,v+rv] -= c*rc
    return {e:c for e,c in out.items() if c}


def add(p,q,scale=Q(1)):
    out = defaultdict(Q,p)
    for e,c in q.items():
        out[e] += scale*c
    return {e:c for e,c in out.items() if c}


def mul(p,q):
    out = defaultdict(Q)
    for e,c in p.items():
        for f,d in q.items():
            out[tuple(x+y for x,y in zip(e,f))] += c*d
    return {e:c for e,c in out.items() if c}


def power(p,n):
    one = {(0,)*len(next(iter(p))):Q(1)}
    for _ in range(n):
        one = mul(one,p)
    return one


def profile_products(k):
    """Multiply the defining factors in (a,u,v,t), then integrate exactly."""
    m = 6-k
    one = {(0,0,0,0):Q(1)}
    a = {(1,0,0,0):Q(1)}
    u = {(0,1,0,0):Q(1)}
    v = {(0,0,1,0):Q(1)}
    t = {(0,0,0,1):Q(1)}
    d = add(one,a)
    r = add(one,mul(a,v),Q(4))
    c = add(one,mul(mul(a,u),add(one,v,Q(-1))),Q(8,m))
    lower_factor = add(d,mul(a,t),Q(-1))
    free_factor = add(d,mul(mul(a,t),c),Q(-1))
    bt = mul(add(one,power(a,2),Q(-1)),t)
    paired_factor = add(mul(power(d,2),add(one,t,Q(-1))),
                        mul(add(bt,mul(power(a,2),power(t,2))),power(r,2)))
    f = mul(mul(power(lower_factor,k),power(free_factor,m)),paired_factor)
    out = defaultdict(Q)
    for (i,j,h,n),c0 in f.items():
        out[i,j,h] += Q(9)*c0/(n+1)
    radius_product = mul(power(r,2),power(c,m))
    for (i,j,h,n),c0 in radius_product.items():
        assert n==0
        out[i,j,h] -= c0
    return {e:c for e,c in out.items() if c}


def to_bernstein(p,degree):
    assert all(e[i]<=degree[i] for e in p for i in range(3))
    basis = dict(p)
    for axis,n in enumerate(degree):
        out = defaultdict(Q)
        for e,c in basis.items():
            for k in range(e[axis],n+1):
                f = list(e); f[axis]=k
                out[tuple(f)] += c*Q(comb(k,e[axis]),comb(n,e[axis]))
        basis = dict(out)
    return {e:basis.get(e,Q(0)) for e in product(*(range(n+1) for n in degree))}


def to_power(basis,degree):
    """Independent reverse basis expansion using B_i^n=x^i(1-x)^(n-i) C(n,i)."""
    out = dict(basis)
    for axis,n in enumerate(degree):
        power_coefficients = defaultdict(Q)
        for e,c in out.items():
            i = e[axis]
            for h in range(n-i+1):
                f = list(e); f[axis]=i+h
                power_coefficients[tuple(f)] += c*comb(n,i)*comb(n-i,h)*(-1)**h
        out = {e:c for e,c in power_coefficients.items() if c}
    return out


def check_bound(k,degree,basis,positive_lower=Q(44,7)):
    zero = [e for e,c in basis.items() if c==0]
    assert zero == ([(11,1,0)] if k==5 else [])
    assert all(c>=positive_lower for c in basis.values() if c)
    assert all(c==8 for e,c in basis.items() if e[0]==0)
    assert len(basis)==(degree[0]+1)*(degree[1]+1)*(degree[2]+1)


def digest_coefficients(basis):
    encoded = ''.join(','.join(map(str,e))+':'+str(c.numerator)+'/'+str(c.denominator)+'\n'
                      for e,c in sorted(basis.items())).encode('ascii')
    return hashlib.sha256(encoded).hexdigest()


def example():
    """Factorization, real-cubic discriminant and strict scope separation."""
    a,t,s = Q(3,4),Q(3,4),Q(1,4)
    w = {(1,):Q(1)}; one = {(0,):Q(1)}
    A = a+t
    p_w = mul(mul(add(w,one,-A),power(w,6)),add(power(w,2),one,s*s))
    derivative = {(e[0]-1,):c*e[0] for e,c in p_w.items() if e[0]}
    cubic = {(3,):Q(9),(2,):-8*A,(1,):7*s*s,(0,):-6*A*s*s}
    assert derivative==mul(power(w,5),cubic)
    aa,bb,cc,dd = [cubic[(i,)] for i in [3,2,1,0]]
    disc = bb*bb*cc*cc-4*aa*cc**3-4*bb**3*dd-27*aa*aa*dd*dd+18*aa*bb*cc*dd
    def evaluate(value):
        return sum(c*value**e[0] for e,c in cubic.items())
    assert disc==Q(-4174875,1024)<0
    assert evaluate(t)==Q(-51,16)<0<evaluate(A)
    assert t*t+s*s==Q(5,8)<1 and a<1
    other_root_product=A**6*(A*A+s*s)
    assert other_root_product==Q(26973,1024)>9
    assert cubic[(0,)]!=0
    return {'cubic_discriminant':str(disc),'cubic_at_z_zero':str(evaluate(t)),
            'other_root_distance_product':str(other_root_product),
            'complex_original_root_radius_squared':str(t*t+s*s)}


def derive():
    summaries=[]; profiles=[]
    for k in range(6):
        p=profile_expansion(k)
        assert p==profile_products(k), ('independent factor expansion failed',k)
        degree=(16,6,12) if k==0 else (16-k,6-k,8-k)
        basis=to_bernstein(p,degree)
        assert to_power(basis,degree)==p, ('reverse basis identity failed',k)
        check_bound(k,degree,basis)
        positive=[c for c in basis.values() if c>0]
        summaries.append({'k':k,'degree':list(degree),'coefficients':len(basis),
                          'minimum_positive':str(min(positive)),
                          'zero_indices':[list(e) for e,c in basis.items() if c==0],
                          'sha256':digest_coefficients(basis)})
        profiles.append((k,p,degree,basis))
    # Meaningful rejection checks: false uniform coefficient bound, corrupted
    # origin polynomial, and a corrupted but positive Bernstein certificate.
    rejected=0
    try:
        check_bound(5,profiles[5][2],profiles[5][3],Q(8))
    except AssertionError:
        rejected+=1
    corrupted=dict(profiles[1][1]); corrupted[(0,0,0)]+=1
    if corrupted!=profile_products(1):
        rejected+=1
    corrupted_basis=dict(profiles[0][3]); corrupted_basis[(0,0,0)]+=1
    if to_power(corrupted_basis,profiles[0][2])!=profiles[0][1]:
        rejected+=1
    assert rejected==3
    return {'schema':1,'arithmetic':'Python Fraction, all exact',
            'profiles':summaries,'total_coefficients':sum(r['coefficients'] for r in summaries),
            'independent_polynomial_identities':6,'complete_reverse_basis_identities':6,
            'mutation_rejections':rejected,'scope_example':example()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected',type=Path,
                        help='write compact deterministic evidence instead of comparing it')
    args=parser.parse_args()
    result=derive()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(result,indent=2)+'\n')
    else:
        expected=json.loads(Path(__file__).with_name('expected.json').read_text())
        assert result==expected, 'compact evidence mismatch'
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
