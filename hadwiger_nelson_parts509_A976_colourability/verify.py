#!/usr/bin/env python3
"""Fresh exact geometry and positive certificate audit; no solver imports.

Coefficient multiplication expands monomial exponents in sqrt(3), sqrt(5),
sqrt(11). This file imports neither the producer nor earlier arithmetic.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
POWERS = [(i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8)]
INDEX = {p: i for i, p in enumerate(POWERS)}
PRIMES = (3, 5, 11)
UNIT = (288**2,) + (0,) * 7


def require(ok, message):
    if not ok:
        raise ValueError(message)


def multiply(left, right):
    result = [0] * 8
    for powers, x in zip(POWERS, left):
        if not x:
            continue
        for other, y in zip(POWERS, right):
            if not y:
                continue
            exponents = [a + b for a, b in zip(powers, other)]
            coefficient = x * y
            for prime, exponent in zip(PRIMES, exponents):
                coefficient *= prime ** (exponent // 2)
            result[INDEX[tuple(e % 2 for e in exponents)]] += coefficient
    return tuple(result)


def distance(a, b):
    x, y = [tuple(u - v for u, v in zip(a[j], b[j])) for j in (0, 1)]
    return tuple(u + v for u, v in zip(multiply(x, x), multiply(y, y)))


def no_sqrt5(point):
    return all(point[axis][i] == 0 for axis in (0, 1) for i in (2, 3, 6, 7))


def read_points():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in {**manifest['coordinate_inputs'], **manifest['corollary_inputs']}.items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == digest, ('input identity', name))
    require(sha256((HERE / 'certificate.json').read_bytes()).hexdigest() == manifest['certificate_sha256'], 'certificate identity')
    points = {}
    rows = [s for s in (REPO / 'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines()
            if s and not s.startswith('#')]
    require(len(rows) == 509, 'original point count')
    for v, row in enumerate(rows):
        values = [3 * int(x) for x in row.split()]
        require(len(values) == 16, 'coordinate width')
        points[v] = (tuple(values[:8]), tuple(values[8:]))
    pool = json.loads((REPO / 'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    require(len(pool) == 1158, 'sealed completion table count')
    for i, row in enumerate(pool):
        axes = []
        for axis in ('x', 'y'):
            scaled = [288 * Fraction(x) for x in row[axis]]
            require(len(scaled) == 8 and all(x.denominator == 1 for x in scaled), 'completion scaling')
            axes.append(tuple(x.numerator for x in scaled))
        points[509 + i] = tuple(axes)
    return points, pool


def check_colour(vertices, edges, colouring):
    require(len(colouring) == len(vertices) and set(colouring) <= set('0123'), 'colour domain')
    colours = dict(zip(vertices, map(int, colouring)))
    require(all(colours[u] != colours[v] for u, v in edges), 'monochromatic edge')
    return colours


def audit(compare_cnf=None):
    start = time.monotonic()
    points, pool = read_points()
    original_A = [v for v in range(509) if no_sqrt5(points[v])]
    require(original_A == list(range(374)), 'original large side')
    candidates = [v for v in range(509, 509 + len(pool)) if no_sqrt5(points[v])]
    added, hist = [], Counter()
    for v in candidates:
        neighbours = [u for u in range(509) if distance(points[u], points[v]) == UNIT]
        require(neighbours == pool[v - 509]['neighbors'], ('completion incidence table', v))
        hist[len(neighbours)] += 1
        if len(neighbours) >= 4:
            added.append(v)
    vertices = original_A + added
    require(len(added) == 602 and len(vertices) == len({points[v] for v in vertices}) == 976, 'exact support')
    require(len({points[v] for v in vertices + list(range(374, 509))}) == 1111, 'composition support distinctness')
    edges = [(u, v) for u, v in combinations(vertices, 2) if distance(points[u], points[v]) == UNIT]
    require(len(edges) == 6406, 'unit edge count')
    cert = json.loads((HERE / 'certificate.json').read_text())
    require(cert['vertices'] == vertices, 'certificate support')
    cols = check_colour(vertices, edges, cert['colouring'])
    require(cols[0] == 0, 'colour normalization')
    # Only a positive restriction is checked here; no old UNSAT proof is rerun.
    old = json.loads((REPO / 'hadwiger_nelson_parts509_rigid_block_core_pilot/certificate.json').read_text())
    T = old['selected']
    require(T == sorted(set(T)) and len(T) == 870 and set(T) <= set(vertices), 'old support containment')
    peeled = sorted(set(T) - {r['v'] for r in old['peeling']})
    require(len(peeled) == 869, 'old peeled support')
    interface = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    require(set(interface['interface_L']) <= set(peeled), 'old interface retained')
    boundary_pattern = [cols[v] for v in interface['interface_L_nonorigin']]
    rename = {0: 0}
    for c in boundary_pattern:
        if c not in rename:
            rename[c] = len(rename)
    canonical = ''.join(str(rename[c]) for c in boundary_pattern)
    require(canonical in [r['class'] for r in interface['classes']], 'realized old boundary class')
    bad = list(cert['colouring'])
    u, v = edges[0]
    bad[vertices.index(v)] = bad[vertices.index(u)]
    rejected = False
    try:
        check_colour(vertices, edges, ''.join(bad))
    except ValueError as error:
        require(str(error) == 'monochromatic edge', 'bad certificate rejection reason')
        rejected = True
    require(rejected, 'improper certificate accepted')
    cross = [(u, v) for u in vertices for v in range(374, 509) if distance(points[u], points[v]) == UNIT]
    boundary = sorted({u for u, v in cross})
    require(len(cross) == 36 and len(boundary) == 25, 'full composition boundary')
    interior = set(vertices) - set(boundary)
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    components = []
    while interior:
        seed = min(interior)
        queue = deque([seed])
        interior.remove(seed)
        component = {seed}
        while queue:
            v = queue.popleft()
            for u in sorted(adjacency[v] & interior):
                interior.remove(u)
                component.add(u)
                queue.append(u)
        neighbours = sorted(set().union(*(adjacency[v] for v in component)) & set(boundary))
        components.append(dict(vertices=len(component), boundary_neighbours=neighbours))
    require(components == [dict(vertices=951, boundary_neighbours=boundary)], 'interior component result')
    pos = {v: i for i, v in enumerate(vertices)}
    rows = [[4*i+c+1 for c in range(4)] for i in range(len(vertices))]
    for u, v in edges:
        for c in range(4):
            rows.append([-4*pos[u]-c-1, -4*pos[v]-c-1])
    rows.append([1])
    raw = (f'p cnf {4*len(vertices)} {len(rows)}\n'+''.join(' '.join(map(str,r))+' 0\n' for r in rows)).encode()
    if compare_cnf is not None:
        require(raw == compare_cnf.read_bytes(), 'entrywise CNF comparison')
    result = dict(status='A976 AND EVERY SUBGRAPH FOUR-COLOURABLE', vertices=len(vertices), unit_edges=len(edges),
                  colouring_sha256=sha256(cert['colouring'].encode()).hexdigest(),
                  edge_sha256=sha256(''.join(f'{u},{v}\n' for u,v in edges).encode()).hexdigest(),
                  unordered_A_pairs_checked=len(vertices)*(len(vertices)-1)//2,
                  field_completion_candidates=len(candidates), completion_incidence_pairs_checked=509*len(candidates),
                  field_completion_degree_histogram=dict(sorted(hist.items())), added_vertices=len(added),
                  cross_pair_checks=976*135, cross_edges=cross, boundary=boundary, interior_components=components,
                  cnf_variables=3904, cnf_clauses=len(rows), cnf_sha256=sha256(raw).hexdigest(),
                  malformed_colouring_rejected=True, full_composition_selection_family_closed=False,
                  old_supports_four_colourable=[870,869], realized_canonical_old_interface_class=canonical,
                  record_improvement=False, native_solver_required=False)
    expected = HERE / 'expected.json'
    if expected.exists():
        require(json.loads(json.dumps(result)) == json.loads(expected.read_text()), 'expected result')
    return dict(result=result, seconds=time.monotonic()-start, direct_native_cnf_comparison=compare_cnf is not None)


def controls():
    basis = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    for i, a in enumerate(basis):
        square = 1
        for prime, exponent in zip(PRIMES, POWERS[i]):
            square *= prime**exponent
        require(multiply(a, a) == (square,) + (0,)*7, 'basis square')
        for b in basis:
            require(multiply(a,b) == multiply(b,a), 'commutativity')
    zero = (0,)*8
    O = (zero, zero)
    X = ((288,)+(0,)*7, zero)
    Y = ((144,)+(0,)*7, (0,144)+(0,)*6)
    require(all(distance(a,b) == UNIT for a,b in combinations((O,X,Y),2)), 'equilateral triangle')
    require(distance(O,O) == zero, 'zero distance')
    require(distance(O,((576,)+(0,)*7,zero)) == (4*288**2,)+(0,)*7, 'nonunit distance')
    return dict(basis_squares=8, commutativity_pairs=64, unit_triangle_edges=3, zero_distance=1, nonunit_distance=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report', type=Path)
    ap.add_argument('--compare-cnf', type=Path)
    args = ap.parse_args()
    result = audit(args.compare_cnf)
    result['controls'] = controls()
    raw = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.report:
        args.report.write_text(raw)
    print(raw, end='')


if __name__ == '__main__':
    main()
