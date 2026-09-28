#!/usr/bin/env python3
"""Exact component inclusions and regressions for the annular exchange proof."""
import argparse
from collections import Counter
import importlib.util
import itertools
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'construction', HERE.parent/'planar_two_geodesic_light_attachment_transfer'/'verify.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
require = base.require


def ears(g, k, sector, order):
    a, b = 1+sector, 1+(sector+1) % k
    inside = list(range(len(g.adj), len(g.adj)+order))
    g.adj.extend({} for _ in inside)
    for u, v in zip([a]+inside, inside+[b]):
        g.edge(u, v, 1)
    face = next(f for f in g.faces if any((u, v) == (a, b)
                for u, v in zip(f, f[1:]+f[:1])))
    expanded = []
    for u, v in zip(face, face[1:]+face[:1]):
        expanded.append(u)
        if (u, v) == (a, b):
            expanded.extend(inside)
    g.faces.remove(face)
    g.faces.extend([tuple(expanded), tuple([a, b]+inside[::-1])])
    chain = inside+[b]
    bags = [{a, x, y} for x, y in zip(chain, chain[1:])]
    g.pieces.append(dict(internal=set(inside), boundary={a, b}, bags=bags,
                         tree=[(i, i+1) for i in range(len(bags)-1)]))


def octahedron(g, k, sector):
    interface = (0, 1+sector, 1+(sector+1) % k)
    mapping = {0:interface[0], 1:interface[2], 2:interface[1]}
    inside = set()
    for i in range(3, 6):
        mapping[i] = len(g.adj)
        inside.add(len(g.adj))
        g.adj.append({})
    for i, j in itertools.combinations(range(6), 2):
        if j-i != 3:
            g.edge(mapping[i], mapping[j], 1)
    guest = []
    for a, b, c in itertools.product((0, 3), (1, 4), (2, 5)):
        order = (a, b, c) if sum(v >= 3 for v in (a, b, c)) % 2 == 0 else (a, c, b)
        guest.append(tuple(mapping[v] for v in order))
    g.faces.remove(interface)
    guest.remove((interface[0], interface[2], interface[1]))
    g.faces.extend(guest)
    g.pieces.append(dict(internal=inside, boundary=set(interface)))


def system(g, k, shift=0, reverse=False):
    S = set(range(2*k+1))
    A = [1+(shift+(-i if reverse else i)) % k for i in range(k)]
    C = [1+k+(shift+(1-i if reverse else i)) % k for i in range(k)]
    P = (0, A[0], C[0])
    variables = {('e', i) for i in range(k)} | {(t, i) for t in ('a', 'c') for i in range(1, k)}
    mapping = {v:None for v in P}
    for i in range(1, k):
        mapping[A[i]], mapping[C[i]] = ('a', i), ('c', i)
    outside = g.components(S)
    for K in outside:
        N = set().union(*(set(g.adj[v]) for v in K)) & S
        Y = N & set(A)
        require(N <= {0} | Y and len(Y) <= 2, 'local active boundary')
        if len(Y) == 2:
            choices = [i for i in range(k) if Y == {A[i], A[(i+1) % k]}]
            require(len(choices) == 1, 'one cyclic sector')
            var = ('e', choices[0])
        elif len(Y) == 1 and A[0] not in Y:
            var = ('a', A.index(next(iter(Y))))
        else:
            var = None
        mapping.update((v, var) for v in K)
    require(set(mapping) == set(range(len(g.adj))), 'mass coordinates cover vertices')

    def atom(t, i):
        item = (t, i % k)
        return {item} if item in variables else set()

    def bounds(i):
        left = {(t, j) for j in range(i) for t in ('a', 'c', 'e')} & variables
        right = variables-left-atom('a', i)-atom('c', i)
        return left, right

    def prepare(q, left, right, kind, i):
        require(left <= variables and right <= variables and not left & right, 'disjoint formal sides')
        parts = g.components(set(P) | set(q))
        for R in parts:
            if R & S:
                coords = {mapping[v] for v in R}
                require(None not in coords and (coords <= left or coords <= right), 'symbolic component inclusion')
            else:
                require(any(R == K for K in outside), 'one whole detached component')
        return dict(q=q, left=left, right=right, parts=parts, kind=kind, i=i)

    sequence, detours = [], []
    for i in range(k):
        lu, ru = bounds(i)
        lv, rv = lu | atom('c', i), ru-atom('c', i+1)
        sequence.append(prepare((0, A[i], C[i]), lu, ru, 'U', i))
        sequence.append(prepare((0, A[i], C[(i+1) % k]), lv, rv, 'V', i))
        require(not ru & lv and ru | lv <= variables, 'inner-step heavy sides disjoint')
        ln, rn = bounds(i+1)
        plus = prepare((A[i], A[(i+1) % k], C[(i+2) % k]),
                       lv | atom('c', i+1), rn, '+', i)
        minus = prepare((A[(i+1) % k], A[i], C[i]),
                        lv, rn | atom('c', i+1), '-', i)
        detours.append((plus, minus))
        four = [rv, ln, plus['left'], minus['right']]
        coeff = Counter(v for side in four for v in side)
        require(all(coeff[v] == 2-int(v in atom('a', i) | atom('a', i+1))
                    for v in variables), 'four-heavy-side coefficient identity')
    lk, rk = bounds(k)
    sequence.append(prepare(P, lk, rk, 'U', k))
    return dict(P=P, S=S, mapping=mapping, outside=outside,
                sequence=sequence, detours=detours, variables=variables)


