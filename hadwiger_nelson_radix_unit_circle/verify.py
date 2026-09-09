#!/usr/bin/env python3
"""Direct all-pair Laurent-norm checker; exact integers and modular gcds."""
import argparse
from collections import Counter
import hashlib
from itertools import product
from math import isqrt
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TRIANGLE=((0,0),(1,0),(0,1))
LABELS=tuple(product(range(3),repeat=5))
PRIMES=(7,13,19,31,37,43,61,67,73,79,97,103,109,127,139,151,157,163,181,193)


def require(ok,message):
    if not ok:raise ValueError(message)


def plus(a,b):return a[0]+b[0],a[1]+b[1]
def times(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1]
def conjugate(a):return a[0]+a[1],-a[1]
def flat(p):return tuple(x for a in p for x in a)
def unflat(p):
    require(isinstance(p,(list,tuple)) and len(p)%2==0 and all(type(x) is int for x in p),'invalid Eisenstein polynomial')
    return tuple(zip(p[::2],p[1::2]))

def multiply(p,q):
    out=[(0,0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]=plus(out[i+j],times(a,b))
    return tuple(out)


def norm_event(a,b):
    """Coefficients of z^n(|v_a-v_b|^2-1) under conjugate(z)=z^-1."""
    d=tuple((TRIANGLE[x][0]-TRIANGLE[y][0],TRIANGLE[x][1]-TRIANGLE[y][1]) for x,y in zip(a,b))
    support=[j for j,c in enumerate(d) if c!=(0,0)]
    require(bool(support),'identical label pair')
    n=support[-1]-support[0]
    if n==0:
        require(times(d[support[0]],conjugate(d[support[0]]))==(1,0),'nonunit digit difference')
        return ()
    h=[(0,0)]*(2*n+1)
    for i in support:
        for j in support:
            k=n+i-j;h[k]=plus(h[k],times(d[i],conjugate(d[j])))
    h[n]=plus(h[n],(-1,0))
    leading=h[-1]
    require(times(leading,conjugate(leading))==(1,0),'nonunit leading coefficient')
    return flat(tuple(times(c,conjugate(leading)) for c in h))


def pair_inventory():
    by_event={}
    for u in range(243):
        for v in range(u+1,243):
            h=norm_event(LABELS[u],LABELS[v]);by_event.setdefault(h,[]).append((u,v))
    require(len(by_event[()])==1215,'universal five-layer edge count')
    require(sum(map(len,by_event.values()))==29403,'label pair coverage')
    require(len(by_event)-1==1272,'event catalog count')
    return by_event


def f4mul(a,b):
    # Cayley table rather than producer bit-polynomial multiplication.
    return ((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))[a][b]


def colour_word(spec):
    if 'word' in spec:
        word=spec['word']
        require(type(word) is str and len(word)==243 and set(word)<=set('0123'),'invalid explicit word')
        return tuple(map(int,word))
    require(set(spec)=={'field','weights'},'invalid linear specification')
    q=spec['field'];w=spec['weights']
    require(q in (3,4) and len(w)==5 and all(type(c) is int and 0<c<q for c in w),'invalid linear weights')
    out=[]
    for label in LABELS:
        if q==3:c=sum(w[j]*label[j] for j in range(5))%3
        else:
            c=0
            for j in range(5):c^=f4mul(w[j],label[j])
        out.append(c)
    return tuple(out)


def pgcd(a,b,p):
    a=list(a);b=list(b)
    while a and a[-1]==0:a.pop()
    while b and b[-1]==0:b.pop()
    while b:
        r=a[:];inv=pow(b[-1],-1,p)
        while len(r)>=len(b):
            k=len(r)-len(b);c=r[-1]*inv%p
            for j,t in enumerate(b):r[k+j]=(r[k+j]-c*t)%p
            while r and r[-1]==0:r.pop()
        a,b=b,r
    return a


def prime_roots():
    out=[]
    for p in PRIMES:
        require(p>=2 and all(p%d for d in range(2,isqrt(p)+1)),'nonprime modulus')
        r=next(x for x in range(p) if (x*x-x+1)%p==0)
        out.append((p,r))
    return out


def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()


def verify(c):
    require(c.get('schema')=='hn-radix-unit-circle-v1','schema')
    events=pair_inventory();hs=sorted(h for h in events if h)
    require(c['event_sha256']==digest(hs),'event digest')
    factors=[unflat(f) for f in c['factors']]
    require(len(set(factors))==len(factors) and factors==sorted(factors),'factor order or duplicate')
    for f in factors:
        require(2<=len(f)<=9 and f[-1]==(1,0),'nonmonic or wrong-degree factor')
    parts=c['factorizations']
    require(len(parts)==len(hs),'missing factorization')
    used=set()
    for h,part in zip(hs,parts):
        got=((1,0),)
        require(bool(part),'empty factorization')
        for i,e in part:
            require(type(i) is int and 0<=i<len(factors) and type(e) is int and 1<=e<=8,'factor index/exponent')
            used.add(i)
            for _ in range(e):got=multiply(got,factors[i])
        require(flat(got)==h,'factor product identity')
    require(used==set(range(len(factors))),'unused factor')
    words=[colour_word(s) for s in c['colour_specs']]
    require(all(set(w)<=set(range(3)) for w in words),'three-colour theorem requires three-colour words')
    bad=[]
    for word in words:
        require(all(word[u]!=word[v] for u,v in events[()]),'monochromatic universal edge')
        bad.append(tuple(i for i,h in enumerate(hs) if any(word[u]==word[v] for u,v in events[h])))
    cover=c['factor_cover']
    require(len(cover)==len(factors),'missing block cover')
    maps=prime_roots();H=[unflat(h) for h in hs]
    reductions=[[[int(a+b*r)%p for a,b in h] for h in H] for p,r in maps]
    checks=Counter();low=0;high=0;maxdeg=0
    for f,k in zip(factors,cover):
        d=len(f)-1
        if k==-1:
            require(d<=4,'h4119 degree condition');low+=1;continue
        require(type(k) is int and 0<=k<len(words),'invalid colour reference')
        high+=1;maxdeg=max(maxdeg,d)
        fs=[[(a+b*r)%p for a,b in f] for p,r in maps]
        for j in bad[k]:
            for t,(p,r) in enumerate(maps):
                if len(pgcd(fs[t],reductions[t][j],p))==1:
                    checks[p]+=1;break
            else:raise ValueError('no modular coprimality certificate for factor/event '+str((flat(f),j)))
    generic=colour_word({'field':3,'weights':[1,1,1,1,1]})
    require(all(generic[u]!=generic[v] for u,v in events[()]),'generic colouring')
    return {'verified':True,'unit_circle_chromatic_number':3,'unit_circle_four_colourability_closed':True,'record_improvement':False,
            'label_vertices':243,'label_pairs':29403,'universal_edges':1215,'event_polynomials':len(hs),
            'event_degree_histogram':dict(sorted(Counter(len(h)//2-1 for h in hs).items())),
            'event_sha256':digest(hs),'factor_polynomials':len(factors),
            'factor_degree_histogram':dict(sorted(Counter(len(f)-1 for f in factors).items())),
            'factor_degree_sum':sum(len(f)-1 for f in factors),
            'factor_product_identities':len(parts),'h4119_blocks':low,'colour_blocks':high,
            'colour_words':len(words),'maximum_block_degree':maxdeg,
            'modular_coprimality_checks':sum(checks.values()),'modular_witness_prime_histogram':dict(sorted(checks.items())),
            'certificate_sha256':hashlib.sha256((json.dumps(c,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest(),
            'external_reviewer_acceptance_claimed':False}


def json_normalize(x):return json.loads(json.dumps(x))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=ROOT/'certificate.json');ap.add_argument('--check-expected',action='store_true');a=ap.parse_args()
    result=json_normalize(verify(json.loads(a.certificate.read_text())))
    if a.check_expected:require(result==json.loads((ROOT/'EXPECTED.json').read_text()),'expected output mismatch')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
