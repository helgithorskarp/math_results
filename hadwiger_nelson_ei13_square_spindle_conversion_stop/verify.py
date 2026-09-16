#!/usr/bin/env python3
"""Solver-free exact verifier. Imports no producer or other package executable."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import gcd
from pathlib import Path
import json

# Independent actual-radicand representation, not the producer's bitmask order.
RAD = (1, 3, 7, 11, 21, 33, 77, 231)
INDEX = {r:i for i,r in enumerate(RAD)}
PUBLISHED_RAD = (1, 3, 7, 21, 11, 33, 77, 231)
ZERO = (0,)*8

def require(test, message):
    if not test: raise ValueError(message)

def scalar(x): return (x,)+(0,)*7
def add(x,y): return tuple(a+b for a,b in zip(x,y))
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def times(x,n): return tuple(a*n for a in x)
def radical(r,n=1): return tuple(n if x==r else 0 for x in RAD)

def multiply(x,y):
    out=[0]*8
    for i,a in enumerate(x):
        if not a: continue
        for j,b in enumerate(y):
            if not b: continue
            g=gcd(RAD[i],RAD[j])
            r=RAD[i]*RAD[j]//(g*g)
            out[INDEX[r]] += a*b*g
    return tuple(out)

def complex_multiply(z,w):
    x,y=z; u,v=w
    return sub(multiply(x,u),multiply(y,v)),add(multiply(x,v),multiply(y,u))

def plus(z,w): return add(z[0],w[0]),add(z[1],w[1])
def minus(z,w): return sub(z[0],w[0]),sub(z[1],w[1])
def scaled(z,n): return times(z[0],n),times(z[1],n)
def half(z):
    require(all(v%2==0 for part in z for v in part),'nonintegral half')
    return tuple(tuple(v//2 for v in part) for part in z)
def quarterturn(z): return times(z[1],-1),z[0]
def norm(z): return add(multiply(z[0],z[0]),multiply(z[1],z[1]))
def isunit(z,w,den): return norm(minus(z,w))==scalar(den*den)

# These are precisely the paper's (a+b sqrt(7),c+d sqrt(7))/4 rows.
SOURCE = ((2,0,2,0),(0,0,0,0),(4,0,0,0),(4,0,4,0),(0,0,4,0),
          (1,-1,3,-1),(3,1,1,1),(2,0,0,2),(1,-1,1,1),(0,-2,2,0),
          (4,2,2,0),(3,1,3,-1),(2,0,4,-2))
UNIT = ((0,5),(0,6),(0,8),(0,11),(1,2),(1,4),(1,8),(2,3),(2,6),
        (3,4),(3,11),(4,5),(5,9),(5,12),(6,7),(6,10),(7,8),(8,9),
        (10,11),(11,12))
DIAGONAL = ((1,3),(1,7),(1,9),(1,11),(2,4),(2,5),(2,7),(2,10),
            (3,8),(3,10),(3,12),(4,6),(4,9),(4,12))

def source_points():
    # Denominator 8, so the midpoints of both diagonals remain integral.
    return [(add(scalar(2*a),radical(7,2*b)),
             add(scalar(2*c),radical(7,2*d))) for a,b,c,d in SOURCE]

def template():
    # Direct expanded coordinates with denominator 12 for a spindle on 0 -> 1.
    # They are independently derived from |H|=|H-1|=sqrt(3), H_y<0.
    s3=radical(3); s11=radical(11); s33=radical(33)
    return [(ZERO,ZERO),(scalar(12),ZERO),(scalar(6),times(s11,-6)),
       (add(scalar(3),s33),add(times(s11,-3),s3)),
       (sub(scalar(3),s33),sub(times(s11,-3),s3)),
       (add(scalar(9),s33),sub(times(s11,-3),s3)),
       (sub(scalar(9),s33),add(times(s11,-3),s3))]

def published_row(z):
    return tuple(z[k][INDEX[r]] for k in (0,1) for r in PUBLISHED_RAD)

def digest(rows):
    return sha256(''.join(','.join(map(str,r))+'\n' for r in rows).encode()).hexdigest()

def geometry():
    src=source_points()
    observed_unit=tuple((i,j) for i,j in combinations(range(13),2) if isunit(src[i],src[j],8))
    observed_diagonal=tuple((i,j) for i,j in combinations(range(13),2)
                            if norm(minus(src[i],src[j]))==scalar(128))
    require(observed_unit==UNIT and observed_diagonal==DIAGONAL,'paper edge list mismatch')
    base=set(src); sides=[(src[i],src[j]) for i,j in UNIT]
    for i,j in DIAGONAL:
        a,b=src[i],src[j]; m=half(plus(a,b)); q=half(quarterturn(minus(b,a)))
        c,d=plus(m,q),minus(m,q)
        base.update((c,d))
        sides.extend(((a,d),(d,b),(b,c),(c,a)))
    require(len(sides)==76,'side occurrence count')
    local=template()
    local_edges=[(i,j) for i,j in combinations(range(7),2) if isunit(local[i],local[j],12)]
    require(len(set(local))==7 and len(local_edges)==11,'local exact spindle')
    physical={scaled(p,12) for p in base}
    cells=[]
    for a,b in sides:
        require(isunit(a,b,8),'nonunit base side')
        v=minus(b,a)
        cell=[plus(scaled(a,12),complex_multiply(v,t)) for t in local]
        require(len(set(cell))==7,'spindle collision')
        physical.update(cell);cells.append(cell)
    points=sorted(physical,key=published_row)
    require(len(points)<=421,'raw cap')
    point_rows=[published_row(p) for p in points]
    ids={p:i for i,p in enumerate(points)}
    source_ids=[ids[scaled(p,12)] for p in src]
    edges=[(i,j) for i,j in combinations(range(len(points)),2) if isunit(points[i],points[j],96)]
    inherited={tuple(sorted((source_ids[i],source_ids[j]))) for i,j in UNIT}
    for cell in cells:
        inherited.update(tuple(sorted((ids[cell[i]],ids[cell[j]]))) for i,j in local_edges)
    require(inherited.issubset(edges),'lost inherited edge')
    return {'points':points,'point_rows':point_rows,'edges':edges,'source_ids':source_ids,
      'moser_ids':[ids[p] for p in cells[0]],'source_unit_edges':[list(e) for e in UNIT],
      'source_diagonal_edges':[list(e) for e in DIAGONAL],
      'local_edges':local_edges,'spindle_occurrences':len(cells),
      'distinct_directed_sides':len(set(sides)),'square_base_vertices':len(base),
      'inherited_edges':len(inherited),'incidental_edges':len(set(edges)-inherited)}

def canonical_count(n,edges,k):
    """Exhaustive fixed-order restricted-growth enumeration, no solver dependency."""
    adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    order=sorted(range(n),key=lambda v:(-len(adj[v]),v))
    word=[-1]*n; leaves=0; visits=0
    def visit(pos,largest):
        nonlocal leaves,visits
        visits+=1
        if pos==n: leaves+=1;return
        v=order[pos]; forbidden={word[u] for u in adj[v] if word[u]>=0}
        for c in range(min(k-1,largest+1)+1):
            if c not in forbidden:
                word[v]=c;visit(pos+1,max(largest,c));word[v]=-1
    visit(0,-1)
    return leaves,visits

def check_word(word,n,edges,k,label):
    require(isinstance(word,list) and len(word)==n,label+' length')
    require(all(type(c) is int and 0<=c<k for c in word),label+' alphabet')
    require(all(word[i]!=word[j] for i,j in edges),label+' improper edge')

def verify(certificate,geom=None):
    g=geometry() if geom is None else geom
    n=len(g['points']);edges=g['edges']
    expected={'schema':'ei13-side-spindle-v1','denominator':96,'bitmask_primes':[3,7,11],
      'vertices':n,'edges':len(edges),'unordered_pairs':n*(n-1)//2,
      'point_sha256':digest(g['point_rows']),'edge_sha256':digest(edges),
      'raw_cap':421,'record_candidate':False}
    for key in ('source_ids','source_unit_edges','source_diagonal_edges','moser_ids',
        'spindle_occurrences','distinct_directed_sides','square_base_vertices',
        'inherited_edges','incidental_edges'):
        expected[key]=g[key]
    for k,v in expected.items(): require(certificate.get(k)==v,'certificate field '+k)
    word=certificate.get('four_word')
    check_word(word,n,edges,4,'physical four-word')
    check_word(certificate.get('source_five_word'),13,UNIT+DIAGONAL,5,'carrier five-word')
    restricted=[word[i] for i in g['source_ids']]
    require(certificate.get('source_four_restriction')==restricted,'source restriction')
    failed=[list((i,j)) for i,j in DIAGONAL if restricted[i]==restricted[j]]
    require(failed and certificate.get('violated_carrier_diagonals')==failed,'failed diagonals')
    carrier_count,carrier_visits=canonical_count(13,UNIT+DIAGONAL,4)
    require(carrier_count==0,'two-distance carrier four-colours')
    mids=g['moser_ids'];lower_edges=[(i,j) for i,j in combinations(range(7),2)
                                  if tuple(sorted((mids[i],mids[j]))) in edges]
    require(lower_edges==g['local_edges'],'embedded spindle edge identity')
    lower_count,lower_visits=canonical_count(7,lower_edges,3)
    four_count,_=canonical_count(7,lower_edges,4)
    require(lower_count==0 and four_count==16,'spindle colour count')
    return {'schema':expected['schema'],'vertices':n,'edges':len(edges),
      'unordered_pairs_checked':expected['unordered_pairs'],'point_sha256':expected['point_sha256'],
      'edge_sha256':expected['edge_sha256'],'chromatic_number':4,
      'four_colour_class_sizes':sorted(Counter(word).values()),
      'raw_cap':421,'spindle_occurrences':g['spindle_occurrences'],
      'distinct_directed_sides':g['distinct_directed_sides'],
      'square_base_vertices':g['square_base_vertices'],'inherited_edges':g['inherited_edges'],
      'incidental_edges':g['incidental_edges'],'source_chromatic_number_two_distance':5,
      'carrier_canonical_four_colourings':carrier_count,'carrier_recursion_visits':carrier_visits,
      'embedded_spindle_canonical_three_colourings':lower_count,
      'embedded_spindle_canonical_four_colourings':four_count,'spindle_recursion_visits':lower_visits,
      'source_four_restriction':restricted,'violated_carrier_diagonals_zero_based':failed,
      'record_candidate':False,'scope':'one frozen EI13 directed-square side-spindle conversion'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,
        default=Path(__file__).with_name('certificate.json'))
    p.add_argument('--write-graph',type=Path);a=p.parse_args()
    c=json.loads(a.certificate.read_text())
    g=geometry();result=verify(c,g)
    if a.write_graph is not None:
        a.write_graph.mkdir(parents=True,exist_ok=True)
        for name,rows in [('points.txt',g['point_rows']),('edges.txt',g['edges'])]:
            (a.write_graph/name).write_text(''.join(','.join(map(str,r))+'\n' for r in rows))
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
