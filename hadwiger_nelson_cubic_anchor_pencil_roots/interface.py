"""Pinned A5 norm curves and the fifty residual cubic-anchor pencils."""
import itertools
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'hadwiger_nelson_radix_c0_physical_star'
sys.path.insert(0,str(OLD))
import algebra as A
import physical
ANCHOR=((0,0,1,0),1)
CURVE_SHA='85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9'


def gf_mul(a,b):
    out=0
    while b:
        if b&1:out^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return out


def canonical(n,c):
    pivot=next(t for t in n if t)
    inv=next(a for a in (1,2,3) if gf_mul(a,pivot)==1)
    return tuple(gf_mul(inv,t) for t in n),gf_mul(inv,c)


def span(left,right):
    return tuple(sorted({canonical(tuple(gf_mul(a,u)^gf_mul(b,v) for u,v in zip(left[0],right[0])),gf_mul(a,left[1])^gf_mul(b,right[1])) for a,b in ((1,0),(0,1),(1,1),(1,2),(1,3))}))


def build():
    rows,events,factors,owners,base,*_=A.architecture.build()
    A.need(A.digest(factors)==CURVE_SHA,'pinned curve inventory')
    lookup={f:i for i,f in enumerate(factors)};buckets={};curve_rows={}
    for row,event in zip(rows,events):
        if not event or sum(c!=(0,0) for c in row)==1:continue
        residue=lambda c:(c[0]%2)+2*(c[1]%2)
        sig=canonical(tuple(residue(c) for c in row[1:]),residue(row[0]))
        i=lookup[event];buckets.setdefault(sig,[]).append(i);curve_rows[i]=row
    for sig in buckets:buckets[sig]=sorted(buckets[sig])
    A.need(len(buckets)==336 and len(curve_rows)==2796,'noncircle curve signatures')
    A.need(set(curve_rows)==set(range(len(factors)))-{342},'only the radial circle has no nonmonomial row')
    A.need(A.geometry.distance_event(((0,0),(1,0),(0,0),(0,0),(0,0)))==factors[342],'circle event ID')
    A.need(buckets[ANCHOR]==[2795,2796],'cubic anchor IDs')
    named={A.geometry.distance_event(((1,0),(0,0),(0,0),(t,0),(0,0))) for t in (1,-1)}
    A.need(named=={factors[i] for i in buckets[ANCHOR]},'unit events |1 +/- z^3|=1')
    return factors,owners,base,buckets,curve_rows


def selection(buckets,residual=None):
    records=json.loads((HERE/'PENCILS.json').read_text())
    if residual:
        source=json.loads(Path(residual).read_text())
        A.need(A.digest(source)==A.RESIDUAL_HASH,'pinned h4195 residual')
        exact=[[i,p] for i,p in enumerate(source['remaining_pencil_signatures']) if [list(ANCHOR[0]),ANCHOR[1]] in p]
        A.need(records==exact,'entrywise complete residual cubic-anchor class')
    pencils=[]
    for idx,p in records:
        p=tuple((tuple(n),c) for n,c in p)
        A.need(p==tuple(sorted(p)) and len(set(p))==5 and ANCHOR in p,'five named sections')
        A.need(all(sig in buckets for sig in p) and span(p[0],p[1])==p,'full affine pencil')
        pencils.append((idx,p))
    A.need([i for i,p in pencils]==list(range(192,242)),'fifty named residual indices')
    A.need(sum(__import__('math').prod(len(buckets[sig]) for sig in p) for i,p in pencils)==1024000,'raw lifted systems')
    A.need(asymmetry_images(pencils)==[230,219,207,218,206,231],
           'asymmetric starting pencil and its six D3 images')
    return pencils


def asymmetry_images(pencils):
    lookup={p:i for i,p in pencils};p=next(p for i,p in pencils if i==230);images=[]
    for reflect in (False,True):
        for rotation in range(3):
            image=[]
            for normal,constant in p:
                coeff=(constant,)+normal
                if reflect:coeff=tuple((0,1,3,2)[t] for t in coeff)
                out=[]
                for k,t in enumerate(coeff):
                    for _ in range(rotation*k):t=gf_mul(t,3)
                    out.append(t)
                image.append(canonical(tuple(out[1:]),out[0]))
            images.append(lookup[tuple(sorted(image))])
    return images


def pair_interface(pencils,buckets):
    selected=[]
    for idx,p in pencils:
        domains=sorted([buckets[sig] for sig in p],key=lambda d:(len(d),d))
        pairs=sorted({tuple(sorted(pair)) for pair in itertools.product(*domains[:2])})
        A.need(all(2795 in pair or 2796 in pair for pair in pairs),'every anchor pair contains cubic event')
        selected.append((idx,domains,pairs))
    all_pairs=sorted({pair for idx,ds,pairs in selected for pair in pairs})
    A.need(len(all_pairs)==584,'complete anchor envelope')
    return selected,all_pairs


def linear_weights(active,curve_rows):
    for tail in itertools.product((1,2),repeat=4):
        w=(1,)+tail
        if all(sum(w[k]*(a-b) for k,(a,b) in enumerate(curve_rows[i]))%3 for i in active if i in curve_rows):return list(w)
    raise ValueError('no linear three-colouring; investigate')


def colour_word(weights,labels,n):
    A.need(len(weights)==5 and weights[0]==1 and all(type(t)==int and t in (1,2) for t in weights),'linear colour weights')
    word=[None]*n
    for label,p in zip(itertools.product(range(3),repeat=5),labels):
        c=sum(w*t for w,t in zip(weights,label))%3
        A.need(word[p] is None or word[p]==c,'colour descends through collisions')
        word[p]=c
    A.need(None not in word,'all physical points coloured')
    return word
