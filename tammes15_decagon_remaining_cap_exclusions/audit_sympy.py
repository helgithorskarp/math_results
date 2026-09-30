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

R_TABLES = [{2: [[1], [], []], 6: [[], [1], []], 7: [[], [], [1]], 1: [[0, 1], [-1], [0, 1]], 0: [[-1, 0, 1], [0, -1], [0, 1, 1]], 5: [[0, 1], [0, 1], [-1]], 3: [[0, 1, 1], [-1, 0, 1], [0, -1]], 4: [[-1, 0, 2, 1], [0, -1, 1, 1], [0, -1, -1]], 11: [[0, -1, 1, 1], [0, -1, -1], [-1, 0, 2, 1]], 12: [[0, -2, 0, 1], [1, 0, -1], [0, 0, 1, 1]]}, {2: [[1], [], []], 6: [[], [1], []], 7: [[], [], [1]], 1: [[0, 1], [-1], [0, 1]], 0: [[-1, 0, 1], [0, -1], [0, 1, 1]], 4: [[0, 1], [0, 1], [-1]], 3: [[0, 1, 1], [-1, 0, 1], [0, -1]], 5: [[-1, 0, 1], [0, 1, 1], [0, -1]], 11: [[0, -1, 1, 1], [-1, 0, 2, 1], [0, -1, -1]], 12: [[0, -2, 0, 1], [0, 0, 1, 1], [1, 0, -1]]}, {2: [[1], [], []], 6: [[], [1], []], 7: [[], [], [1]], 1: [[0, 1], [-1], [0, 1]], 0: [[-1, 0, 1], [0, -1], [0, 1, 1]], 4: [[0, 1], [0, 1], [-1]], 3: [[0, 1, 1], [-1, 0, 1], [0, -1]], 5: [[-1, 0, 1], [0, 1, 1], [0, -1]], 11: [[0, -1, 1, 1], [0, -1, -1], [-1, 0, 2, 1]], 12: [[0, -2, 0, 1], [1, 0, -1], [0, 0, 1, 1]]}]

def direct_points(index):
    # Fixed explicit coordinate polynomials in r; no reflection generator.
    def convert(p):return sum((c*(2*t)**k*S**(3-k) for k,c in enumerate(p)),Z)
    return {i:[convert(p) for p in v] for i,v in R_TABLES[index].items()},S**3


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

def build(index,entry,pieces):
    points,D=direct_points(index);source_points,source_D=check.core_points(index)
    same(D,source_D,'common denominator disagreement')
    for i,v in points.items():
        for k,x in enumerate(v):same(x,source_points[i][k],'coordinate disagreement')
        need(metric(v,v)==D*D,'native core norm')
    for i,j in combinations(sorted(points),2):
        gap=t*D*D-metric(points[i],points[j])
        need(not gap or all(sign(gap,a,b)==1 for a,b in pieces),'native core packing')
    labels=check.ORIGINS[index]
    weights=[check.ORIENTATIONS[index]*(-1)**j
             *determinant([points[labels[k]] for k in range(4) if k!=j]) for j in range(4)]
    W=sum(weights,Z);source_weights,source_W=check.origin_data(source_points,index)
    for p,cs in zip(weights+[W],source_weights+[source_W]):same(p,cs,'origin cofactor disagreement')
    need(all(sum((w*points[i][k] for w,i in zip(weights,labels)),Z)==Z for k in range(3)),
         'native origin identity')
    rank=determinant([points[i] for i in labels[:3]])
    for a,b in pieces:
        need(all(sign(p,a,b)==1 for p in weights+[W,D]),'native positive denominators/cofactors')
        need(sign(rank,a,b) in (-1,1),'native rank three')
    rows=[normalize(normal(points[i])+[t*D]) for i in check.LABELS]
    source_caps,source_heights,source_guards=check.cap_rows(entry)
    h0,eps=qq(Q(*entry['base_height'])),qq(Q(*entry['epsilon']))
    for j,w in enumerate(entry['axes']):
        axis=[R(qq(Q(*x))) for x in w]
        g=(1+t)*metric(axis,axis).mul_ground(s.QQ(1,2))
        h=(R(h0*h0)+g).mul_ground(1/(2*h0))+eps
        guard=(h*h-g)*2
        identity=(R(h0*h0)-g)**2/(4*h0*h0)+eps*(R(h0*h0)+g)/h0+eps*eps
        need(h*h-g==identity,'native cap guard identity')
        same(h,source_heights[j],'cap height disagreement');same(guard,source_guards[j],'guard disagreement')
        need(all(sign(h,a,b)==1 for a,b in pieces),'native positive cap height')
        rows.append(normalize(normal(axis)+[h]))
    source_rows=[check.normalize_row(check.P.normal(source_points[i])+[check.P.mul(check.P.T,source_D)])
                 for i in check.LABELS]+source_caps
    for row,source in zip(rows,source_rows):
        for p,cs in zip(row,source):same(p,cs,'positive inequality row disagreement')
    return points,D,rows,source_rows

