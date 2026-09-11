#!/usr/bin/env python3
"""Exact whole-endpoint replay. Python 3.11+, standard library only; no -O."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import json
import model as M

DATA=json.loads(Path(__file__).with_name('certificates.json').read_text())

@lru_cache(None)
def maps(s):
    return tuple(tuple(sum(1<<order[j] for j in range(s) if B>>j&1)
                       for B in range(1<<s)) for order in permutations(range(s)))

def canonical(x):
    s=(len(x)-1).bit_length()
    return min(tuple(x[A] for A in mp) for mp in maps(s))

EXTRA={}
for c in DATA['noncentral_five_anchor_certificates']:
    x=tuple(c['counts']);pos=tuple(c['positions'])
    assert len(x)==32 and sum(x)==32 and min(x)>=0 and x==canonical(x)
    a,b=M.bound(c['v'],x,positions=pos)
    assert (a,b)==(c['numerator'],c['denominator']) and a<b
    EXTRA[c['v'],x]=pos


def star(v,m,d):
    """Pair-covered vertex; discard edge pairs sharing another vertex."""
    den,cs=M.coefficients(v,1)
    M.CONFIGURATIONS.add((v,1,5,None))
    x=(m-d,d);total=0
    missed=2*((4*d-(v-1)+2)//3)
    assert missed>=0
    for one,two,pairs,mark,L,R in cs:
        a=sum(x[A]*c for A,c in one)
        b=sum(x[A]*c for A,c in two)
        q=sum(x[A]*(x[B]-(A==B))*c for A,B,c in pairs)
        if mark:
            q-=missed*next(c for A,B,c in pairs if A==B==1)
        assert q>=0
        total+=min(a,b,q,den)
    return Fraction(total,den)

@lru_cache(None)
def good(v,x):
    s=(len(x)-1).bit_length()
    if s>1:
        for omitted in range(s):
            order=tuple(i for i in range(s) if i!=omitted)
            if good(v,M.reindex(x,order)):return True
    for order in permutations(range(s)):
        a,b=M.bound(v,M.reindex(x,order))
        if a<b:return True
    if s==5:
        y=canonical(x)
        if (v,y) in EXTRA:
            a,b=M.bound(v,y,positions=EXTRA[v,y]);assert a<b
            return True
    return False


def admissible(v,x):
    s=(len(x)-1).bit_length();N=v-s
    if any(n and A.bit_count()>5 for A,n in enumerate(x)):return False
    for i in range(s):
        if sum(n*(5-A.bit_count()) for A,n in enumerate(x) if A>>i&1)<N:return False
        for j in range(i):
            if sum(n for A,n in enumerate(x) if A>>i&1 and A>>j&1)<1:return False
    if sum(n*comb(5-A.bit_count(),2) for A,n in enumerate(x)
           if A.bit_count()<=3)<comb(N,2):return False
    return True


def finite_cases(v):
    seen=Counter();closed=Counter();lifts=Counter()
    def visit(x):
        s=(len(x)-1).bit_length();seen[s]+=1
        if good(v,x):closed[s]+=1;return
        assert s<5, ('UNRESOLVED',v,x)
        ds=[sum(n for A,n in enumerate(x) if A>>i&1) for i in range(s)]
        for d in range(ds[-1],(160-sum(ds))//(v-s)+1):
            for y in M.extends(x,d):
                lifts[s+1]+=1
                if admissible(v,y):visit(y)
    for x in M.profiles(v,32,3):visit(x)
    return {'v':v,'visited':dict(sorted(seen.items())),
            'closed_by_coloring':dict(sorted(closed.items())),
            'raw_lifts':dict(sorted(lifts.items()))}


def pair_partitions(s=6):
    pairs=list(combinations(range(s),2));idx={p:i for i,p in enumerate(pairs)}
    blocks=[]
    for k in range(2,6):
        for c in combinations(range(s),k):
            blocks.append((sum(1<<idx[p] for p in combinations(c,2)),
                           sum(1<<i for i in c)))
    choices=[[b for b in blocks if b[0]>>i&1] for i in range(len(pairs))]
    out=[]
    def rec(rem,chosen):
        if rem==0:out.append(tuple(sorted(chosen)));return
        i=(rem&-rem).bit_length()-1
        for covered,mask in choices[i]:
            if covered&rem==covered:rec(rem^covered,chosen+[mask])
    rec((1<<len(pairs))-1,[])
    assert len(out)==len(set(out))
    return set(out)


def trace(blocks):
    x=[0]*64
    for A in blocks:x[A]+=1
    for i in range(6):x[1<<i]=6-sum(1 for A in blocks if A>>i&1)
    x[0]=32-sum(x)
    assert min(x)>=0 and sum(x)==32
    return tuple(x)


def case25():
    parts=pair_partitions();types={canonical(trace(p)) for p in parts}
    cert={tuple(r['x']):r for r in DATA['six_anchor_types']}
    assert set(cert)==types
    bad=[]
    for x,row in sorted(cert.items()):
        assert x==canonical(x)
        a,b=M.bound(25,x,positions=tuple(row['positions']))
        assert Fraction(a,b)==Fraction(row['bound'])
        if row['closed']:assert a<b
        else:
            large=[A for A,n in enumerate(x) if n and A.bit_count()>=3]
            assert len(large)==2 and all(A.bit_count()==3 and x[A]==1 for A in large)
            assert large[0]&large[1]==0 and large[0]|large[1]==63
            bad.append(x)
    assert len(bad)==1
    # The proof explains why every six-subset of seven minimum-degree vertices
    # would have two triples and no larger trace, forcing 4*T=7*2.
    assert (7*2)%4!=0
    return {'labeled_pair_partitions':len(parts),'trace_isomorphism_types':len(types),
            'types_closed_by_coloring':len(types)-len(bad),
            'remaining_type':'two disjoint triples','seven_vertex_identity':'4*T=14, impossible'}


def main():
    # A pair-covered 32-edge quotient has at most 25 vertices.
    assert comb(26,2)>32*comb(5,2)
    for v in range(9,19):
        assert 32*(comb(v//2,5)+comb((v+1)//2,5))<comb(v,5)
    small=[]
    for v in [19,20,21]:
        values=[star(v,32,d) for d in range((v+2)//4,160//v+1)]
        assert max(values)<1
        small.append({'v':v,'max_failure_bound':str(max(values))})
    middle=[finite_cases(v) for v in [22,23,24]]
    last=case25()
    from audit import audit_coefficients,audit_pair_partitions,audit_small_controls
    checks={'coefficient_configurations':audit_coefficients(M.CONFIGURATIONS),
            'independent_pair_partitions':audit_pair_partitions(pair_partitions()),
            'small_controls':audit_small_controls()}
    result={'theorem':'Every finite simple 5-uniform hypergraph with at most 32 edges has Property B.',
            'lower_bound_m5':33,'known_upper_bound_m5':51,'small_vertex_cases':small,
            'middle_vertex_cases':middle,'case25':last,'checks':checks}
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: assertions are part of this verifier.')
    main()
