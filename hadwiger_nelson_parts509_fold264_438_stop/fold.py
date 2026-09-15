"""One exact fold of Parts509. Rational multiquadratic arithmetic only."""
from fractions import Fraction as Q
from math import isqrt, lcm, gcd
from itertools import combinations
from pathlib import Path
import hashlib
import json

RAD = (1,3,5,15,11,33,55,165)
ZERO = (Q(0),)*8
ONE = (Q(1),)+(Q(0),)*7
SOURCE_SHA = 'f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50'

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def add(a,b):
    return tuple(x+y for x,y in zip(a,b))

def neg(a):
    return tuple(-x for x in a)

def sub(a,b):
    return add(a,neg(b))

def scale(a,q):
    return tuple(x*q for x in a)

def mul(a,b):
    out=[Q(0)]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    out[i^j]+=x*y*RAD[i&j]
    return tuple(out)

def inverse(a):
    v=a; acc=ONE
    for bit in (1,2,4):
        b=tuple(-x if i&bit else x for i,x in enumerate(v))
        acc=mul(acc,b); v=mul(v,b)
    require(v[0] and not any(v[1:]), 'nonzero rational field norm')
    result=scale(acc,1/v[0])
    require(mul(a,result)==ONE, 'checked inverse')
    return result

def sign(a):
    if not any(a):
        return 0,0
    for bits in (32,64,128,256,512):
        den=1<<bits; lo=Q(0); hi=Q(0)
        for c,d in zip(a,RAD):
            root=isqrt(d*den*den)
            upper=root if root*root==d*den*den else root+1
            if c>=0:
                lo+=c*root;hi+=c*upper
            else:
                lo+=c*upper;hi+=c*root
        # The common positive interval denominator is unnecessary for signs.
        if lo>0:return 1,bits
        if hi<0:return -1,bits
    raise ValueError('Sign unresolved; do not guess a half-plane')

MASK_TERMS=[(i,j,i^j,2*RAD[i&j]) for i in range(8) for j in range(i+1,8)]
GCD_TERMS=[(i,j,RAD.index(RAD[i]*RAD[j]//gcd(RAD[i],RAD[j])**2),
            2*gcd(RAD[i],RAD[j])) for i in range(8) for j in range(i+1,8)]

def norm(v, alternate=False):
    x=v[:8];y=v[8:]
    r=[sum(d*(a*a+b*b) for d,a,b in zip(RAD,x,y))]+[0]*7
    for i,j,k,c in GCD_TERMS if alternate else MASK_TERMS:
        r[k]+=c*(x[i]*x[j]+y[i]*y[j])
    return tuple(r)

def all_edges(points,den,dual=True):
    edges=[];one=(den*den,)+(0,)*7
    for i,j in combinations(range(len(points)),2):
        d=tuple(a-b for a,b in zip(points[i],points[j]));s=norm(d)
        if dual:require(s==norm(d,True),'two exact norm reductions')
        if s==one:edges.append([i,j])
    return edges

def build(path):
    raw=Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'pinned Parts points')
    source=[tuple(map(int,line.split())) for line in raw.decode().splitlines()
            if line and not line.startswith('#')]
    require(len(source)==len(set(source))==509,'source distinctness')
    p=[(tuple(Q(x,96) for x in row[:8]),tuple(Q(y,96) for y in row[8:])) for row in source]
    a,b=264,438
    nx=sub(p[b][0],p[a][0]);ny=sub(p[b][1],p[a][1])
    mx=scale(add(p[a][0],p[b][0]),Q(1,2));my=scale(add(p[a][1],p[b][1]),Q(1,2))
    n2=add(mul(nx,nx),mul(ny,ny));inv=inverse(n2)
    fx=scale(mul(nx,inv),2);fy=scale(mul(ny,inv),2)
    images=[];classes=[];lookup={};image_of=[];side=[];bits_used=[]
    for i,(x,y) in enumerate(p):
        dot=add(mul(sub(x,mx),nx),mul(sub(y,my),ny))
        s,bits=sign(dot);side.append(s);bits_used.append(bits)
        image=(sub(x,mul(dot,fx)),sub(y,mul(dot,fy))) if s<0 else (x,y)
        key=image[0]+image[1]
        if key not in lookup:
            lookup[key]=len(images);images.append(key);classes.append([])
        k=lookup[key];classes[k].append(i);image_of.append(k)
    require(image_of[a]==image_of[b] and len(images)<=508,'prescribed merger and cap')
    den=lcm(*(x.denominator for row in images for x in row))
    points=[tuple(int(x*den) for x in row) for row in images]
    edges=all_edges(points,den)
    source_edges=all_edges(source,96)
    require(len(source_edges)==2442,'complete positive parent edges')
    es={tuple(e) for e in edges}
    mapped={tuple(sorted((image_of[a],image_of[b]))) for a,b in source_edges}
    retained=sum(tuple(sorted((image_of[a],image_of[b]))) in es for a,b in source_edges)
    oldkeys={tuple(Q(x,96) for x in row) for row in source}
    sigma5={tuple(-x if (i%8)&2 else x for i,x in enumerate(row)) for row in oldkeys}
    old_switch=oldkeys|sigma5
    # A fixed inherited Moser spindle, checked only if its images still work.
    moser=[0,398,408,459,397,407,470]
    mv=[image_of[v] for v in moser]
    me=[[i,j] for i,j in combinations(range(7),2) if tuple(sorted((mv[i],mv[j]))) in es]
    result=dict(points=points,denominator=den,edges=edges,source_edges=source_edges,
                classes=classes,image_of=image_of,side=side,
                facts=dict(source_points=509,source_edges=2442,points=len(points),
                    unit_edges=len(edges),moved_points=side.count(-1),
                    fixed_points=side.count(1),on_axis=side.count(0),
                    collision_classes=[c for c in classes if len(c)>1],
                    maximum_sign_interval_bits=max(bits_used),
                    original_edges_retained=retained,original_edges_lost=2442-retained,
                    new_unit_pairs_without_source_edge=len(es-mapped),
                    points_outside_parent=sum(row not in oldkeys for row in images),
                    points_outside_sigma5_union=sum(row not in old_switch for row in images),
                    source_sigma5_union_size=len(old_switch),
                    inherited_moser_distinct=len(set(mv))==7,
                    inherited_moser_image_indices=mv,inherited_moser_edges=me,
                    exact_coordinate_denominator_digits=len(str(den))))
    return result

def dump_cnf(path,n,edges,k=4):
    clauses=[]
    for v in range(n):
        clauses.append([k*v+c+1 for c in range(k)])
        clauses.extend([-k*v-c-1,-k*v-d-1] for c,d in combinations(range(k),2))
    for a,b in edges:
        clauses.extend([-k*a-c-1,-k*b-c-1] for c in range(k))
    clauses.append([1])
    with Path(path).open('w') as f:
        f.write(f'p cnf {k*n} {len(clauses)}\n')
        for c in clauses:f.write(' '.join(map(str,c))+' 0\n')
    return clauses
