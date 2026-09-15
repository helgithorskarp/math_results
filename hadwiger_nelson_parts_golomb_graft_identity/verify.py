#!/usr/bin/env python3
"""Exact single-placement identity; no colour solver or family enumeration."""
import hashlib,json,math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
HERE=Path(__file__).resolve().parent
B=(1,3,5,15,11,33,55,165)

def require(ok,message):
    if not ok:raise ValueError(message)

def plus(a,b):
    out=a.copy()
    for d,x in b.items():out[d]=out.get(d,0)+x
    return {d:x for d,x in out.items() if x}

def scale(a,t):return {d:x*t for d,x in a.items() if x*t}

def times(a,b):
    out={}
    for d,x in a.items():
        for e,y in b.items():
            g=math.gcd(d,e);r=d*e//(g*g)
            out[r]=out.get(r,0)+g*x*y
    return {d:x for d,x in out.items() if x}

def psub(a,b):return plus(a[0],scale(b[0],-1)),plus(a[1],scale(b[1],-1))
def padd(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def conjugate(a):return a[0],scale(a[1],-1)
def product(a,b):
    return plus(times(a[0],b[0]),scale(times(a[1],b[1]),-1)),plus(times(a[0],b[1]),times(a[1],b[0]))
def norm(a):return plus(times(a[0],a[0]),times(a[1],a[1]))
def encoded(a):
    xs=[a[k].get(d,0)*96 for k in range(2) for d in B]
    require(all(F(x).denominator==1 for x in xs),'nonintegral coordinate')
    return tuple(int(x) for x in xs)
def decoded(a):return tuple({d:F(a[8*k+i],96) for i,d in enumerate(B) if a[8*k+i]} for k in range(2))

def squared_integer_difference(a,b):
    # Full integer sparse-radical norm, independent of the discovery XOR basis.
    v=tuple({d:a[8*k+i]-b[8*k+i] for i,d in enumerate(B) if a[8*k+i]!=b[8*k+i]} for k in range(2))
    return norm(v)

def compute():
    manifest=json.loads((HERE/'inputs.json').read_text())
    data=(HERE.parent/manifest['coordinate_file']).read_bytes()
    require(hashlib.sha256(data).hexdigest()==manifest['coordinate_sha256'],'coordinate pin')
    old=[tuple(map(int,line.split())) for line in data.decode().splitlines() if not line.startswith('#')]
    require(len(old)==509 and len(set(old))==509 and all(len(p)==16 for p in old),'source shape')
    rows=[(0,0,0,0),(36,0,0,0),(18,0,18,0),(-18,0,18,0),(-36,0,0,0),(-18,0,-18,0),(18,0,-18,0),(6,0,0,2),(-3,-3,3,-1),(-3,3,-3,-1)]
    atom=[({d:x for d,x in {1:F(a,36),33:F(b,36)}.items() if x},{d:x for d,x in {3:F(c,36),11:F(d,12)}.items() if x}) for a,b,c,d in rows]
    edge=psub(atom[8],atom[7]);require(norm(edge)=={1:1},'Golomb anchor edge')
    target=psub(decoded(old[149]),decoded(old[0]));require(norm(target)=={1:1},'Parts anchor edge')
    u=product(target,conjugate(edge));require(norm(u)=={1:1},'isometry multiplier')
    placed=[padd(decoded(old[0]),product(u,psub(g,atom[7]))) for g in atom]
    require(all(norm(psub(placed[i],placed[j]))==norm(psub(atom[i],atom[j])) for i,j in combinations(range(10),2)),'all45 atom distances preserved')
    mapped=[encoded(g) for g in placed]
    collisions={str(i):old.index(q) for i,q in enumerate(mapped) if q in old}
    new=sorted(set(mapped)-set(old));require(len(new)==1,'one new point')
    q=(64,0,0,0,0,0,0,0,0,0,0,0,32,0,0,0);require(new==[q],'exact q')
    points=old+new
    edges=[(i,j) for i,j in combinations(range(510),2) if squared_integer_difference(points[i],points[j])=={1:96**2}]
    neighbors=[i for i,j in edges if j==509]
    report={'all_checks':True,'source_points':509,'atom_points':10,'coincidences':collisions,'new_points':1,'new_point_scale96':list(q),'union_points':510,'complete_unit_edges':len(edges),'base_edges':sum(j<509 for i,j in edges),'new_neighbors':neighbors,'atom_distances_checked':45,'union_pair_checks':129795,'edge_sha256':hashlib.sha256((json.dumps(edges,separators=(',',':'))+'\n').encode()).hexdigest(),'record_candidate':False,'new_four_colour_query':False,'new_five_colouring_check':False,'capped_exclusion_is_imported':True}
    return report,mapped,edges

if __name__=='__main__':
    result,_,_=compute()
    expected=HERE/'expected.json'
    if expected.exists():require(result==json.loads(expected.read_text()),'expected output')
    print(json.dumps(result,sort_keys=True))
