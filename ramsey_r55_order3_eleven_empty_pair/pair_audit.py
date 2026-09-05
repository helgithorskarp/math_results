#!/usr/bin/env python3
"""Literal pair orbits, complete formula bridge, local fixtures and clause controls."""
from itertools import combinations, product
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def primary():
    def move(v):
        return 3*(v//3)+(v+1) % 3 if v < 33 else v
    classes = set()
    for a, b in combinations(range(43), 2):
        if b < 33 and a//3 == b//3:
            continue
        orbit = []
        for _ in range(3):
            orbit.append(tuple(sorted((a, b))))
            a, b = move(a), move(b)
        classes.add(min(orbit))
    cross = sorted(p for p in classes if p[1] < 33)
    fixed = sorted(p for p in classes if p[0] >= 33)
    links = sorted((p for p in classes if p[0] < 33 <= p[1]), key=lambda p: p[::-1])
    require((len(cross), len(fixed), len(links)) == (165, 45, 110), 'primary census')
    return {p: i+1 for i, p in enumerate(cross+fixed+links)}


def expected(color):
    ids = primary()
    if color == 'red':
        return [(ids[33, 34],)]
    require(color == 'blue', 'color')
    clauses = {(-ids[33, 34],)}
    def add(row):
        clauses.add(tuple(sorted(row)))
    for t in range(9, 33, 3):
        add([ids[t, 33], ids[t, 34]])
    for f in range(35, 43):
        for omitted in combinations((0, 3, 6), 2):
            add([ids[33, f], ids[34, f]]+[ids[t, f] for t in omitted])
    for triple in combinations(range(35, 43), 3):
        add([ids[u, f] for u in (33, 34) for f in triple])
    for t in (0, 3, 6):
        for f, g in combinations(range(35, 43), 2):
            add([ids[u, v] for u in (33, 34) for v in (f, g)]+[ids[t, f], ids[t, g]])
    return sorted(clauses, key=lambda c: (len(c), c))


def audit(base, path, color):
    tail = expected(color)
    with base.open('rb') as a, path.open('rb') as b:
        _, _, nv, nc = a.readline().split()
        nv, nc = int(nv), int(nc)
        require((nv, nc) == (34268, 617207), 'full many-empty base dimensions')
        require(b.readline() == f'p cnf {nv} {nc+len(tail)}\n'.encode(), 'new header')
        for _ in range(nc):
            line = a.readline()
            require(line and b.readline() == line, 'entire original prefix')
        require(not a.read(), 'base EOF')
        for row in tail:
            require(b.readline() == (' '.join(map(str, row))+' 0\n').encode(), 'pair consequence clause')
        require(not b.read(), 'final EOF')
    return dict(variables=nv, clauses=nc+len(tail), appended_clauses=len(tail), complete_prefix=True)


def read_graph(text):
    lines = text.splitlines()
    n, m = map(int, lines[0].split())
    edges = [tuple(map(int, s.split())) for s in lines[1:]]
    require(n == 13 and len(edges) == m and len(set(edges)) == m, 'fixture dimensions/duplicates')
    require(all(0 <= a < b < n for a, b in edges), 'fixture pair')
    return n, set(edges)


def inspect(text, core):
    n, red = read_graph(text)
    def r(a, b):
        return tuple(sorted((a, b))) in red
    counts = [0, 0]
    for five in combinations(range(n), 5):
        colors = {r(a, b) for a, b in combinations(five, 2)}
        if len(colors) == 1:
            counts[int(next(iter(colors)))] += 1
    require(counts == [0, 0], 'monochromatic K5')
    signatures = []
    for f in range(9, 13):
        row = []
        for i in range(3):
            bits = {r(t, f) for t in range(3*i, 3*i+3)}
            require(len(bits) == 1, 'nonuniform attachment')
            row.append(int(bits.pop()))
        signatures.append(sum(bit << i for i, bit in enumerate(row)))
    require(signatures == [0, 0, 3, 5], 'fixture signatures')
    require(not r(9, 10) and all(not r(u, f) for u in (9, 10) for f in (11, 12)), 'sharp common blue neighborhood')
    code = ''.join(str(int(r(3*i, 3*j+t))) for i, j in ((0, 1), (0, 2), (1, 2)) for t in range(3))
    require(code == {11: '100110110', 13: '110110101'}[core], 'core convention')
    def move(v):
        return 3*(v//3)+(v+1) % 3 if v < 9 else v
    require(all(r(a, b) == r(move(a), move(b)) for a, b in combinations(range(n), 2)), 'full local action')
    require(all(r(a, b) for t in (0, 3, 6) for a, b in combinations(range(t, t+3), 2)), 'internal red triangles')
    return dict(core=core, vertices=n, red_edges=len(red), five_sets_checked=1287,
                action_pairs_checked=78, signatures=signatures, common_blue_fixed=2, ramsey=True)


def controls(producer, work):
    work.mkdir(parents=True, exist_ok=True)
    ids = primary()
    for color in ('red', 'blue'):
        require(producer.tail(color) == expected(color), 'producer binding match')
    require(expected('blue')[0] == (-166,) and expected('red') == [(166,)], 'disjoint complete color split')
    tallies = {}
    for kind, variables in [('majority', 2), ('signature', 4), ('common_cap', 6), ('omitted', 6)]:
        total = 0
        for bits in product((0, 1), repeat=variables):
            clause = any(bits)
            if kind == 'majority':
                forbidden = bits == (0, 0)
            elif kind == 'signature':
                common = not bits[0] and not bits[1]
                forbidden = common and not any(bits[2:])
            elif kind == 'common_cap':
                forbidden = sum(not bits[2*i] and not bits[2*i+1] for i in range(3)) > 2
            else:
                forbidden = not any(bits[:4]) and not any(bits[4:])
            require(clause != forbidden, 'clause semantic control')
            total += 1
        tallies[kind] = total
    # The intersection fact in the hand proof, independently over bit sets.
    large = [set(i for i in range(3) if s >> i & 1) for s in range(8) if s.bit_count() >= 2]
    require(all(a & b for a, b in product(large, repeat=2)), 'two-of-three intersection')
    fixtures = []
    for core in (11, 13):
        data = producer.fixture(core)
        path = work / f'core{core}.edges'
        path.write_text(data)
        fixtures.append(inspect(data, core))
    bad = producer.fixture(11)
    lines = bad.splitlines()
    mutated = '\n'.join([lines[0]]+lines[1:]+[lines[1]])+'\n'
    rejected = []
    for name, data in [('duplicate_edge', mutated), ('wrong_order', bad.replace('13 ', '14 ', 1))]:
        try:
            inspect(data, 11)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('fixture mutation accepted')
    n, red = read_graph(bad)
    red |= set(combinations(range(5), 2))
    planted = f'{n} {len(red)}\n'+''.join(f'{a} {b}\n' for a, b in sorted(red))
    try:
        inspect(planted, 11)
    except ValueError:
        rejected.append('planted_red_five')
    else:
        raise ValueError('planted K5 accepted')
    return dict(primary_variables=len(ids), blue_clauses=173, red_clauses=1,
                family_counts=dict(color=1, majority=8, signature=24, common_cap=56, omitted=84),
                truth_assignments=tallies, intersection_pairs=16, fixtures=fixtures,
                rejected_fixture_mutations=rejected)


if __name__ == '__main__':
    from pathlib import Path
    import argparse
    import pair_model
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    result = controls(pair_model, a.work)
    (a.work / 'pair_controls.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
