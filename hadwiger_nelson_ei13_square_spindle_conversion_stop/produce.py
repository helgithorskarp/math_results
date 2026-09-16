#!/usr/bin/env python3
"""One frozen EI13 side-spindle conversion; exact arithmetic, no search over frames."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter
from pysat.solvers import Solver

P = (3, 7, 11)
N = 8
ZERO = (F(0),) * N
ONE = (F(1),) + (F(0),) * 7

def rational(x):
    return (F(x),) + (F(0),) * 7

def radical(bit):
    return tuple(F(i == 1 << bit) for i in range(N))

def add(x, y):
    return tuple(a+b for a,b in zip(x,y))

def neg(x):
    return tuple(-a for a in x)

def scale(x, a):
    return tuple(v*a for v in x)

def mul(x, y):
    z = [0]*N
    for i,a in enumerate(x):
        if not a: continue
        for j,b in enumerate(y):
            if not b: continue
            f = 1
            for k,p in enumerate(P):
                if (i & j) >> k & 1: f *= p
            z[i^j] += a*b*f
    return tuple(z)

def padd(z,w): return (add(z[0],w[0]),add(z[1],w[1]))
def psub(z,w): return (add(z[0],neg(w[0])),add(z[1],neg(w[1])))
def pscale(z,a): return (scale(z[0],a),scale(z[1],a))
def itimes(z): return (neg(z[1]),z[0])
def rtimes(z,r): return (mul(z[0],r),mul(z[1],r))
def norm(z): return add(mul(z[0],z[0]),mul(z[1],z[1]))

# Paper label order; (a+b sqrt(7),c+d sqrt(7))/4.
SOURCE_ROWS = [(2,0,2,0),(0,0,0,0),(4,0,0,0),(4,0,4,0),
 (0,0,4,0),(1,-1,3,-1),(3,1,1,1),(2,0,0,2),
 (1,-1,1,1),(0,-2,2,0),(4,2,2,0),(3,1,3,-1),(2,0,4,-2)]

def source():
    out=[]
    for a,b,c,d in SOURCE_ROWS:
        x=add(rational(F(a,4)),scale(radical(1),F(b,4)))
        y=add(rational(F(c,4)),scale(radical(1),F(d,4)))
        out.append((x,y))
    return out

def exact_edges(points,target=1):
    want=rational(target)
    return [(i,j) for i in range(len(points)) for j in range(i+1,len(points))
            if norm(psub(points[i],points[j])) == want]

def spindle(a,b):
    v=psub(b,a)
    if norm(v) != ONE: raise ValueError('nonunit spindle side')
    h=psub(pscale(padd(a,b),F(1,2)),pscale(rtimes(itimes(v),radical(2)),F(1,2)))
    out=[a,b,h]
    for x in (a,b):
        mid=pscale(padd(h,x),F(1,2))
        off=pscale(rtimes(itimes(psub(h,x)),radical(0)),F(1,6))
        out.extend((padd(mid,off),psub(mid,off)))
    if len(set(out)) != 7 or len(exact_edges(out)) != 11:
        raise ValueError('malformed spindle')
    return out

def stream(rows):
    return ''.join(','.join(map(str,row))+'\n' for row in rows).encode()

def sha(rows): return hashlib.sha256(stream(rows)).hexdigest()

def colour(n,edges,k):
    def var(v,c): return k*v+c+1
    clauses=[]
    for v in range(n):
        clauses.append([var(v,c) for c in range(k)])
        for a,b in itertools.combinations(range(k),2):
            clauses.append([-var(v,a),-var(v,b)])
    for u,v in edges:
        for c in range(k): clauses.append([-var(u,c),-var(v,c)])
    with Solver(name='cadical195',bootstrap_with=clauses) as solver:
        sat=solver.solve()
        if not sat: return None
        model=set(solver.get_model())
    word=[next(c for c in range(k) if var(v,c) in model) for v in range(n)]
    if any(word[u]==word[v] for u,v in edges): raise ValueError('bad solver word')
    return word

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args()
    t=perf_counter(); root=args.output_dir;root.mkdir(parents=True,exist_ok=True)
    src=source(); unit=exact_edges(src); diagonal=exact_edges(src,2)
    if (len(src),len(unit),len(diagonal)) != (13,20,14): raise ValueError('source counts')
    sides=[(src[i],src[j]) for i,j in unit]
    square_points=[]
    for i,j in diagonal:
        a,b=src[i],src[j]
        mid=pscale(padd(a,b),F(1,2)); off=pscale(itimes(psub(b,a)),F(1,2))
        c,d=padd(mid,off),psub(mid,off)
        square_points.extend((c,d))
        sides.extend(((a,d),(d,b),(b,c),(c,a)))
    cells=[spindle(a,b) for a,b in sides]
    points=sorted(set(src+square_points+[z for cell in cells for z in cell]))
    if len(points)>421: raise ValueError('cap failure')
    rows=[]
    for x,y in points:
        row=[v*96 for v in x+y]
        if any(v.denominator!=1 for v in row): raise ValueError('unexpected denominator')
        rows.append([int(v) for v in row])
    # A second, integral representation is used for the all-pairs decision.
    target=(96**2,)+(0,)*7
    edges=[]
    for i in range(len(rows)):
        for j in range(i+1,len(rows)):
            dx=tuple(a-b for a,b in zip(rows[i][:8],rows[j][:8]))
            dy=tuple(a-b for a,b in zip(rows[i][8:],rows[j][8:]))
            if add(mul(dx,dx),mul(dy,dy)) == target: edges.append((i,j))
    ids={p:i for i,p in enumerate(points)}
    source_ids=[ids[p] for p in src]
    inherited=set(tuple(sorted((ids[src[i]],ids[src[j]]))) for i,j in unit)
    for cell in cells:
        inherited.update(tuple(sorted((ids[cell[i]],ids[cell[j]]))) for i,j in exact_edges(cell))
    if not inherited.issubset(set(edges)): raise ValueError('missing inherited unit edge')
    (root/'points.txt').write_bytes(stream(rows));(root/'edges.txt').write_bytes(stream(edges))
    word=colour(len(points),edges,4)
    if word is None:
        (root/'NONFOUR_SIGNAL.json').write_text(json.dumps({'vertices':len(points),'edges':len(edges),'edge_sha256':sha(edges)},indent=2)+'\n')
        raise RuntimeError('NONFOUR SIGNAL: preserve graph; independent proof and five-colouring required')
    carrier_word=colour(13,unit+diagonal,5)
    if carrier_word is None: raise ValueError('carrier five-colouring failed')
    result={'schema':'ei13-side-spindle-v1','denominator':96,'bitmask_primes':list(P),
      'vertices':len(points),'edges':len(edges),'unordered_pairs':len(points)*(len(points)-1)//2,
      'point_sha256':sha(rows),'edge_sha256':sha(edges),'raw_cap':421,
      'source_unit_edges':unit,'source_diagonal_edges':diagonal,'source_ids':source_ids,
      'source_five_word':carrier_word,'spindle_occurrences':len(cells),
      'distinct_directed_sides':len(set(sides)),'square_base_vertices':len(set(src+square_points)),
      'inherited_edges':len(inherited),'incidental_edges':len(set(edges)-inherited),
      'four_word':word,'source_four_restriction':[word[i] for i in source_ids],
      'violated_carrier_diagonals':[(i,j) for i,j in diagonal if word[source_ids[i]]==word[source_ids[j]]],
      'moser_ids':[ids[p] for p in cells[0]],'record_candidate':False}
    (root/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    (root/'points.txt').write_bytes(stream(rows));(root/'edges.txt').write_bytes(stream(edges))
    (root/'producer_run.json').write_text(json.dumps({'seconds':round(perf_counter()-t,6)},indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('four_word','source_unit_edges','source_diagonal_edges')},indent=2))

if __name__=='__main__': main()
