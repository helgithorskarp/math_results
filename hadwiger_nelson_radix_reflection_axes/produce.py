#!/usr/bin/env python3
"""Produce monic factor blocks with FLINT and colour complete event graphs."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys
import flint
import sympy as S
import exact as X

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'hadwiger_nelson_complex_radix_architecture'))
import geometry as G


def inventory():
    rows, edge_lists = G.inventory()
    circle = G.primitive({(2,0):1, (0,2):3, (0,0):-1})
    events = {G.distance_event(r):(r,es) for r,es in zip(rows,edge_lists) if sum(x != (0,0) for x in r) >= 2}
    factors = sorted(list(events)+[circle])
    base = next(es for r,es in zip(rows,edge_lists) if r == G.canon(((1,0),(0,0),(0,0),(0,0),(0,0))))
    data = {i:events[f] for i,f in enumerate(factors) if f != circle}
    special = []
    for f in factors:
        q = [0]*(1+max(i for i,j,c in f))
        for i,j,c in f:
            if j == 0:
                q[i] += c
        q = X.trim(q)
        X.need(q[-1] == 1, 'monic real-axis norm polynomial')
        special.append(tuple(q))
    return factors, factors.index(circle), data, base, special


def modular_audit(blocks):
    tables = {p:[flint.nmod_poly(list(g),p) for g in blocks] for p in X.PRIMES}
    histogram, trace = Counter(), hashlib.sha256()
    for i,j in combinations(range(len(blocks)),2):
        for prime in X.PRIMES:
            if tables[prime][i].gcd(tables[prime][j]).degree() == 0:
                histogram[prime] += 1
                trace.update(f'{i},{j},{prime}\n'.encode())
                break
        else:
            raise ValueError('pair needs another exact coprimality certificate')
    squarefree = []
    for i,g in enumerate(blocks):
        prime = next(p for p in X.PRIMES if tables[p][i].gcd(flint.nmod_poly(X.derivative(g),p)).degree() == 0)
        squarefree.append(prime)
    return {'pair_checks':sum(histogram.values()), 'prime_histogram':{str(p):n for p,n in sorted(histogram.items())},
            'pair_trace_sha256':trace.hexdigest(), 'squarefree_primes_sha256':X.digest(squarefree)}


def make_certificate():
    factors,circle,data,base,special = inventory()
    unique = sorted(set(special))
    decompositions, all_blocks = {}, set()
    for f in unique:
        content, terms = flint.fmpz_poly(list(f)).factor()
        X.need(int(content) == 1, 'monic factorization content')
        terms = [(tuple(map(int,g)),int(e)) for g,e in terms]
        product = flint.fmpz_poly([1])
        for g,e in terms:
            all_blocks.add(g)
            product *= flint.fmpz_poly(list(g))**e
        X.need(tuple(map(int,product)) == f, 'exact factorization product')
        decompositions[f] = terms
    blocks = sorted(all_blocks)
    block_id = {g:i for i,g in enumerate(blocks)}
    factorizations = [sorted((block_id[g],e) for g,e in decompositions[f]) for f in unique]
    event_blocks = [{block_id[g] for g,e in decompositions[f]} for f in special]
    colourings = [[sum(a*b for a,b in zip(w,label)) % 3 for label in G.LABELS] for w in X.WEIGHTS]
    colours, real_roots, event_lists = [], [], []
    x = S.Symbol('x')
    for i,g in enumerate(blocks):
        events = [c for c,bs in enumerate(event_blocks) if i in bs]
        event_lists.append(events)
        if len(g) <= 5:
            colours.append(None)
            real_roots.append(None)
            continue
        edges = set(base).union(*(set(data[c][1]) for c in events))
        valid = [k for k,w in enumerate(colourings) if all(w[u] != w[v] for u,v in edges)]
        X.need(valid, 'one of the four physical three-colour words must work')
        colours.append(valid[0])
        real_roots.append(int(S.Poly.from_list(list(reversed(g)),x).count_roots(-S.oo,S.oo)))
    audit = modular_audit(blocks)
    high = [i for i,g in enumerate(blocks) if len(g)>5]
    higher = [i for i in high if len(event_lists[i])>=5 and real_roots[i]]
    result = {
        'active_curves':len(factors), 'unique_real_axis_norm_polynomials':len(unique),
        'monic_blocks':len(blocks), 'block_degree_histogram':{str(d):n for d,n in sorted(Counter(len(g)-1 for g in blocks).items())},
        'low_degree_blocks_closed_by_h4119':len(blocks)-len(high), 'higher_degree_blocks':len(high),
        'higher_block_colour_histogram':{str(k):n for k,n in sorted(Counter(colours[i] for i in high).items())},
        'higher_blocks_with_real_roots':sum(bool(real_roots[i]) for i in high),
        'higher_block_real_roots':sum(real_roots[i] for i in high),
        'higher_block_incidence_histogram':{str(k):n for k,n in sorted(Counter(len(event_lists[i]) for i in high).items())},
        'higher_incidence_real_blocks':[{'block_id':i,'polynomial':blocks[i],'curves':event_lists[i],
                                       'real_roots':real_roots[i],'colour_index':colours[i]} for i in higher],
        'coprimality':audit, 'all_reflection_axis_members_chromatic_number':3,
        'eight_active_gate_closed':False, 'record_improvement':False,
    }
    return {'schema':'hn-radix-reflection-axis-v1','curve_inventory_sha256':X.digest(factors),
            'real_norm_inventory_sha256':X.digest(unique),'blocks':blocks,'factorizations':factorizations,
            'colour_assignments':colours,'real_root_counts':real_roots,'result':result}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    certificate=make_certificate()
    with args.out.open('x') as f:
        json.dump(certificate,f,sort_keys=True,separators=(',',':'))
        f.write('\n')
    print(json.dumps(certificate['result'],indent=2,sort_keys=True))


if __name__=='__main__':
    main()
