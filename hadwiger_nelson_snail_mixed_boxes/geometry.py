"""Exact rational-field geometry for the Snail mixed-box certificate."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations

import field_base as F


def q(x): return tuple(Fraction(a) for a in x)
ZERO, ONE = q(F.ZERO), q(F.ONE)
POINTS = tuple(q(x) for x in F.seed())


def add(x,y): return tuple(a+b for a,b in zip(x,y))
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def scale(x,a): return tuple(a*b for b in x)
def mul(x,y): return F.mul(x,y)
def bar(x): return F.conjugate(x)
def norm(x): return mul(x,bar(x))


def inverse(x):
    """Invert a nonzero field element by exact rational elimination."""
    columns=[mul(x,q(F.basis(j))) for j in range(F.SIZE)]
    a=[[columns[j][i] for j in range(F.SIZE)]+[Fraction(i==0)]
       for i in range(F.SIZE)]
    for col in range(F.SIZE):
        pivot=next((r for r in range(col,F.SIZE) if a[r][col]),None)
        if pivot is None: raise ZeroDivisionError
        a[col],a[pivot]=a[pivot],a[col]
        z=a[col][col];a[col]=[v/z for v in a[col]]
        for r in range(F.SIZE):
            if r!=col and a[r][col]:
                z=a[r][col];a[r]=[u-z*v for u,v in zip(a[r],a[col])]
    answer=tuple(a[i][-1] for i in range(F.SIZE))
    if mul(x,answer)!=ONE: raise ArithmeticError('inverse check')
    return answer


# (translation, multiplier, conjugate-input flag), acting on scaled points.
IDENTITY=(ZERO,ONE,False)


def apply(f,z):
    a,u,flip=f
    return add(a,mul(u,bar(z) if flip else z))


def compose(f,h):
    """Return f after h."""
    a,u,flip=f;b,v,hflip=h
    if flip:return add(a,mul(u,bar(b))),mul(u,bar(v)),not hflip
    return add(a,mul(u,b)),mul(u,v),hflip


def pair_map(source,target,flip,swap):
    x0,x1=(POINTS[i] for i in source);y0,y1=(POINTS[i] for i in target)
    if swap:y0,y1=y1,y0
    dx=sub(bar(x1) if flip else x1,bar(x0) if flip else x0)
    u=mul(sub(y1,y0),inverse(dx))
    a=sub(y0,mul(u,bar(x0) if flip else x0))
    f=(a,u,flip)
    if apply(f,x0)!=y0 or apply(f,x1)!=y1 or norm(u)!=ONE:
        raise ArithmeticError('pair isometry')
    return f


@lru_cache(None)
def distance_classes():
    classes=defaultdict(list)
    for i,j in combinations(range(29),2):
        classes[norm(sub(POINTS[j],POINTS[i]))].append((i,j))
    return tuple(tuple(p) for p in classes.values() if len(p)>=2)


@lru_cache(None)
def all_generators():
    out={IDENTITY}
    for pairs in distance_classes():
        source=pairs[0]
        for target in pairs:
            for flip in (False,True):
                for swap in (False,True):out.add(pair_map(source,target,flip,swap))
    out.discard(IDENTITY)
    return tuple(sorted(out,key=repr))


@lru_cache(None)
def augmentation_generators():
    """Maps from the red and green nonedge congruences involving p or q."""
    out={IDENTITY};unit=scale(ONE,F.D*F.D)
    for pairs in distance_classes():
        if norm(sub(POINTS[pairs[0][1]],POINTS[pairs[0][0]]))==unit:continue
        if not any(0 in pair or 1 in pair for pair in pairs):continue
        source=pairs[0]
        for target in pairs:
            for flip in (False,True):
                for swap in (False,True):out.add(pair_map(source,target,flip,swap))
    out.discard(IDENTITY)
    return tuple(sorted(out,key=repr))


@lru_cache(maxsize=100000)
def cloud(f):return tuple(apply(f,x) for x in POINTS)


def overlap(f):
    base=set(POINTS)
    return sum(apply(f,x) in base for x in POINTS)


@lru_cache(None)
def high_generators():
    ranked=sorted(((overlap(t),i,t) for i,t in enumerate(all_generators())),
                  reverse=True,key=lambda z:(z[0],-z[1]))
    return tuple(ranked[:20])


def powers(t,n=31):
    out=[IDENTITY]
    for _ in range(1,n):out.append(compose(out[-1],t))
    return tuple(out)


def box(hpowers,upowers,order,long,short):
    if order not in (0,1):raise ValueError('order')
    return tuple(dict.fromkeys((compose(hpowers[i],upowers[j]) if order==0
                                else compose(upowers[j],hpowers[i]))
                               for i in range(long) for j in range(short)))


PRIME=F.PRIME


@lru_cache(maxsize=300000)
def evaluate(x):
    total=0
    for a,b in zip(x,F.RESIDUES):
        if a.denominator%PRIME==0:raise ValueError('noninvertible denominator')
        total+=(a.numerator%PRIME)*pow(a.denominator,-1,PRIME)*b
    return total%PRIME


def residue_graph(transforms):
    """Return the point set and a supergraph of all physical unit edges."""
    points=sorted({x for f in transforms for x in cloud(f)})
    values=[evaluate(x) for x in points]
    bars=[evaluate(bar(x)) for x in points]
    goal=F.D*F.D%PRIME
    edges=[(i,j) for i,j in combinations(range(len(points)),2)
           if (values[i]-values[j])*(bars[i]-bars[j])%PRIME==goal]
    return points,edges
