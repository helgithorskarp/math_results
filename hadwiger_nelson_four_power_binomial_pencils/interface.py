"""Exact A5 norms and all homogeneous four-position pencils containing binomials."""
import itertools
import json
from pathlib import Path
import sys
import pins

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'hadwiger_nelson_radix_c0_physical_star'
sys.path.insert(0,str(OLD))
import algebra as A
import physical
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
    pins.verify()
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
    return factors,owners,base,buckets,curve_rows


def generate_pencils():
    """All357 two-dimensional row spaces, by unique rank-two RREF matrices."""
    spaces=[];selected=[]
    for p,q in itertools.combinations(range(4),2):
        free=[(i,j) for i,pivot in enumerate((p,q)) for j in range(pivot+1,4) if j not in (p,q)]
        for values in itertools.product(range(4),repeat=len(free)):
            rows=[[0]*4 for _ in range(2)];rows[0][p]=rows[1][q]=1
            for (i,j),v in zip(free,values):rows[i][j]=v
            pencil=span((tuple(rows[0]),0),(tuple(rows[1]),0));spaces.append(pencil)
            if min(sum(v!=0 for v in n) for n,c in pencil)==2 and all(any(n[k] for n,c in pencil) for k in range(4)):selected.append(pencil)
    A.need(len(spaces)==len(set(spaces))==357,'all rank-two RREF spaces')
    A.need(len(selected)==189,'all four-position binomial pencils')
    return sorted(selected)


def selection(buckets,residual=None):
    records=json.loads((HERE/'PENCILS.json').read_text());pencils=[]
    for idx,p in records:
        p=tuple((tuple(n),c) for n,c in p)
        A.need(p==tuple(sorted(p)) and len(set(p))==5 and all(c==0 for n,c in p),'homogeneous five sections')
        A.need(all(sig in buckets for sig in p) and span(p[0],p[1])==p,'full affine pencil')
        A.need(sorted(len(buckets[s]) for s in p) in ([2,4,4,8,8],[2,2,8,8,8]),'complete unit lift buckets')
        pencils.append((idx,p))
    A.need([i for i,p in pencils]==list(range(189)),'intrinsic canonical indices')
    A.need(sorted(p for i,p in pencils)==generate_pencils(),'entire intrinsic binomial family')
    if residual:
        source=json.loads(Path(residual).read_text())
        A.need(A.digest(source)==A.RESIDUAL_HASH,'pinned h4195 residual')
        known={p for i,p in pencils}
        expected=[[i,p] for i,p in enumerate(source['remaining_pencil_signatures']) if tuple((tuple(n),c) for n,c in p) in known]
        A.need(expected==json.loads((HERE/'RESIDUAL.json').read_text()),'entrywise residual intersection')
    residual_records=json.loads((HERE/'RESIDUAL.json').read_text())
    A.need(len(residual_records)==162,'retained residual members')
    named=next(p for i,p in residual_records if i==412)
    named=tuple((tuple(n),c) for n,c in named)
    A.need(named in {p for i,p in pencils},'named asymmetric pencil412')
    return pencils


def pair_interface(pencils,buckets):
    selected=[]
    for idx,p in pencils:
        domains=sorted([buckets[sig] for sig in p],key=lambda d:(len(d),d))
        pairs=sorted({tuple(sorted(pair)) for pair in itertools.product(*domains[:2])})
        selected.append((idx,domains,pairs))
    all_pairs=sorted({pair for idx,ds,pairs in selected for pair in pairs})
    A.need(len(all_pairs)==1404,'complete anchor envelope')
    return selected,all_pairs


def linear_weights(active,curve_rows):
    # First try nonzero weights; off the unit circle, zero weights are allowed.
    choices=[(1,2)] if 342 in active else [(1,2),(0,1,2)]
    for values in choices:
        for tail in itertools.product(values,repeat=4):
            w=(1,)+tail
            if all(sum(w[k]*(a-b) for k,(a,b) in enumerate(curve_rows[i]))%3 for i in active if i in curve_rows):return list(w)
    raise ValueError('no linear three-colouring; investigate')


def colour_word(weights,labels,n):
    A.need(len(weights)==5 and weights[0]==1 and all(type(t)==int and t in (0,1,2) for t in weights),'linear colour weights')
    word=[None]*n
    for label,p in zip(itertools.product(range(3),repeat=5),labels):
        c=sum(w*t for w,t in zip(weights,label))%3
        A.need(word[p] is None or word[p]==c,'colour descends through collisions')
        word[p]=c
    A.need(None not in word,'all physical points coloured')
    return word
