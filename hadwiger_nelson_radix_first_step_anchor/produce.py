#!/usr/bin/env python3
"""FLINT coefficient-norm producer and exact factor/colour certificate."""
import argparse
from collections import Counter
from itertools import combinations
import hashlib,json,sys
from pathlib import Path
import flint
import sympy as S
import common as C
X=C.X
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hadwiger_nelson_complex_radix_architecture'))
import geometry as G


def inventory():
    rows,edges=G.inventory();circle=G.primitive({(2,0):1,(0,2):3,(0,0):-1})
    eventrows={G.distance_event(r):r for r in rows if sum(d!=(0,0) for d in r)>1}
    factors=sorted(list(eventrows)+[circle]);byid={i:eventrows[f] for i,f in enumerate(factors) if f!=circle}
    return factors,factors.index(circle),byid


def restrictions(byid,circle,sign):
    F=flint.fmpz_poly;one=F([1]);zero=F([])
    def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1]
    numerator=(F([0,-2]),F([0,4]));denominator=(F([1,1]),F([0,-2]));np=[(one,zero)];dp=list(np)
    for _ in range(4):np.append(mul(np[-1],numerator));dp.append(mul(dp[-1],denominator))
    realden=F(C.H);qs=[None]*2797;qs[circle]=(-1,0,9);collision={}
    for curve,row in byid.items():
        k=max(j for j,d in enumerate(row) if d!=(0,0));a,b=zero,zero
        for j,(u,v) in enumerate(row[:k+1]):
            term=mul(mul(np[j],dp[k-j]),(F([u*sign**j]),F([v*sign**j])));a+=term[0];b+=term[1]
        q=a*a+a*b+b*b-realden**k;qs[curve]=C.primitive(list(map(int,q)))
        g=a.gcd(b)
        if g.degree()>0:
            for f,e in g.factor()[1]:collision.setdefault(C.primitive(list(map(int,f))),row)
    return qs,collision


def modular_audit(blocks,roots):
    tables={p:[flint.nmod_poly(q,p) for q in blocks] for p in X.PRIMES}
    hist=Counter();trace=hashlib.sha256();real=[i for i,n in enumerate(roots) if n]
    for i,j in combinations(real,2):
        for p in X.PRIMES:
            if blocks[i][-1]%p and blocks[j][-1]%p and tables[p][i].gcd(tables[p][j]).degree()==0:
                hist[p]+=1;trace.update(f'{i},{j},{p}\n'.encode());break
        else:raise ValueError('real-root block coprimality')
    sf=[next(p for p in X.PRIMES if q[-1]%p and tables[p][i].gcd(tables[p][i].derivative()).degree()==0) for i,q in enumerate(blocks)]
    return {'real_block_pair_checks':sum(hist.values()),'prime_histogram':{str(p):n for p,n in sorted(hist.items())},
            'pair_trace_sha256':trace.hexdigest(),'squarefree_primes_sha256':X.digest(sf)}


def produce():
    factors,circle,byid=inventory();data=[restrictions(byid,circle,s) for s in (1,-1)];qs=[d[0] for d in data]
    X.need(set(qs[0])==set(qs[1]),'two signs have the same polynomial inventory')
    unique=sorted(set(qs[0])-{()});blocks=set();dec={}
    for q in unique:
        scalar,fs=flint.fmpz_poly(list(q)).factor();terms=[(C.primitive(list(map(int,g))),int(e)) for g,e in fs]
        dec[q]=(int(scalar),terms);blocks.update(g for g,e in terms)
    blocks=sorted(blocks);ids={g:i for i,g in enumerate(blocks)};t=S.Symbol('t')
    roots=[int(S.Poly.from_list(list(reversed(q)),t).count_roots(-S.oo,S.oo)) for q in blocks]
    collided={i for i,g in enumerate(blocks) if roots[i] and all(g in d[1] for d in data)}
    bad={c:[i for i,w in enumerate(C.WEIGHTS) if not sum(a*((b-d)%3) for a,(b,d) in zip(w,row))%3] for c,row in byid.items()}
    bad[circle]=[i for i,w in enumerate(C.WEIGHTS) if not all(w)]
    colourings=[]
    for si,sign in enumerate((1,-1)):
        anchor=qs[si].index(());events=[{anchor} for g in blocks]
        for c,q in enumerate(qs[si]):
            if q:
                for g,e in dec[q][1]:events[ids[g]].add(c)
        colours=[]
        for i in range(len(blocks)):
            if not roots[i] or i in collided:colours.append(None);continue
            forbidden=set().union(*(bad[c] for c in events[i]));good=[k for k in range(len(C.WEIGHTS)) if k not in forbidden]
            X.need(good,'three-colour gate succeeds for every real block');colours.append(good[0])
        colourings.append(colours)
    cert={'schema':'hn-radix-first-anchor-v1','curve_inventory_sha256':X.digest(factors),'restriction_inventory_sha256':X.digest(unique),
          'blocks':blocks,'factorizations':[[dec[q][0],[[ids[g],e] for g,e in dec[q][1]]] for q in unique],
          'real_root_counts':roots,'colour_assignments':colourings,
          'collision_witnesses':[{'block_id':i,'rows':[d[1][blocks[i]] for d in data]} for i in sorted(collided)]}
    # FLINT may order factors differently; canonicalize the compact multiplicities.
    for scalar,terms in cert['factorizations']:terms.sort()
    audit=modular_audit([list(q) for q in blocks],roots);cert['result']=C.summarize(cert,qs,audit)
    return cert


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    cert=produce()
    with args.out.open('x') as f:json.dump(cert,f,sort_keys=True,separators=(',',':'));f.write('\n')
    print(json.dumps(cert['result'],indent=2,sort_keys=True))