def complete(g, sys, weights, result):
    values = dict.fromkeys(sys['variables'], 0)
    discarded = 0
    for v, mass in enumerate(weights):
        var = sys['mapping'][v]
        if var is not None:
            values[var] += mass
        elif v not in sys['P']:
            discarded += mass
    M = sum(values.values())
    B = max((sum(weights[v] for v in K) for K in sys['outside']), default=0)
    W = sum(weights)
    require(M == W-sum(weights[v] for v in sys['P'])-discarded, 'mass identity')
    bound2 = max(M, 2*B)

    def value(side):
        return sum(values[v] for v in side)

    chosen = None
    previous = None
    for cut in sys['sequence']:
        left, right = value(cut['left']), value(cut['right'])
        if 2*max(left, right) <= bound2:
            chosen = cut
            result['spoke_choices'] += 1
            break
        require(not (2*left > bound2 and 2*right > bound2), 'one heavy side')
        if previous is not None and previous[1] and 2*left > bound2:
            prev = previous[0]
            require(prev['kind'] == 'V' and cut['kind'] == 'U', 'only sector step can cross')
            for option in sys['detours'][prev['i']]:
                if 2*max(value(option['left']), value(option['right'])) <= bound2:
                    chosen = option
                    result['exchange_choices'] += 1
                    break
            require(chosen is not None, 'four-term exchange finds a path')
            break
        previous = (cut, 2*right > bound2)
    require(chosen is not None, 'sweep terminates')
    maximum = max((sum(weights[v] for v in R) for R in chosen['parts']), default=0)
    require(2*maximum <= bound2, 'sharper full-graph residual bound')
    if 2*B <= W:
        require(2*maximum <= W, 'half balance for light components')
        result['light_half_checks'] += 1
    result['completion_checks'] += 1
    result['discarded_mass_checks'] += int(discarded > 0)
    return chosen, B


def heavy(g, d, w, result):
    piece = next(p for p in g.pieces if 2*sum(w[v] for v in p['internal']) > sum(w))
    for bag in piece['bags']:
        if all(2*sum(w[v] for v in R) <= sum(w) for R in g.components(bag)):
            ps = base.cover_bag(g, bag, d)
            for p in ps:
                g.check_path(p, d)
            deleted = set().union(*map(set, ps))
            require(all(2*sum(w[v] for v in R) <= sum(w) for R in g.components(deleted)), 'global centroid witness')
            result['heavy_checks'] += 1
            return
    raise AssertionError('no local centroid')


def abstract(k):
    g, _ = base.annulus(k)
    for i in range(k):
        for N in ((0, 1+i, 1+(i+1) % k), (1+i, 1+(i+1) % k), (0, 1+i)):
            x = len(g.adj)
            g.adj.append({})
            for v in N:
                g.edge(x, v, 1)
    x = len(g.adj)
    g.adj.append({})
    g.edge(0, x, 1)
    return g


