"""Exact shared definitions; computation paths use different norm expansions."""
from fractions import Fraction
from itertools import product
from math import gcd,lcm
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('prior_exact_polynomials',HERE.parent/'hadwiger_nelson_radix_reflection_axes/exact.py')
X=importlib.util.module_from_spec(spec);spec.loader.exec_module(X)
LABELS=tuple(product(range(3),repeat=5))
WEIGHTS=tuple((1,)+tail for tail in product(range(3),repeat=4))
UNITS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
H=[1,0,3]


def primitive(values):
    values=X.trim(values)
    if not values:return ()
    den=lcm(*(Fraction(v).denominator for v in values))
    ints=[int(v*den) for v in values]
    content=gcd(*ints)
    if ints[-1]<0:content=-content
    return tuple(v//content for v in ints)


def quotient(numerator,denominator):
    a=list(map(Fraction,numerator));b=list(map(Fraction,denominator))
    out=[Fraction(0)]*max(0,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        offset=len(a)-len(b);scale=a[-1]/b[-1];out[offset]+=scale
        for i,v in enumerate(b):a[offset+i]-=scale*v
        a=X.trim(a)
    X.need(not a,'exact rational polynomial quotient')
    return X.trim(out)


def powers(poly,n):
    result=[[1]]
    for _ in range(n):result.append(X.mul(result[-1],poly))
    return result


def bivariate_pull(f,sign):
    degree=max(i+j for i,j,c in f)
    X.need(degree in (2,4,6,8),'even norm-curve degree')
    xp=powers([0,0,-6*sign],degree);yp=powers([0,2*sign],degree);hp=powers(H,degree)
    numerator=[]
    for i,j,c in f:
        term=X.mul(X.mul(xp[i],yp[j]),hp[degree-i-j])
        numerator=X.add(numerator,term,c)
    return primitive(quotient(numerator,hp[degree//2]))


def e_mul(a,b):
    return X.add(X.mul(a[0],b[0]),X.mul(a[1],b[1]),-1),X.add(X.add(X.mul(a[0],b[1]),X.mul(a[1],b[0])),X.mul(a[1],b[1]))


def real_denominator_row(row,sign):
    # z=sign*((-6t^2-2t)+4t*omega)/(1+3t^2).
    n=([0,-2*sign,-6*sign],[0,4*sign]);np=[([1],[])];hp=powers(H,4)
    for _ in range(4):np.append(e_mul(np[-1],n))
    k=max(j for j,d in enumerate(row) if d!=(0,0));out=([],[])
    for j,(a,b) in enumerate(row[:k+1]):
        term=e_mul(([a],[b]),np[j]);term=tuple(X.mul(t,hp[k-j]) for t in term)
        out=tuple(X.add(x,y) for x,y in zip(out,term))
    return out


def check_collision(row,block,sign):
    row=tuple(map(tuple,row))
    X.need(len(row)==5 and any(a!=(0,0) for a in row) and all(a==(0,0) or a in UNITS for a in row),'actual digit-difference collision row')
    a,b=real_denominator_row(row,sign)
    X.need(not X.rem(a,block) and not X.rem(b,block),'both exact coordinate numerators vanish on the block')


def root_audit(blocks,roots):
    X.need(all(X.is_prime(p) for p in X.PRIMES),'proof moduli prime')
    X.need(len(blocks)==len(roots),'one root count per block')
    for q,n in zip(blocks,roots):X.need(type(n)is int and n==X.root_count(q),'exact rational Sturm count')


def summarize(cert,specializations,audit):
    from collections import Counter
    blocks=cert['blocks'];roots=cert['real_root_counts'];coll={r['block_id'] for r in cert['collision_witnesses']}
    return {'event_curves':2797,'representative_anchor_curves':[q.index(()) for q in specializations],
            'unique_nonzero_restricted_polynomials':len(set(specializations[0])-{()}),
            'primitive_blocks':len(blocks),'degree_histogram':{str(k):n for k,n in sorted(Counter(len(q)-1 for q in blocks).items())},
            'blocks_with_real_roots':sum(n>0 for n in roots),'distinct_finite_real_event_parameters_per_representative':sum(roots),
            'nonreal_blocks':sum(n==0 for n in roots),'blocks_closed_by_collision_witness':len(coll),
            'real_parameters_closed_by_collision_witness':sum(roots[i] for i in coll),
            'colour_word_blocks_per_representative':[sum(v is not None for v in cs) for cs in cert['colour_assignments']],
            'used_colour_words':[[list(w) for w in sorted({WEIGHTS[v] for v in cs if v is not None})] for cs in cert['colour_assignments']],
            'coprimality':audit,'all_six_anchor_loci_chromatic_number':3,'maximum_physical_order':243,
            'complete_architecture_closed':False,'record_improvement':False}
