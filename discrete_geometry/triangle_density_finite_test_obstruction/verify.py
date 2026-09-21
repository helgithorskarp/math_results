#!/usr/bin/env python3
"""Audit common multipliers by direct matrices and multiplication determinants.

Finite corroboration of PROOF.md, not a universal computational proof.
CPython 3.11+, standard library. Checks remain active under -O.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from hashlib import sha256
import json
import sys
import construct as producer


def require(ok,msg):
    if not ok:raise ValueError(msg)


def normalize(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:normalize(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [normalize(v) for v in o]
    return o


def determinant(a):
    """Bareiss, independently of the producer's conjugate multiplication."""
    a=[list(map(int,row)) for row in a];n=len(a);prev=1;sign=1
    for k in range(n-1):
        pivot=next((j for j in range(k,n) if a[j][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        p=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                val=a[i][j]*p-a[i][k]*a[k][j]
                require(val%prev==0,'Bareiss division inexact')
                a[i][j]=val//prev
            a[i][k]=0
        prev=p
    return sign*a[-1][-1]


def norm_matrix(rad,t):
    """Multiplication by t-sum sqrt(rad) on the monomial radical basis."""
    n=1<<len(rad);a=[[0]*n for _ in range(n)]
    for mask in range(n):
        a[mask][mask]=t
        for j,r in enumerate(rad):
            a[mask^(1<<j)][mask]-=r if mask&(1<<j) else 1
    return a


def independent_rank(rad):
    """Prime-valuation bit vectors, unlike the producer's square-root tests."""
    rows=[];primes=set()
    for r in rad:
        x=abs(r);f={-1};p=2
        while p*p<=x:
            odd=0
            while x%p==0:x//=p;odd^=1
            if odd:f.add(p)
            p+=1
        if x>1:f.add(x)
        rows.append(f);primes|=f
    piv={}
    for f in rows:
        f=set(f)
        while f:
            p=max(f)
            if p in piv:f^=piv[p]
            else:piv[p]=f;break
    return len(piv)


def check_matrix(g,s,alpha):
    actual=[[sum(s[k][i]*g[k][l]*s[l][j] for k in (0,1) for l in (0,1))
             for j in (0,1)] for i in (0,1)]
    require(actual==[[alpha*g[i][j] for j in (0,1)] for i in (0,1)],'direct similitude check')
    require(s[0][0]*s[1][1]-s[0][1]*s[1][0]==alpha,'similitude determinant')


def evaluation(p,t):return sum(c*t**i for i,c in enumerate(p))


def run():
    path=Path(__file__).with_name('fixtures.json');fixtures=json.loads(path.read_text())
    output=[];counts={'suites':0,'forms':0,'matrix_identities':0,'norm_determinants':0,'rejections':0}
    for case in fixtures:
        r=producer.construct(case['forms']);rad=r['radicands'];alpha=r['common_integer'];t=r['t']
        require(len(r['forms'])==len(case['forms']),'all input forms have certificates')
        require(independent_rank(rad)==len(rad),'square-class rank')
        require(len(r['norm_polynomial'])==r['field_degree']+1,'norm degree')
        require(r['field_degree']==2**len(rad),'field degree')
        # Values at degree+1 distinct integers determine the entire norm polynomial.
        for k in range(r['field_degree']+1):
            require(determinant(norm_matrix(rad,k))==evaluation(r['norm_polynomial'],k),'norm polynomial determinant')
            counts['norm_determinants']+=1
        require(determinant(norm_matrix(rad,t))==alpha,'large norm determinant')
        counts['norm_determinants']+=1
        require(alpha.denominator==1 and alpha>0 and isqrt(alpha.numerator)**2!=alpha,'nonsquare norm')
        cert=r['nonsquare_certificate'];q=cert['square_part'];rem=cert['remainder']
        qq=[F(0)]*(2*len(q)-1)
        for i,x in enumerate(q):
            for j,y in enumerate(q):qq[i+j]+=x*y
        padded=rem+[F(0)]*(len(qq)-len(rem))
        require([a+b for a,b in zip(qq,padded)]==r['norm_polynomial'],'square-part identity')
        require(len(rem)-1<len(q)-1 and any(rem),'remainder degree')
        for dt in [0,1,2]:
            val=evaluation(r['norm_polynomial'],t+dt)
            require(val>0 and val.denominator==1 and isqrt(val.numerator)**2!=val,'threshold boundary check')
        for form,rec in zip(case['forms'],r['forms']):
            g=[list(map(F,row)) for row in form];d=g[0][0]*g[1][1]-g[0][1]*g[1][0]
            require(rec['determinant']==d and rec['u']**2+d*rec['v']**2==alpha,'norm representation')
            check_matrix(g,rec['matrix'],alpha);check_matrix(g,rec['near_identity_matrix'],r['squared_scale'])
            counts['forms']+=1;counts['matrix_identities']+=2
        near=r['squared_scale'];require(1<near<(1+F(1,1000))**2,'near-identity interval')
        counts['suites']+=1;output.append({'name':case['name'],'certificate':r})
    # A small, independently specified missed-test example.
    alpha=F(325,324)
    require(13==2**2+3**2==1**2+3*2**2,'common 13 norms')
    for d,v in [(1,(F(36,65),F(54,65))),(3,(F(18,65),F(36,65)))]:
        require(alpha*(v[0]**2+d*v[1]**2)==1,'explicit positive density witness')
    residues={x*x%13 for x in range(13)}
    require((-2)%13 not in residues,'missed triangle norm obstruction')
    require(alpha.numerator%13==0 and alpha.numerator%(13**2)!=0 and alpha.denominator%13!=0,'odd 13 valuation')
    # This monic positive quartic tests a genuinely fractional square part.
    p=list(map(F,[1,1,1,1,1]));c=producer.nonsquare_threshold(p)
    require(c['denominator']==8,'fractional square-part control')
    for n in (c['threshold'],c['threshold']+1):
        z=evaluation(p,n);require(isqrt(z.numerator)**2!=z,'fractional threshold')
    def reject(fn):
        try:fn()
        except ValueError:counts['rejections']+=1
        else:raise ValueError('negative control accepted')
    for bad in [[],[[1,0],[1,1]],[[0,0],[0,1]],[[1,2],[2,1]],[[1.0,0],[0,1]]]:
        reject(lambda b=bad:producer.construct([b]))
    reject(lambda:producer.construct([[[1,0],[0,1]]],0))
    reject(lambda:producer.Field([-1,-4]))
    reject(lambda:producer.Field([2]))
    for p in ([1,0,1,1],[1,2,1],[1,0,2]):reject(lambda p=p:producer.nonsquare_threshold(p))
    reject(lambda:check_matrix([[F(1),F(0)],[F(0),F(3)]],[[F(1),F(0)],[F(0),F(1)]],F(2)))
    result=normalize({'status':'pass','counts':counts,'suites':output,
                      'fractional_square_part_control':c,
                      'explicit_example':{'squared_scale':alpha,'missed_d':2,'obstruction_prime':13},
                      'fixture_sha256':sha256(path.read_bytes()).hexdigest()})
    payload=json.dumps(result,separators=(',',':'),sort_keys=True).encode()
    result['certificate_sha256']=sha256(payload).hexdigest()
    return result


if __name__=='__main__':
    result=run()
    if '--emit' not in sys.argv[1:]:
        require(result==json.loads(Path(__file__).with_name('expected.json').read_text()),'expected output mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