def main():
    result = dict(symbolic_annuli=0, symbolic_spokes=0, symbolic_cut_checks=0,
                  coefficient_identities=0, fixtures=0, local_decompositions=0,
                  completion_checks=0, light_half_checks=0, discarded_mass_checks=0,
                  spoke_choices=0, exchange_choices=0, heavy_checks=0,
                  nonuniform_fixtures=0, octahedral_pockets=0,
                  rooted_paths=0, rooted_pairs=0, rooted_optimum=0,
                  strict_fixture_vertices=0, fixed_spoke_witness_maximum=0,
                  aggregate_heavy_sector_checks=0, rejected_c_boundary=0)
    for k in range(3, 41):
        g = abstract(k)
        for reverse in (False, True):
            sys = system(g, k, reverse=reverse)
            result['symbolic_spokes'] += 1
            result['symbolic_cut_checks'] += 4*k+1
            result['coefficient_identities'] += k
        result['symbolic_annuli'] += 1
    # Exact control: a component on C-boundaries is outside this theorem.
    bad, _ = base.annulus(5)
    x = len(bad.adj)
    bad.adj.append({})
    bad.edge(x, 6, 1)
    bad.edge(x, 7, 1)
    try:
        system(bad, 5)
    except AssertionError as error:
        require(str(error) == 'local active boundary', 'expected boundary rejection')
        result['rejected_c_boundary'] = 1
    require(result['rejected_c_boundary'] == 1, 'C-boundary rejected')

    specs = [(3, 2, [0, 1, 2], 1, 1, False, False),
             (6, 3, [0, 2, 4], 1, 1, False, False),
             (9, 3, list(range(9)), 1, 1, False, False),
             (7, 3, list(range(7)), 2, 1, True, False),
             (8, 2, [1, 3, 5, 7], 1, 1, False, True),
             (5, 0, list(range(5)), 1, 1, False, False)]
    rng = random.Random(2026092811)
    for k, m, sites, scale, pocket_length, long_rim, multiple in specs:
        g, _ = base.annulus(k)
        for u, row in enumerate(g.adj):
            for v in row:
                row[v] *= scale
        if long_rim:
            for i in range(k):
                u, v = 1+k+i, 1+k+(i+1) % k
                g.adj[u][v] = g.adj[v][u] = scale*(2+i % 3)
        core_dist = g.distances()
        for i in sites:
            if m:
                g.attach(m, (0, 1+i, 1+(i+1) % k), long_edges=pocket_length)
            else:
                octahedron(g, k, i)
                result['octahedral_pockets'] += 1
        if multiple:
            for i in range(k):
                ears(g, k, i, 3)
                ears(g, k, i, 4)
            g.attach(3, (0, 1))
        g.sphere()
        d = g.distances()
        require(all(d[u][v] == core_dist[u][v] for u in range(2*k+1)
                    for v in range(2*k+1)), 'core isometry')
        if m:
            for piece in g.pieces:
                g.check_local_decomposition(piece)
                result['local_decompositions'] += 1
        result['fixtures'] += 1
        result['nonuniform_fixtures'] += int(scale != pocket_length or long_rim)
        systems = [system(g, k, shift, reverse) for shift in range(k) for reverse in (False, True)]
        for sys in systems:
            g.check_path(sys['P'], d)
            for cut in sys['sequence'] + [q for pair in sys['detours'] for q in pair]:
                g.check_path(cut['q'], d)
        weights = list(base.masses(g, rng))
        if multiple:
            selected = [p for p in g.pieces if p['boundary'] == {1, 2}]
            require(len(selected) == 2, 'two separate components in sector zero')
            inside = set().union(*(p['internal'] for p in selected))
            w = [20 if v in inside else 1 for v in range(len(g.adj))]
            require(2*sum(w[v] for v in inside) > sum(w), 'aggregate sector is heavy')
            require(all(2*sum(w[v] for v in p['internal']) <= sum(w) for p in g.pieces), 'individual components light')
            weights.append(w)
            result['aggregate_heavy_sector_checks'] += len(systems)
        for w in weights:
            for sys in systems:
                _, B = complete(g, sys, w, result)
            if m and 2*B > sum(w):
                heavy(g, d, w, result)
        if (k, m) == (6, 3):
            n = len(g.adj)
            rooted = list(g.paths(0, range(n), d))
            explicit = {(0,)} | {(0, v) for v in g.adj[0]}
            explicit |= {(0, 1+i, 1+k+j % k) for i in range(k) for j in (i, i+1)}
            require(set(rooted) == explicit, 'all rooted geodesics enumerated')
            pairs = list(itertools.combinations_with_replacement(rooted, 2))
            optimum = min(max(map(len, g.components(set(p) | set(q))), default=0) for p, q in pairs)
            require(n == 43 and optimum == 23 and 2*optimum > n, 'rooted obstruction')
            P, Q = (0, 1, 7), (3, 4, 11)
            g.check_path(P, d)
            g.check_path(Q, d)
            maximum = max(map(len, g.components(set(P) | set(Q))))
            require(maximum == 14, 'local witness')
            require(all(len(K) == 10 and 2*len(K) < n for K in g.components(range(13))), 'three light pockets')
            result.update(rooted_paths=len(rooted), rooted_pairs=len(pairs), rooted_optimum=optimum,
                          strict_fixture_vertices=n, fixed_spoke_witness_maximum=maximum)
    require(result['exchange_choices'] > 0, 'exchange is exercised')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = main()
    if args.check:
        require(output == json.loads((HERE/'expected.json').read_text()), 'expected output')
    print(json.dumps(output, indent=2, sort_keys=True))
