#!/usr/bin/env python3
"""Exact proper-body Cayley quotient; not by itself a Rupert exclusion.

The written finite-to-continuum bridge is in PROOF.md.
All signs and quaternion identities below use ordered Q(phi), not float.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
import argparse,hashlib,importlib.util,json,resource,sys,time
ROOT=Path(__file__).resolve().parents[3]
PATH=ROOT/'round-two/six-rupert-1/pentagonal_minimum_diameter/verify.py'
PIN='12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339'
if hashlib.sha256(PATH.read_bytes()).hexdigest()!=PIN:
    raise ValueError('named-model arithmetic fingerprint changed')
spec=importlib.util.spec_from_file_location('cayley_cell_named_arithmetic',PATH)
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)
Q,Z,O,phi=V.Q,V.Z,V.ONE,V.PHI

def require(test,message):
    if not test:raise ValueError(message)

def determinant(A):
    return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
            -A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
            +A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))

def solve(A,b):
    rows=[list(row)+[rhs] for row,rhs in zip(A,b)]
    for j in range(3):
        pivot=next((i for i in range(j,3) if rows[i][j]!=Z),None)
        require(pivot is not None,'singular active normal triple')
        rows[j],rows[pivot]=rows[pivot],rows[j]
        factor=rows[j][j];rows[j]=[x/factor for x in rows[j]]
        for i in range(3):
            if i!=j:
                factor=rows[i][j]
                rows[i]=[a-factor*b for a,b in zip(rows[i],rows[j])]
    result=tuple(row[-1] for row in rows)
    require(V.mv(A,result)==tuple(b),'exact active-triple solution identity')
    return result

def quaternion(M):
    scalar_square=(sum(M[i][i] for i in range(3))+1)/4
    candidates=(O,phi/2,(phi-1)/2,Q(F(1,2)),Z)
    scalar=next((x for x in candidates if x*x==scalar_square),None)
    require(scalar is not None,'proper-group quaternion scalar')
    if scalar!=Z:
        vector=((M[2][1]-M[1][2])/(4*scalar),
                (M[0][2]-M[2][0])/(4*scalar),
                (M[1][0]-M[0][1])/(4*scalar))
    else:
        i=next(i for i in range(3) if M[i][i]+1!=Z)
        square=(M[i][i]+1)/2
        roots=(O,Q(F(1,2)),phi/2,(phi-1)/2)
        root=next((x for x in roots if x*x==square),None)
        require(root is not None,'half-turn quaternion axis root')
        vector=tuple(root if j==i else M[j][i]/(2*root) for j in range(3))
    require(scalar*scalar+V.dot(vector,vector)==O,'exact unit quaternion')
    x,y,z=vector;cross=((Z,-z,y),(z,Z,-x),(-y,x,Z))
    rebuilt=tuple(tuple((scalar*scalar-V.dot(vector,vector))*(O if i==j else Z)
                        +2*vector[i]*vector[j]+2*scalar*cross[i][j]
                        for j in range(3)) for i in range(3))
    require(rebuilt==M,'exact proper-group quaternion reconstruction')
    return scalar,vector

def encode(x):return [str(x.a),str(x.b)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=str(Path(__file__).resolve().parent/'.generated/source.json'))
    args=parser.parse_args();start=time.monotonic()
    group=V.group();quaternions=[quaternion(M) for M in group]
    coordinate_basis={tuple(O if i==j else Z for i in range(4))for j in range(4)}
    signed_quaternions={tuple(sgn*x for x in (a,*b))for a,b in quaternions for sgn in(-1,1)}
    require(coordinate_basis<=signed_quaternions,'identity and three coordinate half-turns ensure a nonzero folded scalar')
    W=tuple(tuple(s*x for x in w) for w in V.W for s in (-1,1))
    threshold=phi-1
    require(len(W)==len(set(W))==12 and threshold.sign()>0,'twelve literal facets and origin interior')
    # Opposite normals of three independent pairs force recession cone0.
    require(all(tuple(-x for x in w) in W for w in W),'all opposite facet pairs')
    require(determinant((W[0],W[2],W[4]))!=Z,'facet normals span R3')
    near=[(i,a,b) for i,(a,b) in enumerate(quaternions) if a==phi/2]
    require(len(near)==12,'twelve nearest nontrivial proper matrices')
    require({tuple(2*phi*x for x in b) for _,a,b in near}==set(W),'nearest-group constraints exactly literal facets')
    require(2*phi*(1-phi/2)==threshold,'Cayley halfspace normalization')
    vertices=set();nonsingular=0;singular=0;feasible_triples=[]
    for selected in combinations(range(12),3):
        A=tuple(W[i] for i in selected)
        if determinant(A)==Z:singular+=1;continue
        nonsingular+=1;c=solve(A,(threshold,)*3)
        if all((threshold-V.dot(w,c)).sign()>=0 for w in W):
            vertices.add(c);feasible_triples.append(selected)
    expected=set()
    scale=1/(phi*phi*phi)
    expected.update(tuple(scale*Q(s) for s in signs) for signs in product((-1,1),repeat=3))
    for s,t in product((-1,1),repeat=2):
        d=(Z,Q(s)/phi,Q(t)*phi)
        for _ in range(3):expected.add(tuple(scale*x for x in d));d=(d[2],d[0],d[1])
    require(len(vertices)==20 and vertices==expected,'complete exact dodecahedral vertex inventory')
    vertices=sorted(vertices,key=lambda row:tuple((x.a,x.b) for x in row))
    comparisons=0
    for c in vertices:
        for a,b in quaternions:
            value=a+V.dot(b,c)
            require((1-value).sign()>=0 and (1+value).sign()>=0,'complete proper-body closest-identity inequality')
            comparisons+=2
    radius_square=3*scale*scale
    require(all(V.dot(c,c)==radius_square for c in vertices),'common exact extreme squared radius')
    require(radius_square==Q(39,-24),'exact covering radius squared')
    coordinate_limit=2-phi
    require(all((coordinate_limit-s*c[i]).sign()>=0 for c in vertices for i in range(3) for s in (-1,1)),
            'exact coordinate radius')
    record=dict(status='EXACT_PROPER_BODY_CAYLEY_CELL_IDENTITIES_PASSED_NOT_A_RUPERT_EXCLUSION',
                agent='six-rupert-1',role='researcher',facet_count=12,proper_body_count=60,
                triple_candidates=220,nonsingular_triples=nonsingular,singular_triples=singular,
                feasible_active_triples=len(feasible_triples),vertices_count=20,
                all_proper_signed_vertex_comparisons=comparisons,
                facets=[list(map(encode,w)) for w in W],threshold=encode(threshold),
                vertices=[list(map(encode,c)) for c in vertices],
                proper_quaternions=[dict(scalar=encode(a),vector=list(map(encode,b))) for a,b in quaternions],
                covering_cayley_radius_squared=encode(radius_square),coordinate_limit=encode(coordinate_limit),
                exact_angle='2*atan(sqrt(39-24*phi)); attained at every listed vertex',
                source_sha256={'named_model/verify.py':PIN},
                written_bridge='Every proper Q may be right-folded by a proper body g; the nearest-identity quaternion has positive scalar, c=vector/scalar. The complete60 inequalities |a+b dot c|<=1 equal these12 halfspaces by exact vertex domination. Bounded recession plus complete active-triple enumeration certifies the full real cell. Standard nearest-orbit/quaternion geometry; no method priority claimed.',
                scope='A full relative SO(3)/I chart, retaining chiral same-handed source and arbitrary actual translation. No containment classification or global/nonlocal Rupert exclusion.',
                arithmetic='Python Fraction and ordered Q(phi); ordinary written convexity/quaternion argument is unformalized and independently unreviewed.')
    Path(args.output).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=record['status'],vertices_count=20,comparisons=comparisons,
                         elapsed_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))

if __name__=='__main__':main()