def parent_match(points,D,index):
    parent=HERE.parent/'tammes15_decagon_extension_reduction'
    need((parent/'polytope.py').is_file(),'previous published source unavailable')
    if str(parent) not in sys.path:sys.path.insert(0,str(parent))
    from polytope import core
    previous,mask,mapping=core(check.CORE_KEYS[index],check.ALIASES[index])
    need(mask==check.MASKS[index] and set(previous)==set(points),'parent prototype identification')
    for i,v in previous.items():
        for k,x in enumerate(v):need(native(x.n)*D==native(x.d)*points[i][k],'parent pointwise identity')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,default=364)
    parser.add_argument('--compare-parent',action='store_true');args=parser.parse_args()
    need(1<=args.limit<=364,'bounded per-core audit workload')
    certificate=json.loads((HERE/'certificate.json').read_text())
    source=check.verify(certificate,trace=True);traces=source.pop('traces')
    need(source==json.loads((HERE/'EXPECTED.json').read_text()),'source exact result mismatch')
    triples=list(combinations(range(14),3));witness_count=0
    need(len(traces)==3,'complete core trace indexing')
    for index,entry in enumerate(certificate['types']):
        pieces=check.intervals(entry,index)
        points,D,rows,source_rows=build(index,entry,pieces)
        if args.compare_parent:parent_match(points,D,index)
        source_data=check.cramer_data(source_rows);type_traces=traces[index]
        need(len(type_traces)==len(pieces)
             and all([w[0] for w in trace]==[list(x) for x in triples] for trace in type_traces),
             'complete witness indexing')
        for position,triple in enumerate(triples[:args.limit]):
            N=[rows[i][:3] for i in triple];b=[rows[i][3] for i in triple]
            d=determinant(N)
            Y=[determinant([[b[i] if j==k else N[i][j] for j in range(3)] for i in range(3)])
               for k in range(3)]
            E=[row[3]*d-ordinary(row[:3],Y) for row in rows];K=metric(Y,Y)-d*d
            py_triple,py_d,py_Y,py_E,py_K=source_data[position]
            need(tuple(py_triple)==triple,'Cramer indexing disagreement');same(d,py_d,'Cramer determinant disagreement')
            for p,cs in zip(Y+E+[K],py_Y+py_E+[py_K]):same(p,cs,'Cramer/slack/norm disagreement')
            for piece,(a,b) in enumerate(pieces):
                witness=type_traces[piece][position]
                if witness[1]=='singular':need(not d,'native singular witness')
                elif witness[1]=='opposite':need(sign(E[witness[2]],a,b)==1 and sign(E[witness[3]],a,b)==-1,
                                               'native opposite signs')
                elif witness[1]=='norm':need(sign(K,a,b)==-1,'native norm sign')
                else:raise ValueError('unknown witness type')
                witness_count+=1
    print(json.dumps({'agent':'six-tammes-2','role':'researcher','sympy_version':s.__version__,
                      'status':'COMPLETE_SEPARATE_ALGEBRA_AUDIT' if args.limit==364 else 'PARTIAL_AUDIT_NOT_A_CERTIFICATE',
                      'coordinate_entries_compared':90,'inequality_rows_compared':42,
                      'cramer_triples_compared':3*args.limit,'closed_interval_witnesses_checked':witness_count,
                      'parent_pointwise_identities_checked':args.compare_parent,'source_expected_matches':True,
                      'trust':'Direct coordinate tables, QQ[t] arithmetic, permutation determinants, native affine composition and exact Bernstein signs separately checked. Certificate and written geometry shared. No independent mathematical review or formalization.'},indent=2,sort_keys=True))
