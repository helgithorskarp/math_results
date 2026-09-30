"""Separate QQ[t] algebra audit: direct coordinate table and permutation Cramer determinants.

The certificate and written convex-polytope/cap argument are shared. This is
arithmetic validation, not independent mathematical review or formalization.
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache, reduce
from itertools import combinations, permutations
from math import comb, gcd, lcm
import argparse, json, sys
import sympy as s
from sympy.polys.rings import ring
import check

R,t = ring('t',s.QQ)
Z,O,S = R.zero,R.one,1+t
HERE = Path(__file__).resolve().parent

def need(q,message):
    if not q:raise ValueError(message)

def qq(x):
    x=Q(x);return s.QQ(x.numerator)/s.QQ(x.denominator)

def native(cs):
    return R.from_dict({(i,):qq(x) for i,x in enumerate(cs) if x})

def coefficients(p):
    return tuple(Q(c.numerator,c.denominator) for k in range(p.degree()+1)
                 for c in (p.get((k,),s.QQ.zero),)) if p else ()

def same(p,cs,message):
    need(coefficients(p)==tuple(cs),message)

def determinant(m):
    return sum(((-1)**sum(p[i]>p[j] for i,j in combinations(range(3),2))
                *m[0][p[0]]*m[1][p[1]]*m[2][p[2]] for p in permutations(range(3))),Z)

def metric(x,y):
    return sum((x[i]*(O if i==j else t)*y[j] for i in range(3) for j in range(3)),Z)

def ordinary(x,y):
    return sum((a*b for a,b in zip(x,y)),Z)

def normal(x):
    return [sum((x[i]*(O if i==j else t) for i in range(3)),Z) for j in range(3)]

@lru_cache(None)
def sign_coefficients(cs,a,b):
    if not cs:return 0
    p=native(cs);n=p.degree()
    shifted=p.compose(t,qq(a)+qq(b-a)*t)
    c=[shifted.get((k,),s.QQ.zero) for k in range(n+1)]
    B=[sum((c[k]*(s.QQ(comb(i,k))/s.QQ(comb(n,k))) for k in range(i+1)),s.QQ.zero)
       for i in range(n+1)]
    if B[0]>0 and B[-1]>0 and all(x>=0 for x in B):return 1
    if B[0]<0 and B[-1]<0 and all(x<=0 for x in B):return -1
    return None

def sign(p,a,b):
    return sign_coefficients(coefficients(p),a,b)

def direct_points():
    # Independent explicit polynomials in r, rather than the reflection generator.
    table={
        0:[(-1,0,1),(0,-1),(0,1,1)],
        1:[(0,1),(-1,),(0,1)],
        2:[(1,),(),()],
        3:[(0,1),(0,1),(-1,)],
        4:[(0,-1,1,1),(-1,0,2,1),(0,-1,-1)],
        5:[(-1,0,1),(0,1,1),(0,-1)],
        6:[(),(1,),()],
        7:[(),(),(1,)],
        11:[(0,-1,1,1),(0,-1,-1),(-1,0,2,1)],
        12:[(0,-2,0,1),(1,0,-1),(0,0,1,1)]}
    def convert(p):return sum((c*(2*t)**k*S**(3-k) for k,c in enumerate(p)),Z)
    return {i:[convert(p) for p in v] for i,v in table.items()},S**3

def normalize(row):
    denominator=lcm(*(int(c.denominator) for p in row for c in p.values()))
    row=[p.mul_ground(s.QQ(denominator)) for p in row]
    while True:
        pairs=[p.div(S) for p in row]
        if any(r for q,r in pairs):break
        row=[q for q,r in pairs]
    content=reduce(gcd,(int(c) for p in row for c in p.values()),0)
    need(content>0,'native nonzero row')
    return [p.mul_ground(s.QQ(1)/s.QQ(content)) for p in row]

def build(certificate,pieces):
    points,D=direct_points();source_points,source_D=check.core_points()
    same(D,source_D,'common denominator disagreement')
    for i,v in points.items():
        for k,x in enumerate(v):same(x,source_points[i][k],'coordinate disagreement')
        need(metric(v,v)==D*D,'native core norm')
    for i,j in combinations(sorted(points),2):
        gap=t*D*D-metric(points[i],points[j])
        need(not gap or all(sign(gap,a,b)==1 for a,b in pieces),'native core packing')
    A,B,W=native((-1,-1,5,5)),native((1,5,-1,-13)),native((0,8,8,-16))
    weights=(A,B,A,B)
    need(sum(weights,Z)==W,'native weight normalization')
    need(all(sum((w*points[i][k] for w,i in zip(weights,(0,1,4,5))),Z)==Z for k in range(3)),'native origin identity')
    rank=determinant([points[i] for i in (0,1,4)])
    for a,b in pieces:
        need(all(sign(p,a,b)==1 for p in weights+(W,D)),'native positive denominators/weights')
        need(sign(rank,a,b) in (-1,1),'native rank three')
    rows=[normalize(normal(points[i])+[t*D]) for i in check.LABELS]
    source_caps,source_heights,source_guards=check.cap_rows(certificate)
    h0,eps=qq(Q(*certificate['base_height'])),qq(Q(*certificate['epsilon']))
    for j,w in enumerate(certificate['axes']):
        axis=[R(qq(Q(*x))) for x in w]
        g=(1+t)*metric(axis,axis).mul_ground(s.QQ(1,2))
        h=(R(h0*h0)+g).mul_ground(1/(2*h0))+eps
        guard=(h*h-g)*2
        identity=(R(h0*h0)-g)**2/(4*h0*h0)+eps*(R(h0*h0)+g)/h0+eps*eps
        need(h*h-g==identity,'native cap guard identity')
        same(h,source_heights[j],'cap height disagreement');same(guard,source_guards[j],'cap guard disagreement')
        need(all(sign(h,a,b)==1 for a,b in pieces),'native positive cap height')
        rows.append(normalize(normal(axis)+[h]))
    source_rows=[check.normalize_row(check.P.normal(source_points[i])+[check.P.mul(check.P.T,source_D)]) for i in check.LABELS]+source_caps
    for row,source in zip(rows,source_rows):
        for p,cs in zip(row,source):same(p,cs,'positive inequality row disagreement')
    return points,D,rows,source_rows

def parent_match(points,D):
    parent=HERE.parent/'tammes15_decagon_extension_reduction'
    need((parent/'polytope.py').is_file(),'previous published source unavailable')
    sys.path.insert(0,str(parent))
    from polytope import core
    previous,mask,mapping=core((2,1,1),[(0,9),(1,10),(7,8)])
    need(mask==22577587577793 and set(previous)==set(points),'parent prototype identification')
    for i,v in previous.items():
        for k,x in enumerate(v):need(native(x.n)*D==native(x.d)*points[i][k],'parent pointwise identity')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=364)
    parser.add_argument('--compare-parent',action='store_true');args=parser.parse_args()
    need(1<=args.limit<=364,'bounded audit workload')
    certificate=json.loads((HERE/'certificate.json').read_text());pieces=check.intervals(certificate)
    source=check.verify(certificate,trace=True);traces=source.pop('traces')
    need(source==json.loads((HERE/'EXPECTED.json').read_text()),'source exact result mismatch')
    points,D,rows,source_rows=build(certificate,pieces)
    if args.compare_parent:parent_match(points,D)
    source_data=check.cramer_data(source_rows);triples=list(combinations(range(14),3))
    need(len(traces)==len(pieces) and all([w[0] for w in trace]==[list(x) for x in triples] for trace in traces),'complete witness indexing')
    for index,triple in enumerate(triples[:args.limit]):
        N=[rows[i][:3] for i in triple];b=[rows[i][3] for i in triple]
        d=determinant(N)
        Y=[determinant([[b[i] if j==k else N[i][j] for j in range(3)] for i in range(3)]) for k in range(3)]
        E=[row[3]*d-ordinary(row[:3],Y) for row in rows];K=metric(Y,Y)-d*d
        py_triple,py_d,py_Y,py_E,py_K=source_data[index]
        need(tuple(py_triple)==triple,'Cramer indexing disagreement');same(d,py_d,'Cramer determinant disagreement')
        for native_p,cs in zip(Y+E+[K],py_Y+py_E+[py_K]):same(native_p,cs,'Cramer/slack/norm polynomial disagreement')
        for piece,(a,b) in enumerate(pieces):
            witness=traces[piece][index]
            if witness[1]=='singular':need(not d,'native singular witness')
            elif witness[1]=='opposite':need(sign(E[witness[2]],a,b)==1 and sign(E[witness[3]],a,b)==-1,'native opposite slack signs')
            elif witness[1]=='norm':need(sign(K,a,b)==-1,'native strict norm sign')
            else:raise ValueError('unknown witness type')
    print(json.dumps({'agent':'six-tammes-2','role':'researcher','sympy_version':s.__version__,
                      'status':'COMPLETE_SEPARATE_ALGEBRA_AUDIT' if args.limit==364 else 'PARTIAL_AUDIT_NOT_A_CERTIFICATE',
                      'coordinate_entries_compared':30,'inequality_rows_compared':14,
                      'cramer_triples_compared':args.limit,'closed_interval_witnesses_checked':args.limit*len(pieces),
                      'parent_pointwise_identity_checked':args.compare_parent,'source_expected_matches':True,
                      'trust':'Direct coordinate table, QQ[t] arithmetic, permutation determinants, native affine composition and exact Bernstein signs separately checked. Certificate and written geometry shared. No independent mathematical review or formalization.'},indent=2,sort_keys=True))
