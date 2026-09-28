#!/usr/bin/env python3
"""Exact regression checks; the all-order theorem has a written proof."""
import argparse
from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'previous_transfer', HERE.parent / 'planar_two_geodesic_light_attachment_transfer' / 'verify.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
require = base.require


def subdivide(g, u, v, lengths):
    require(sum(lengths) >= g.adj[u][v], 'rim length does not decrease')
    del g.adj[u][v]
    del g.adj[v][u]
    inner = list(range(len(g.adj), len(g.adj) + len(lengths)-1))
    g.adj.extend({} for _ in inner)
    chain = [u] + inner + [v]
    for a, b, length in zip(chain, chain[1:], lengths):
        g.edge(a, b, length)
    faces = []
    for face in g.faces:
        expanded = []
        for a, b in zip(face, face[1:] + face[:1]):
            expanded.append(a)
            if (a, b) == (u, v):
                expanded.extend(inner)
            elif (a, b) == (v, u):
                expanded.extend(reversed(inner))
        faces.append(tuple(expanded))
    g.faces = faces
    return set(inner)


def fixture(k, m, sites, scale=1, pocket_length=1, stretch=False, singles=()):
    g, C = base.annulus(k)
    for row in g.adj:
        for v in row:
            row[v] *= scale
    if stretch:
        for i in range(k):
            u, v = 1+k+i, 1+k+(i+1) % k
            if i % 2:
                g.adj[u][v] = g.adj[v][u] = 3*scale
            else:
                C |= subdivide(g, u, v, [scale, 1, scale])
    S = set(range(len(g.adj)))
    old_dist = g.distances()
    for i in sites:
        g.attach(m, (0, 1+i, 1+(i+1) % k), long_edges=pocket_length)
    for i in singles:
        g.attach(m, (0, 1+i), long_edges=pocket_length)
    g.sphere()
    dist = g.distances()
    require(all(dist[u][v] == old_dist[u][v] for u in S for v in S), 'isometric core')
    for piece in g.pieces:
        g.check_local_decomposition(piece)
    return g, C, S, dist


def covers(k, sites):
    edges = [{1+i, 1+(i+1) % k} for i in sites]
    return [(a, b) for a in range(1, k+1) for b in range(a+1, k+1)
            if (b-a) not in (1, k-1) and all({a, b} & edge for edge in edges)]


def boundary(g, K, S):
    return set().union(*(set(g.adj[v]) for v in K)) & S


def transfer(g, S, p, qs, parts_by_q, w, result, whole_core):
    P = set(p)
    outside = g.components(S | P)
    proxy = [w[v] if v in S-P else 0 for v in range(len(w))]
    discarded = largest = 0
    W = sum(w)
    for K in outside:
        mass = sum(w[v] for v in K)
        largest = max(largest, mass)
        if mass == 0:
            continue
        N = boundary(g, K, S-P)
        require(len(N) <= 1, 'one surviving support neighbor')
        require(2*mass <= W, 'light outside component')
        if N:
            proxy[next(iter(N))] += mass
        else:
            discarded += mass
    M = sum(proxy)
    require(M == W-sum(w[v] for v in P)-discarded, 'mass identity')
    witnesses = 0
    for q, parts in zip(qs, parts_by_q):
        if any(2*sum(proxy[v] for v in R) > M for R in parts):
            continue
        witnesses += 1
        for R in parts:
            actual = sum(w[v] for v in R)
            require(2*actual <= max(M, 2*largest), 'sharper bound')
            require(2*actual <= W, 'original half bound')
            if R & S:
                require(actual <= sum(proxy[v] for v in R), 'partial attachment inequality')
            else:
                require(any(R <= K for K in outside), 'one original outside component')
        if set(q)-whole_core and W and all(w[v] > 0 for v in range(len(w))):
            result['positive_mass_witnesses_entering_attachments'] += 1
        result['proxy_balanced_pairs_checked'] += 1
    require(witnesses > 0, 'sweep completion exists')
    result['transfer_checks'] += 1
    result['first_path_outside_support_checks'] += int(not P <= S)


def heavy(g, dist, w, result):
    piece = next(p for p in g.pieces if 2*sum(w[v] for v in p['internal']) > sum(w))
    for bag in piece['bags']:
        if all(2*sum(w[v] for v in R) <= sum(w) for R in g.components(bag)):
            paths = base.cover_bag(g, bag, dist)
            for p in paths:
                g.check_path(p, dist)
            deleted = set().union(*map(set, paths))
            require(all(2*sum(w[v] for v in R) <= sum(w) for R in g.components(deleted)), 'heavy witness')
            result['heavy_checks'] += 1
            return
    raise AssertionError('no local centroid bag')


