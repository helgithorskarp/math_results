#!/usr/bin/env python3
"""Produce the C0 star certificate with Groebner algebra and event-owned edges."""
import argparse
import json
import time
from collections import defaultdict
from pathlib import Path
import algebra as A
import physical


def colour(n,edges,triangle):
    from pysat.solvers import Solver
    var = lambda v,c:3*v+c+1
    cnf = [[var(v,c) for c in range(3)] for v in range(n)]
    cnf += [[-var(v,a),-var(v,b)] for v in range(n) for a in range(3) for b in range(a)]
    cnf += [[-var(a,c),-var(b,c)] for a,b in edges for c in range(3)]
    cnf += [[var(v,c)] for c,v in enumerate(triangle)]
    with Solver(name='cadical153',bootstrap_with=cnf) as solver:
        A.need(solver.solve(),'NO THREE-COLOUR WITNESS: investigate before claiming a lower bound')
        model = set(k for k in solver.get_model() if k>0)
    word = [next(c for c in range(3) if var(v,c) in model) for v in range(n)]
    physical.check_word(word,n,edges)
    return word


def produce(residual):
    _,_,factors,owners,base,_,_,_ = A.architecture.build()
    pairs = A.select(residual,factors)
    x,y,s = A.sp.symbols('x y s')
    data,sources,pair_rows = {},defaultdict(list),[]
    for a,b in pairs:
        f,g = [A.expression(factors[i],x,y) for i in (a,b)]
        keys = []
        for q,xx,yy in A.groebner_components(f,g,x,y,s):
            nreal = int(q.count_roots(-A.sp.oo,A.sp.oo))
            if not nreal:
                continue
            c = A.encode(q,xx,yy,s)
            ev = A.evaluator(c)
            A.need(ev(factors[a]) and ev(factors[b]),'component substitution')
            key = A.digest(c)
            data[key] = dict(c,real_embeddings=nreal)
            sources[key].append([a,b])
            keys.append(key)
        A.need(len(keys)==len(set(keys)),'duplicate component in pair')
        pair_rows.append({'pair':[a,b],'components':sorted(keys)})
    records = []
    for key in sorted(data):
        c = data[key]
        evaluates = A.evaluator(c)
        active = [i for i,f in enumerate(factors) if evaluates(f)]
        points,label_map = physical.coordinates(c)
        edges = sorted({tuple(sorted((label_map[a],label_map[b]))) for a,b in base+[e for i in active for e in owners[i]]})
        A.need(all(a!=b for a,b in edges),'event unit edge collapsed to a loop')
        edges = [list(e) for e in edges]
        triangle = [label_map[i] for i in (0,81,162)]
        word = colour(len(points),edges,triangle)
        records.append(dict(c,key=key,source_pairs=sorted(sources[key]),active_curves=active,
                            point_count=len(points),edge_count=len(edges),edge_sha256=A.digest(edges),
                            label_map_sha256=A.digest(label_map),three_colouring=word))
    return {'schema':'hn-radix-c0-physical-star-v1','source_residual_sha256':A.RESIDUAL_HASH,
            'curve_inventory_sha256':A.digest(factors),'pairs':pair_rows,'components':records}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--residual',type=Path);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();start=time.monotonic();result=produce(args.residual)
    args.out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'pairs':len(result['pairs']),'components':len(result['components']),
                      'real_parameters':sum(c['real_embeddings'] for c in result['components']),
                      'certificate_sha256':__import__('hashlib').sha256(args.out.read_bytes()).hexdigest(),
                      'seconds':time.monotonic()-start},indent=2))
