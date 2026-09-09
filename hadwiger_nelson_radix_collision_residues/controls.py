#!/usr/bin/env python3
"""Malformed certificate controls and exact physical collision fixtures."""
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
from verify import Quotient, ROOT, require, verify


def rejects(fn):
    try:
        fn()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError('malformed input was accepted')


def eadd(a,b):
    return (a[0]+b[0],a[1]+b[1])


def emul(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])


def econj(a):
    return (a[0]+a[1],-a[1])


def physical_fixtures():
    T=((0,0),(1,0),(0,1))
    out=[]
    for name,z in [('zero',(0,0)),('one',(1,0)),('omega',(0,1))]:
        powers=[(1,0)]
        for _ in range(4):
            powers.append(emul(powers[-1],z))
        vertices=set()
        for label in product(T,repeat=5):
            p=(0,0)
            for t,power in zip(label,powers):
                p=eadd(p,emul(t,power))
            vertices.add(p)
        V=sorted(vertices);col=[(a-b)%3 for a,b in V];edges=0
        for i,a in enumerate(V):
            for j in range(i+1,len(V)):
                b=V[j];delta=(a[0]-b[0],a[1]-b[1])
                if emul(delta,econj(delta))==(1,0):
                    require(col[i]!=col[j], 'monochromatic Eisenstein fixture')
                    edges+=1
        out.append({'z':name,'labels':243,'physical_vertices':len(V),'unit_edges':edges,'colours':len(set(col))})
    # z=(1+sqrt(5))/2, a real root of z²-z-1. Basis 1,z over E is exact:
    # sqrt(5) is not in Q(sqrt(-3)). Tuples below hold the two E coefficients.
    zero=((0,0),(0,0));one=((1,0),(0,0));z=((0,0),(1,0))
    def add(a,b):return tuple(eadd(x,y) for x,y in zip(a,b))
    def multiply(a,b):
        c0=emul(a[0],b[0]);c1=eadd(emul(a[0],b[1]),emul(a[1],b[0]));c2=emul(a[1],b[1])
        return (eadd(c0,c2),eadd(c1,c2))
    powers=[one]
    for _ in range(4):powers.append(multiply(powers[-1],z))
    points=set()
    for label in product(T,repeat=5):
        v=zero
        for t,p in zip(label,powers):v=add(v,multiply((t,(0,0)),p))
        points.add(v)
    F=Quotient([1,0,1])
    alpha=next(a for a in range(9) if F.minus(F.minus(F.times(a,a),a),1)==0)
    def residue(v):
        a,b=[(x-y)%3 for x,y in v]
        neg_b=(3-b)%3
        return F.minus(a,F.times(neg_b,alpha))
    V=sorted(points);col=[F.vectors[residue(v)][0] for v in V];edges=0
    for i,a in enumerate(V):
        for j in range(i+1,len(V)):
            b=V[j];delta=tuple((x[0]-y[0],x[1]-y[1]) for x,y in zip(a,b))
            if multiply(delta,tuple(econj(x) for x in delta))==one:
                require(col[i]!=col[j], 'monochromatic golden fixture')
                edges+=1
    out.append({'z':'positive_golden_root','labels':243,'physical_vertices':len(V),'unit_edges':edges,'colours':len(set(col))})
    require(all(r['physical_vertices']<243 and r['colours']==3 for r in out), 'fixture scope')
    return out


def main():
    cert=json.loads((ROOT/'certificate.json').read_text())
    verify(cert)
    mutations=[]
    x=deepcopy(cert);x['graphs'].pop('norm81');mutations.append(x)
    x=deepcopy(cert);x['graphs']['norm81']['weights']=[0,0,0,0];mutations.append(x)
    x=deepcopy(cert);x['graphs']['norm81']['colour_word']='0'*81;mutations.append(x)
    x=deepcopy(cert);x['graphs']['norm81']['weights']=[0,0,0,0];x['graphs']['norm81']['colour_word']='0'*81;mutations.append(x)
    x=deepcopy(cert);x['graphs']['norm81']['edge_sha256']='0'*64;mutations.append(x)
    x=deepcopy(cert);x['graphs']['hyperbola81']['connection'].pop();mutations.append(x)
    x=deepcopy(cert);x['graphs']['hyperbola81']['modulus_low_first']=[2,0,1];mutations.append(x)
    x=deepcopy(cert);x['graphs']['hyperbola81']['colour_word']=x['graphs']['hyperbola81']['colour_word'][:-1];mutations.append(x)
    for x in mutations:rejects(lambda x=x:verify(x))
    rejects(lambda:Quotient([2,0,1])) # X²-1 is reducible.
    # Directly require the small grid lemma to reject a functional zero on i.
    F=Quotient([1,0,1])
    rejects(lambda:require(all(F.vectors[a][0]%3 for a in [1,2,3,6]), 'bad grid functional'))
    print(json.dumps({'verified':True,'rejected_controls':len(mutations)+2,
                      'physical_fixtures':physical_fixtures()},sort_keys=True,indent=2))


if __name__=='__main__':
    main()
