#!/usr/bin/env python3
"""Producer-independent literal orbit/formula and edge-list verification."""
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def primary(triangles=8, red_triangles=4):
    def g(v): return 3*(v//3)+(v%3+1)%3
    left = set(combinations(range(3*triangles),2));orbits = [];edges = {}
    while left:
        e = min(left);orbit = {e};f = tuple(sorted(map(g,e)))
        while f != e:
            orbit.add(f);f = tuple(sorted(map(g,f)))
        left -= orbit
        if e[0]//3 == e[1]//3:
            for f in orbit: edges[f] = (e[0]//3 < red_triangles)
        else:
            orbits.append(orbit)
    orbits.sort(key=min)
    for v,orbit in enumerate(orbits,1):
        for e in orbit: edges[e] = v
    return edges


def check_cases(cases):
    old = json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_blue4'/'result.json').read_text())
    expected = [{k:c[k] for k in ('index','bits','labeled','omitted')} for c in old['cases'] if c['status']=='open']
    need(cases == expected and [c['index'] for c in cases] == [124,155,159,168,180,194], 'complete six-case identity')
    return dict(cores=6, labeled=sum(c['labeled'] for c in cases))


def check_formula(path, case):
    edges = primary();rows = set();counts = {}
    for size, sign, wanted in ((4,1,False),(5,-1,True)):
        covered = 0
        for vertices in combinations(range(24),size):
            colors = [edges[e] for e in combinations(vertices,2)]
            if any(type(c) is bool and c != wanted for c in colors): continue
            rows.add(tuple(sorted({sign*c for c in colors if type(c) is int})));covered += 1
        counts[str(size)] = covered
    expected = sorted(rows)
    ids = [edges[3*i,3*j+d] for i,j in combinations(range(4),2) for d in range(3)]
    need(ids == [1,2,3,4,5,6,7,8,9,22,23,24,25,26,27,40,41,42], 'local core primary IDs')
    expected.extend((v if bit=='1' else -v,) for v,bit in zip(ids,case['bits']))
    with path.open() as f:
        need(f.readline() == f'p cnf 84 {len(expected)}\n', 'exact header')
        for row in expected: need(f.readline() == ' '.join(map(str,row))+' 0\n', 'literal clique/core clause')
        need(not f.read(), 'exact EOF; no local or global normalizers')
    return dict(variables=84, clauses=len(expected), primary_edges=len(edges), ramsey_clauses=len(rows),
                unsimplified_nonconstant_subsets=counts, core_units=18, normalization_clauses=0)


def read_edges(path):
    rows = path.read_text().splitlines();need(bool(rows), 'nonempty edge list')
    header = rows[0].split();need(len(header)==2, 'two header fields')
    n,m = map(int,header);need(n==24 and len(rows)==m+1, 'exact edge count')
    result = set()
    for line in rows[1:]:
        parts = line.split();need(len(parts)==2, 'two edge endpoints')
        a,b = map(int,parts);need(0<=a<b<n and (a,b) not in result, 'valid distinct undirected edge')
        result.add((a,b))
    return n,result


def clique_count(n, red, size, color):
    return sum(all(((a,b) in red)==color for a,b in combinations(vertices,2))
               for vertices in combinations(range(n),size))


def check_graph(path, case):
    n,red = read_edges(path)
    need(clique_count(n,red,5,True)==0, 'red K5')
    need(clique_count(n,red,4,False)==0, 'blue K4')
    def g(v): return 3*(v//3)+(v%3+1)%3
    for a,b in combinations(range(24),2):
        need(((a,b) in red)==(tuple(sorted((g(a),g(b)))) in red), 'order-three invariance')
        if a//3 == b//3: need(((a,b) in red)==(a//3<4), 'internal triangle colors')
    word = ''.join('1' if (3*i,3*j+d) in red else '0'
                   for i,j in combinations(range(4),2) for d in range(3))
    need(word==case['bits'], 'literal red core')
    degrees = [sum((min(a,b),max(a,b)) in red for b in range(n) if a!=b) for a in range(n)]
    return dict(vertices=n, red_edges=len(red), red_K5=0, blue_K4=0,
                order_three=True, internal_red_triangles=4, internal_blue_triangles=4,
                red_degrees=degrees, core_bits=word,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--edges', type=Path, required=True)
    p.add_argument('--bits', required=True, help='18 core bits in pair order 01,02,03,12,13,23')
    a = p.parse_args()
    need(len(a.bits)==18 and set(a.bits)<={'0','1'}, '18 binary core bits')
    print(json.dumps(check_graph(a.edges, dict(bits=a.bits)), indent=2, sort_keys=True))