def main():
    result = dict(core_distance_annuli=0, ordered_distance_checks=0,
                  cover_subsets_checked=0, fixtures=0, local_decompositions=0,
                  transfer_checks=0, proxy_balanced_pairs_checked=0,
                  positive_mass_witnesses_entering_attachments=0,
                  first_path_outside_support_checks=0, heavy_checks=0,
                  strict_fixture_vertices=0, strict_core_order=0,
                  strict_geodesic_union_order=0, old_boundary_failures=0,
                  rejected_three_disjoint_sectors=0, rejected_shortening_control=0,
                  zero_mass_multiboundary_controls=0)
    # Check the distance formula over all roots and nonadjacent pairs.
    for k in range(5, 51):
        g, C = base.annulus(k)
        d = g.distances()
        for a in range(1, k+1):
            require(base.support(d, a, C) == set(range(2*k+1)), 'whole core visible')
            for b in range(1, k+1):
                if a == b or b in g.adj[a]:
                    continue
                c = next((v for v in C & set(g.adj[b]) if d[a][v] == 3), None)
                require(c is not None, 'nonadjacent active witness')
                g.check_path((a, 0, b, c), d)
                result['ordered_distance_checks'] += 1
        result['core_distance_annuli'] += 1
    # Every edge subset with a <=2 cover has a nonadjacent two-vertex cover.
    for k in range(5, 13):
        for mask in range(1 << k):
            sites = [i for i in range(k) if mask >> i & 1]
            any_cover = any(all(i in pair or (i+1) % k in pair for i in sites)
                            for pair in itertools.combinations(range(k), 2))
            require(bool(covers(k, sites)) == any_cover, 'cover conversion')
            result['cover_subsets_checked'] += 1
    require(not covers(9, [0, 3, 6]), 'three disjoint sectors outside hypothesis')
    result['rejected_three_disjoint_sectors'] = 1

    rng = random.Random(2026092810)
    specs = [(5, 2, [0, 2], 1, 1, False, ()),
             (8, 3, [0, 3], 1, 1, True, (6,)),
             (10, 3, [0, 1, 5, 6], 1, 1, False, (8,)),
             (9, 5, [0, 4], 2, 1, False, ()),
             (9, 5, [0, 4], 2, 1, True, (7,)),
             (12, 7, [0, 1, 6, 7], 2, 1, True, ())]
    for k, m, sites, scale, length, stretch, singles in specs:
        g, C, S, d = fixture(k, m, sites, scale, length, stretch, singles)
        result['fixtures'] += 1
        result['local_decompositions'] += len(g.pieces)
        weights = list(base.masses(g, rng))
        choices = []
        for a, b in covers(k, sites):
            for a, b in ((a, b), (b, a)):
                J = base.support(d, a, C)
                require(S <= J, 'core in facial union after attachments')
                cs = [c for c in C & set(g.adj[b]) if d[a][c] == 3*scale]
                require(cs, 'rerooted path after attachments')
                p = (a, 0, b, min(cs))
                g.check_path(p, d)
                qs = list(g.paths(a, C, d))
                for q in qs:
                    g.check_path(q, d)
                    require(set(q) <= J, 'second path in facial union')
                parts = [g.components(set(p) | set(q)) for q in qs]
                choices.append((p, qs, parts))
        require(choices, 'eligible boundary cover')
        for w in weights:
            if any(2*sum(w[v] for v in K) > sum(w) for K in g.components(S)):
                heavy(g, d, w, result)
            else:
                for p, qs, parts in choices:
                    transfer(g, S, p, qs, parts, w, result, S)
                p, qs, parts = choices[0]
                transfer(g, S-set(p), p, qs, parts, w, result, S)

        if (k, m, scale, stretch) == (9, 5, 2, False):
            p = (1, 0, 5, 14)
            J = base.support(d, 1, C)
            require(len(g.adj) == 51 and len(S) == 19 and len(J) == 22, 'strict fixture sizes')
            failures = [K for K in g.components(J) if len(boundary(g, K, J-set(p))) > 1]
            require(len(failures) == 2, 'old exact-union condition fails')
            require(all(2*len(K) <= len(g.adj) for K in failures), 'old outside pieces are light')
            require(all(len(boundary(g, K, S-set(p))) <= 1 for K in g.components(S)), 'new condition holds')
            result.update(strict_fixture_vertices=len(g.adj), strict_core_order=len(S),
                          strict_geodesic_union_order=len(J), old_boundary_failures=len(failures))
            # Force a positive-mass proxy witness that enters and deletes part of a pocket.
            qs = list(g.paths(1, C, d))
            parts = [g.components(set(p) | set(q)) for q in qs]
            q = (1, 19, 0, 8, 17)
            R = min(g.components(set(p) | set(q)), key=len)
            w = [1]*len(g.adj)
            w[min(R & (S-set(p)-set(q)))] += 3
            transfer(g, S, p, qs, parts, w, result, S)
            # A zero-mass component with two surviving neighbors stays in G.
            p = (1, 0, 3, 13)
            g.check_path(p, d)
            w = [int(v not in g.pieces[1]['internal']) for v in range(len(g.adj))]
            require(len(boundary(g, g.pieces[1]['internal'], S-set(p))) == 2,
                    'zero-mass component has two surviving neighbors')
            parts = [g.components(set(p) | set(q)) for q in qs]
            transfer(g, S, p, qs, parts, w, result, S)
            result['zero_mass_multiboundary_controls'] = 1
            # A new route strictly shorter than a core edge violates isometry.
            damaged = g.distances()
            g.adj[1][19] = g.adj[19][1] = 1
            g.adj[19][0] = g.adj[0][19] = Fraction(1, 2)
            require(g.distances()[1][0] < damaged[1][0], 'shortening is detected')
            result['rejected_shortening_control'] = 1
    require(result['positive_mass_witnesses_entering_attachments'] > 0, 'nonvacuous partial-attachment checks')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    answer = main()
    if args.check:
        require(answer == json.loads((HERE / 'expected.json').read_text()), 'expected output')
    print(json.dumps(answer, indent=2, sort_keys=True))
