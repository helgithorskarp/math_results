"""Exact continuous decagon coordinates, graph identification and polytope arithmetic."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from family import models,branch_rat,dot,cross,H,t,one,zero
from polynomial import need,bernstein,root_count,value

@lru_cache(None)
def polynomial_sign(p):
    if not p:return 0
    b=bernstein(p)
    if all(x>=0 for x in b) and any(x>0 for x in b):return 1
    if all(x<=0 for x in b) and any(x<0 for x in b):return -1
    if root_count(p)==0:
        v=value(p,Fraction(11,20));return (v>0)-(v<0)
    return None

def sign(x):
    if not x.n:return 0
    a,b=polynomial_sign(x.n),polynomial_sign(x.d)
    return a*b if a is not None and b not in (None,0) else None

def ordinary(x,y):return sum((a*b for a,b in zip(x,y)),zero)
def determinant(rows):return ordinary(rows[0],cross(rows[1],rows[2]))
def normal(x):return [sum((x[i]*H[i][k] for i in range(3)),zero) for k in range(3)]
def encode(x):return {'numerator':list(x.n),'denominator':list(x.d)}
def code(y):return tuple((x.n,x.d) for x in y)

def canonical(edges,labels):
    edges=frozenset(edges);triangles=[z for z in combinations(labels,3) if all(e in edges for e in combinations(z,2))]
    count=Counter(e for z in triangles for e in combinations(z,2));boundary={e for e in edges if count[e]==1}
    need(len(edges)==17 and len(triangles)==8 and len(boundary)==10 and max(count.values())==2,'decagon incidence')
    nb={i:{j for e in boundary if i in e for j in e if j!=i} for i in labels};need(all(len(v)==2 for v in nb.values()),'boundary degrees')
    order=[min(labels)]
    while len(order)<10:
        choices=nb[order[-1]]-set(order);need(choices,'connected boundary');order.append(min(choices))
    need(order[0] in nb[order[-1]],'boundary cycle')
    index={v:i for i,v in enumerate(order)};pairs=list(combinations(range(10),2));images=[]
    for shift in range(10):
        for direction in (-1,1):
            mapping={v:(shift+direction*i)%10 for v,i in index.items()}
            es={tuple(sorted((mapping[i],mapping[j]))) for i,j in edges}
            mask=sum(1<<k for k,e in enumerate(pairs) if e in es);images.append((mask,mapping))
    return min(images,key=lambda z:z[0])

def core(key,aliases):
    p,c,orientation=key;mm=models();model=mm[p];case=model['cases'][c]
    need(not case['residual'].n and orientation in (-1,1),'continuous branch')
    raw={**model['a'],**branch_rat(case,orientation)};mapping={i:i for i in range(13)}
    need(len(aliases)==3 and {j for i,j in aliases}=={8,9,10},'anchor alias cover')
    for i,j in aliases:
        need(type(i) is int and 0<=i<8,'alias domain')
        need(all(not (x-y).n for x,y in zip(raw[i],raw[j])),'exact alias identity');mapping[j]=i
    points={mapping[i]:raw[i] for i in range(13)};need(len(points)==10,'ten distinct indices')
    need(all(not (dot(x,x)-one).n for x in points.values()),'unit norms')
    edges=[]
    for i,j in combinations(sorted(points),2):
        g=dot(points[i],points[j]);need(sign(one-g)==1,'real distinctness')
        gap=t-g;need(not gap.n or sign(gap)==1,'packing throughout interval')
        if not gap.n:edges.append((i,j))
    mask,canonical_mapping=canonical(edges,sorted(points))
    return points,mask,canonical_mapping

def origin_relation(points,labels):
    need(len(labels)==4 and len(set(labels))==4 and set(labels)<=set(points),'origin labels')
    cofactors=[(-1)**j*determinant([points[labels[k]] for k in range(4) if k!=j]) for j in range(4)]
    total=sum(cofactors,zero);need(sign(total) in (-1,1),'origin cofactor sum')
    weights=[x/total for x in cofactors]
    need(all(sign(x)==1 for x in weights),'positive origin weights')
    need(all(not sum((weights[j]*points[labels[j]][k] for j in range(4)),zero).n for k in range(3)),'origin relation')
    need(not (sum(weights,zero)-one).n,'weight normalization')
    need(any(sign(x) in (-1,1) for x in cofactors),'rank3 throughout interval')
    return weights

def active_triple(points,triple):
    normals={j:normal(x) for j,x in points.items()};ns=[normals[j] for j in triple]
    d=determinant(ns);cv=[cross(ns[1],ns[2]),cross(ns[2],ns[0]),cross(ns[0],ns[1])]
    numer=[t*sum((v[k] for v in cv),zero) for k in range(3)]
    return normals,d,numer
